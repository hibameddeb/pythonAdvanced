"""
import requests

def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    response = requests.get(url)
    print(f"Scraping: {url}")
    print(response)
   #print(response.content)

if __name__ == "__main__":
  main()

 

import requests
from bs4 import BeautifulSoup

def main():
  url = "https://news.ycombinator.com/item?id=42919502"
  response = requests.get(url)

  soup = BeautifulSoup(response.content, "html.parser")
  # find all elements with class="comment"
  elements = soup.find_all(class_="comment")

  # Show the number of elementd found
  print(f"Elements: {len(elements)}")

if __name__ == "__main__":
  main()


import requests
from bs4 import BeautifulSoup

def main():
  url = "https://news.ycombinator.com/item?id=42919502"
  response = requests.get(url)

  soup = BeautifulSoup(response.content, "html.parser")
  # find all elements with class="ind" and indent level = 0
  elements = soup.find_all(class_="ind" , indent=0)
  # for each of this elements, find the next element
  comments = [e.find_next(class_="comment") for e in elements]

  # Show the number of comments found
  #print(f"Comments: {len(comments)}")
  

  # show each comment (job post) with  tags
  #for comment in comments:
  #print(comment)
  
  #print les elemnts choisis sous forme du text 
  for comment in comments:
    comment_text = comment.get_text()
    print(comment_text)

if __name__ == "__main__":
  main()

"""


import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def main():
  url = "https://news.ycombinator.com/item?id=42919502"
  response = requests.get(url)

  soup = BeautifulSoup(response.content, "html.parser")
  # find all elements with class="ind" and indent level = 0
  elements = soup.find_all(class_="ind" , indent=0)
  # for each of this elements, find the next element
  comments = [e.find_next(class_="comment") for e in elements]

  # Map of technologies keyword to search for
  # and the occurence initialized at 0
  keywords = {"python": 0, "javascript": 0, "typescript": 0, "go": 0, "c#": 0, "java": 0, "rust": 0 }

  # show each comment (job post)
  for comment in comments:
    # get the comment text and lower case it
    comment_text = comment.get_text().lower()

    # split comment by space which create an array of words
    words = comment_text.split(" ")
    # Use the string strip function and place all the caracters we want to strip away to clean up 
    words = [w.strip(".,/:;!@") for w in words]
    # Use the string strip function
    # and place all the caracters we want to strip away
    # Use a set to have unique words
    words = {w.strip(".,/:;!@") for w in words}

    # search for k in keywords, this give you the dictionory key
    # if the key is in the words set, we add 1 to the keywords score

    for k in keywords:
        if k in words:
            keywords[k] += 1
    
    
    # plot a bar graph
  plt.bar(keywords.keys(), keywords.values())
    # Add labels
  plt.xlabel("Language")
  plt.ylabel("# of Mentions")
  plt.show()
    
if __name__ == "__main__":
  main()
  