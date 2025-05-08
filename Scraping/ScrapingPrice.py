from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_indeed_jobs(location, job_title):
    url = f"https://www.indeed.com/jobs?q={job_title}&l={location}"
    
    # Set up Selenium WebDriver (you can set headless mode here)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode, no browser UI
    service = Service(ChromeDriverManager().install())  # Automatically install and set path to chromedriver
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        
        # Wait for the job cards to load (wait for the first job card to appear)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-SerpJobCard")))
        
        jobs = []
        
        job_cards = driver.find_elements(By.CLASS_NAME, 'jobsearch-SerpJobCard')
        
        if not job_cards:
            print("No job cards found. The page might not have loaded properly.")
        
        for card in job_cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, 'a[title]').get_attribute('title')
                company = card.find_element(By.CLASS_NAME, 'company').text.strip()
                location = card.find_element(By.CLASS_NAME, 'location').text.strip()
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location
                })
            except Exception as e:
                print(f"Error parsing a job card: {e}")
        
        return jobs
    except Exception as e:
        print(f"Error fetching Indeed jobs: {e}")
        return []
    finally:
        driver.quit()

def main():
    location = input("Enter the location (e.g., New York, NY): ")
    job_title = input("Enter the job title (e.g., Software Engineer): ")
    
    print("\nFetching jobs from Indeed...")
    indeed_jobs = get_indeed_jobs(location, job_title)
    
    if indeed_jobs:
        for job in indeed_jobs:
            print(f"Title: {job['title']}, Company: {job['company']}, Location: {job['location']}")
    else:
        print("No jobs found on Indeed.")

if __name__ == '__main__':
    main()
