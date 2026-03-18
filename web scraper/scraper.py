import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

articles = []

request = requests.get('https://sekurak.pl/?cat=7,3')
soup = BeautifulSoup(request.text, "html.parser")

last = soup.find_all('a', 'last')[0].get('href')
#print(last)

#i= 1
#page = ""
#while page != last:
'''Można scrapować wybraną ilość stron (na każdej po 15 artykułów), ale przy >3 zajmuje zbyt długo. w pliku dane2.json są zescrapowane dane z 10 stron'''
for i in range (1, 2):
    try:
        page = f'https://sekurak.pl/page/{i}/?cat=7%2C3'
        #print(page)
        request_i = requests.get(page)
        soup = BeautifulSoup(request_i.text, "html.parser")
        posts = soup.find_all('article')

        for post in posts:
            link = post.a.get('href')
            title = post.a.get('title')
            #print(f'link: {link}, title: {title}')

            request_post = requests.get(link)
            #print(f'request: {request_post}')

            try:
                driver = webdriver.Chrome()
                driver.get(link)

                meta = driver.find_elements(By.CLASS_NAME, 'meta')
                #print (meta[1].text)
                tags = meta[1].find_elements(By.CSS_SELECTOR, 'a')

                tags_dict = dict()
                for tag in tags:
                    tags_dict[tag.text] = tag.get_attribute('href')
                #print(tags_dict)


                article = {'Title': title, 'Link': link, 'Tags': tags_dict}
                articles.append(article)

                driver.quit()

            except:
                pass

    except:
        pass

    #i+=1

print("ALL:")
print(articles)
json_articles = json.dumps(articles)
print(json_articles)

with open('dane.json', 'w') as f:
    f.write(json_articles)

#odpalenie serwera www
os.system("interface.py")