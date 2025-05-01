"""                          
#without lambda aws
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def scrape_website(url, config):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    keywords = {keyword: 0 for keyword in config['keywords']}
    
    elements = soup.find_all(config['element_tag'], class_=config['element_class'])
    print(f"Found {len(elements)} elements with tag {config['element_tag']} and class {config['element_class']}")
    
    for e in elements:
        comment = e.get_text().lower().strip()
        
        #print if the comment is empty
        if not comment:
            print("Empty comment text found, skipping...")
            continue
        
        words = comment.split(" ")
        words = {w.strip(".,/:;!@") for w in words} 
        

        
        
        for k in keywords:
            if k in words:
                keywords[k] += 1
    
   
    return keywords


# function for graph
def plot_keywords(keywords):
    plt.bar(keywords.keys(), keywords.values())
    plt.xlabel("Language")
    plt.ylabel("# of Mentions")
    plt.title("Technology Mentions in Comments")
    plt.show()


def main():
    config = {
        "example1": {
            "url": "https://news.ycombinator.com/item?id=42919502",
            "element_tag": "div", 
            "element_class": "comment", 
            "keywords": ["python", "javascript", "go", "java", "rust"]
        },
        
        
    }
    website_key = "example1" 
    site_config = config[website_key]
    
  
    keywords = scrape_website(site_config['url'], site_config)

    # Plot the results
    plot_keywords(keywords)


if __name__ == "__main__":
    main()


#with Serverless API


import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def scrape_website(url, config):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    keywords = {keyword: 0 for keyword in config['keywords']}
    
   
    elements = soup.find_all(config['element_tag'], class_=config['element_class'])
    
    for e in elements:
        comment = e.get_text().lower().strip()
        
        if not comment:
            print("Empty comment text found, skipping...")
            continue
        
        words = comment.split(" ")
        words = {w.strip(".,/:;!@") for w in words}
        
        for k in keywords:
            if k in words:
                keywords[k] += 1
    
    return keywords

def lambda_handler(event, context):
    try:
        url = event['url']
        config = event['config']
        keyword_counts = scrape_website(url, config)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Scraping successful!',
                'keyword_counts': keyword_counts
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
def plot_keywords(keywords):
    plt.bar(keywords.keys(), keywords.values())
    plt.xlabel("Keyword")
    plt.ylabel("Mentions")
    plt.title("Keyword Mentions")
    plt.show()


def main():
    event = {
        "url": "https://news.ycombinator.com/item?id=42919502",
        "config": {
            "element_tag": "div",
            "element_class": "comment",  
            "keywords": ["python", "javascript", "go", "java", "rust"]
        }
    }

    result = lambda_handler(event, None)
    print(json.dumps(json.loads(result['body']), indent=2))

    if result['statusCode'] == 200:
        keyword_counts = json.loads(result['body'])['keyword_counts']
        plot_keywords(keyword_counts)

if __name__ == "__main__":
    main()
"""

"""
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run headlessly
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_with_selenium(url, config):
    driver = setup_driver()
    driver.get(url)
    time.sleep(3)  # Wait for JS-rendered content to load

    elements = driver.find_elements(By.CLASS_NAME, config["element_class"])
    
    keywords = {keyword: 0 for keyword in config["keywords"]}
    raw_data = []
    data=[]

    for e in elements:
        comment = e.text.lower().strip()
        if not comment:
            continue

        words = {w.strip(".,/:;!@") for w in comment.split()}
        for k in keywords:
            if k in words:
                keywords[k] += 1
        data.append({"words": words})
    raw_data.append({"keywords": keywords})

    driver.quit()

    # Save to CSV the final result 
    df = pd.DataFrame(raw_data)
    df.to_csv("keywords.csv", index=False)
    print("Comments saved to keywords.csv")
    d = pd.DataFrame(data)
    d.to_csv("scraped_comments.csv", index=False)
    print("Comments saved to scraped_comments.csv")

    return keywords

def lambda_handler(event, context):
    try:
        url = event['url']
        config = event['config']
        keyword_counts = scrape_with_selenium(url, config)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Scraping successful!',
                'keyword_counts': keyword_counts
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def plot_keywords(keywords):
    plt.bar(keywords.keys(), keywords.values())
    plt.xlabel("Keyword")
    plt.ylabel("Mentions")
    plt.title("Keyword Mentions")
    plt.show()
    #also i save the figure
    plt.savefig("keyword_mentions.png")

def main():
    event = {
        "url": "https://news.ycombinator.com/item?id=42919502",
        "config": {
            "element_tag": "a",
            "element_class": "comment",
            "keywords": ["python", "javascript", "go", "java", "rust"]
        }
    }

    result = lambda_handler(event, None)
    print(json.dumps(json.loads(result['body']), indent=2))

    if result['statusCode'] == 200:
        keyword_counts = json.loads(result['body'])['keyword_counts']
        plot_keywords(keyword_counts)

if __name__ == "__main__":
    main()

"""

import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request, send_file

# Flask setup
app = Flask("scrap")

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run headlessly
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_with_selenium(url, config):
    driver = setup_driver()
    driver.get(url)
    time.sleep(3)  # Wait for JS-rendered content to load

    elements = driver.find_elements(By.CLASS_NAME, config["element_class"])
    
    keywords = {keyword: 0 for keyword in config["keywords"]}
    raw_data = []
    data = []

    for e in elements:
        comment = e.text.lower().strip()
        if not comment:
            continue

        words = {w.strip(".,/:;!@") for w in comment.split()}
        for k in keywords:
            if k in words:
                keywords[k] += 1
        data.append({"words": words})
    raw_data.append({"keywords": keywords})

    driver.quit()

    # Save to CSV the final result 
    df = pd.DataFrame(raw_data)
    df.to_csv("keywords.csv", index=False)
    print("Comments saved to keywords.csv")
    d = pd.DataFrame(data)
    d.to_csv("scraped_comments.csv", index=False)
    print("Comments saved to scraped_comments.csv")

    return keywords

def plot_keywords(keywords):
    plt.bar(keywords.keys(), keywords.values())
    plt.xlabel("Keyword")
    plt.ylabel("Mentions")
    plt.title("Keyword Mentions")
    
    
    # Save the figure
    plt.savefig("keyword_mentions.png")
    print("Figure saved as 'keyword_mentions.png'")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        keywords_input = request.form['keywords']
        element_tag = request.form['element_tag']
        element_class = request.form['element_class']
        keywords = keywords_input.split(",")  # Get keywords from input (comma separated)

        config = {
            "element_tag": element_tag,  # Get the element tag input
            "element_class": element_class,  # Get the element class input
            "keywords": [keyword.strip() for keyword in keywords]
        }

        # Scrape and get keyword counts
        keyword_counts = scrape_with_selenium(url, config)

        # Generate and display plot
        plot_keywords(keyword_counts)

        # Render results in HTML
        return render_template('index.html', keyword_counts=keyword_counts)

    return render_template('index.html', keyword_counts=None)

@app.route('/download_csv')
def download_csv():
    # Serve the scraped comments CSV file
    return send_file('scraped_comments.csv', as_attachment=True)

@app.route('/download_keywords_csv')
def download_keywords_csv():
    # Serve the keywords CSV file
    return send_file('keywords.csv', as_attachment=True)

@app.route('/download_plot')
def download_plot():
    # Serve the keyword plot figure
    return send_file('keyword_mentions.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
