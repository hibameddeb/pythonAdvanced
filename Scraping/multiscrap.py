"""
without lambda aws
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

"""
#with Serverless API

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def scrape_website(url, config):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.prettify())
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
        
      
        print(f"Words in comment: {words}")
        
        
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
            "url": "https://dev.to/",
            "element_tag": "div", 
            "element_class": "comment", 
            "keywords": ["python", "javascript", "go", "java", "springboot"]
        },
        
        
    }
    website_key = "example1" 
    site_config = config[website_key]
    
  
    keywords = scrape_website(site_config['url'], site_config)

    # Plot the results
    plot_keywords(keywords)


if __name__ == "__main__":
    main()


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
