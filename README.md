# Data Scientist's Salary Predictor
* Created a model that estimates a data scientist's annual salary based on various parameters. This would help data scientists in negotiating their salary by getting an estimate of the salary they should receive as per the parameters of the company and job offer. 
* The model estimates annual salary with mean_absolute_error = 10.95 i.e, estimates salary with error arround $11,000.

* Used __Selenium__ in __Python__ to scrape around 1000 job postings from Glassdoor.com
* Cleaned the scraped data of missing values and extracted information about skills (Python, R, AWS, Excel & Spark) required for a particular job from the text of each job description. 
* Exploratory data analysis done on data to understand correlation between different parameters and effect of different parameters on average salary.
* Optimized and compared __Multiple Linear Regression__ , __Lasso Regression__ & __Random Forest Regressor__ to obtain the best model for prediction.
* Built a client facing API using __Flask__.

* __Python version__: 3.6.10
* __Libraries used__: pandas, numpy, matplotlib, seaborn, sklearn, pickle, flask, json 

## Scraping Glassdoor.com for Jobs
###### (File: glassdoor_scraper.py & data_collection.py)
Reference Article: https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905.

Reference Code: https://github.com/arapfaik/scraping-glassdoor-selenium.

Used the above article and code for reference to scrape around 1000 data scientist jobs in U.S. from Glassdoor (File: glassdoor_jobs.csv). Run the data_collection.py file to start scraping.

We get the following columns for each job:
  * Job title
  * Salary Estimate
  * Job Description
  * Rating
  * Company
  * Location
  * Company Headquarters
  * Company Size
  * Company Founded Date
  * Type of Ownership
  * Industry
  * Sector
  * Revenue
  * Competitors
  
## Cleaning the Data
###### (File: data_cleaning.ipynb & data_analysis_EDA.ipynb)
The scraped data was cleaned to be used for our model. (File: model_data.csv).

The following changes were made:
  * Removed rows without salary data.
  * Extracted numeric data from salary column to make new columns for min_salary & max_salary, calculated avg_salary using them.
  * New column for state in which company is located.
  * New columns to depict hourly salary & employer provided salary.
  * New column for age of the company, which is calculated using founded data.
  * New columns to depict which skill(s) (Python, R, Excel, AWS, Spark) is/are present in the job description.
  * New column for job title (data scientist, data engineer, machine learning engineer, analyst, manager, director).
  * New column for seniority (senior, junior). 
  
## Exploratory Data Analysis (EDA)
###### (File: data_analysis_EDA.ipynb)
* Explored the distributions of data and value counts for different categorical variables. 
* Plotted __heatmap to visualize correlation__ between different parameters and average salary.
* Plotted __histograms of value counts vs category of different parameters__ like location, size of company, type of ownership, industry, sector, revenue, etc. to see the distribution of data in each category.
* Made __pivot tables for average salary based on different parameters__ like job position, seniority, job state, industry, sector, revenue, type of ownership, required skills, etc. to observe the salary provided in each category.

![alt text](https://github.com/chinmaysharmacs10/Data_Scientist_Salary_Predictor/blob/master/Pictures/correlation.png "Correlation between parameters and average salary")
![alt text](https://github.com/chinmaysharmacs10/Data_Scientist_Salary_Predictor/blob/master/Pictures/location.png "Location vs number of jobs")
![alt text](https://github.com/chinmaysharmacs10/Data_Scientist_Salary_Predictor/blob/master/Pictures/pivot_table.PNG "Pivot table")


## Building the Prediction Model
###### (File: prediction_model.py)
* The categorical variables (ex: Type of ownership, Industry, Sector, job state, job position, etc.) were transformed into dummy variables.
* The data was split into train and test set, with 20% of data as test set.
* Three models were tried to make prediction and were evaluated using mean_absolute_error.
  1. __Multiple Linear Regression__: Mean Absolute Error = 19.53
     It tries to fit a single line through multi-dimensional space. It did not perform well due to the sparse distribution of the data.
  2. __Lasso Regression__: Mean Absolute Error = 20.14
     It is a normalized regression. It is generally effective in case of sparse data distribution, but did not perform well here.
  3. __Random Forest Regressor (Best)__: Mean Absolute Error = __10.95__
     It is a tree based algorithm that has a number of decision trees to predict output value. It is effective in a sparse data distribution, hence performs best on our data. __GridsearchCV__ was used to find the best value of parameters for the random forest regressor.
     
* Since the Random Forest Regressor model outperform the other two, it is chosen as the prediction model.
* The model is then pickled so that it need not be trained again and again when a request is made via the API built in the next step.
     

## Productionization by making a Flask API
###### (File: Flask_API)
Reference Article: https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2.

* Built a flask API endpoint that was hosted on a local webserver. (File: Flask_API/app.py)
* The API endpoint takes in a request with a list of values from a job listing and returns the salary predicted by our model as response. (File: Flask_API/request.py)
* A sample response can be seen in (File: Flask_API/Sample_Request.ipynb), where the model predicts a salary of around $53,000 for a random data sample from the test set.

