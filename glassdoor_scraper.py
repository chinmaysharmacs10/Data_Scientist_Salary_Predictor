from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, path, slp_time):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')    # so that a new Chrome window does not open, scraping done in background

    # Used Google Chrome's web driver
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="

    driver.get(url)
    jobs = []      # Initializing an empty list to collect data about each job

    while len(jobs) < num_jobs:  # If true look for new jobs.
        time.sleep(slp_time)     # sleep time is added so that scraping is not too fast or multiple links are not accessed at once

        # To remove the sign-up window every time we go to new page
        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()   # random click to open sign-up window
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  # clicking on the X to close signup window.
        except NoSuchElementException:
            pass


        # To extract all jobs on a page
        job_buttons = driver.find_elements_by_class_name("jl")    # list of all job postings on the page
        for job_button in job_buttons:
            #print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:   # if required no. of jobs scraped then stop
                break

            job_button.click()    # to click on a job in the jobs list
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            # extract the range of salary given for the job
            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1

            # extract the rating of the company
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1


            # Go to the company tab inside each job posting
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()  # to click on the company tab

                # extract the location of headquarters of the company
                try:
                    headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                # extract size of company (based on no. of employees)
                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                # extract the year the company was established
                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                # extract type of ownership of the company
                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                # extract the industry the company belongs to
                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                # extract the sector the company belongs to
                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                # extract the revenue generated by the company
                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                # extract the names of the competitors
                try:
                    competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:    # in case the job posting does not have a company tab
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1


            # Add all the details as dictionary to the jobs list
            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})

        # To go to the next page
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()   # to click next arrow button
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,len(jobs)))
            break

    return pd.DataFrame(jobs)  # convert the dictionary object into a pandas DataFrame.

