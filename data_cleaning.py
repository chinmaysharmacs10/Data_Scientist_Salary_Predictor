import pandas as pd

df = pd.read_csv("glassdoor_jobs.csv")

# salary
df = df[df['Salary Estimate']!='-1']   # remove rows with -1 in salary estimate
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])            # remove (Glassdoor est.)
salary_nums = salary.apply(lambda x: x.replace('K','').replace('$',''))    # remove K and $

df['hourly_salary'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)   # mark rows which have salary per hour
df['employer_provided_salary'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)  # mark rows which have employer provided salary

salary_clean = salary_nums.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))  # remove 'per hour' and 'employer provided salary' from salary

df['min_salary'] = salary_clean.apply(lambda x: int(x.split('-')[0]))       # take the min salary amount from salary range
df['max_salary'] = salary_clean.apply(lambda x: int(x.split('-')[1]))       # max salary amount from salary range
df['avg_salary'] = (df.min_salary + df.max_salary)/2


# extract only the name of the company, remove the rating
df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-4],axis=1)

# extract the state from the location of the job
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
#df.job_state.value_counts()   # describes how many jobs are in each state
# check if headquarters is in the same state as the job location
df['same_state'] = df.apply(lambda x: 1 if x.Location==x.Headquarters else 0, axis=1)

# if entry is -1 then keep it -1, else 2020-founded year
df['company_age'] = df.Founded.apply(lambda x: x if x<1 else 2020-x)


# Look for python, R studio, excel, spark, aws

df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
# df.python.value_counts()

df['r_studio'] = df['Job Description'].apply(lambda x: 1 if 'r-studio' in x.lower() or 'r studio' in x.lower() else 0)
# df.r_studio.value_counts()

df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
# df.spark.value_counts()

df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
# df.aws.value_counts()

df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
# df.excel.value_counts()

df_out = df.drop(['Unnamed: 0'], axis=1)
df_out.to_csv('salary_data_cleaned.csv',index=False)