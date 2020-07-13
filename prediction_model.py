import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# import data
df = pd.read_csv('model_data.csv')

# Relevant data parameters for our model
df_model = df[['avg_salary','Rating','Size','Type of ownership','Industry','Sector','Revenue','no_of_competitors','hourly_salary','employer_provided_salary',
             'job state','same_state','company_age','python','spark','aws','excel','job position','seniority','description_len']]

# Get dummy data
df_dummy = pd.get_dummies(df_model)
#print(df_dummy.columns)


# Creating training and testing data
from sklearn.model_selection import train_test_split

X = df_dummy.drop('avg_salary', axis=1)           # every parameter apart from avg_salary is our independent variable
y = df_dummy.avg_salary.values                    # avg_salary is our dependent variable which is to be predicted

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


########################################## Choosing best model ################################################################################################


# Multiple Linear Regression Model
from sklearn.linear_model import LinearRegression       # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
from sklearn.model_selection import cross_val_score     # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html

multiple_lr = LinearRegression()
multiple_lr.fit(X_train,y_train)

multiple_cv = np.mean(cross_val_score(multiple_lr,X_train,y_train, scoring='neg_mean_absolute_error', cv=3))
# print(multiple_cv)            # we get -21.3963, that means error of around 15,000 dollars in prediction
# Multiple linear regression doesn't work well because of the sparsity of the data

#----------------------------------------------------------------------------------------------------------------------------------------

# Lasso Regression Model
from sklearn.linear_model import Lasso          # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html

# Find best value of alpha for Lasso regression
alpha = []
error = []
for i in range(1,100):
    alpha.append(i/100);
    lasso_regression = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lasso_regression,X_train,y_train, scoring='neg_mean_absolute_error', cv=3)))
# plt.plot(alpha,error)     # plot variation of error wrt alpha
# plt.show()

error_alpha_list = pd.DataFrame({'alpha':alpha,'error':error})   # make a panda data frame with alpha and error as columns
best_alpha = error_alpha_list[error_alpha_list.error == max(error_alpha_list.error)]    # find the alpha that corresponds to the least error
# print(best_alpha)

# We obtain best_alpha = 0.13 for error = -19.862132

lasso_r = Lasso(alpha=0.13)
lasso_r.fit(X_train,y_train)
lasso_cv = np.mean(cross_val_score(lasso_r,X_train,y_train, scoring='neg_mean_absolute_error', cv=3))
# print(lasso_cv)        # we get -19.8621, that means error of around 19,000 dollars in prediction

#----------------------------------------------------------------------------------------------------------------------------------------------------------

# Random Forest Model
from sklearn.ensemble import RandomForestRegressor    # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html

random_forest = RandomForestRegressor()
# n_estimators: number of trees in forest = 100 (default)
# criterion: criteria to measure quality of split = Mean Squared Error
# bootstrap = True
# min_samples_split: minimum no. of samples required to split internal node = 2
# max_features: number of features to consider when looking for the best split = 'auto'

random_forest_cv = np.mean(cross_val_score(random_forest,X_train,y_train, scoring='neg_mean_absolute_error', cv=3))
# print(random_forest_cv)    # we get -15.2529, that means error of around 15,000 dollars in prediction


###################################### Tuning Random Forest Model using GridsearchCV #############################################################


from sklearn.model_selection import GridSearchCV     # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}    # n_estimators goes from 10 to 300 at interval of 10

gs = GridSearchCV(random_forest,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

best_score = gs.best_score_              # gives the best neg_mean_absolute_error achieved from the model
best_parameters = gs.best_params_        # gives the parameter values for best_score

#print(best_score)           # we get -15.1890
#print(best_parameters)      # gives {'n_estimators':120, 'criterion':'mse', 'max_features':'auto'}


############################################ Use different models on X_test set #########################################################################################


# Make predictions using all the models on the X_test data
multiple_lr_pred = multiple_lr.predict(X_test)
lasso_r_pred = lasso_r.predict(X_test)
random_forest_pred = gs.best_estimator_.predict(X_test)           # we take the random_forest model with the best parameters feeded in i.e. best_estimator

# Used mean_absolute_error(mae) to find error in the predicted values
from sklearn.metrics import mean_absolute_error

multiple_lr_mae = mean_absolute_error(y_test,multiple_lr_pred)
lasso_r_mae = mean_absolute_error(y_test,lasso_r_pred)
random_forest_mae = mean_absolute_error(y_test,random_forest_pred)

print(multiple_lr_mae)     # gives mean_absolute_error = 19.53
print(lasso_r_mae)         # gives mean_absolute_error = 20.14
print(random_forest_mae)   # gives mean_absolute_error = 10.95  (best result)

# The Random Forest Model performs best on the test dataset as it did on the training dataset, so it is chosen as our prediction model


###################################################### Pickle the model #######################################################################


# pickle the model so that it does not need to train again when a request is make through the API
# https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2
import pickle

pickled_model = {'model':gs.best_estimator_}
pickle.dump(pickled_model,open('model_file' + ".p", "wb"))
# model_file.p (pickled random forest regressor) can be used to make predictions






