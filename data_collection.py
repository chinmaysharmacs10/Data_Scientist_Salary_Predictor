import glassdoor_scraper as gs
import pandas as pd

path = "C:/Users/Chinmay Sharma/PycharmProjects/Salary_Predictor/chromedriver"   # define the path where the chromedriver is in your computer

# call the scraper function to get data; (keyword='data+scientist', num_jobs=1000, path=path, slp_time=15)
df = gs.get_jobs('data+scientist',1000,path,15)

# store the data scraped in a csv file
df.to_csv('glassdoor_jobs.csv',index=False)