import requests 
from bs4 import BeautifulSoup 
import pandas as pd
from time import sleep

search_query = 'BAGS'.replace('','+')
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'.format(search_query)
items = []
for i in range(1,11):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content,'html.parser')

    results = soup.find_all('div',{'class':'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
    
    for result in results:

        product_name = result.find('span',class_="a-size-medium a-color-base a-text-normal").text
        
        try:
            rating = result.find('i',class_="a-icon a-icon-star-small a-star-small-4 aok-align-bottom").text
            review = result.find('span',class_="a-size-base s-underline-text").text
        except AttributeError:
            continue
        
        try:
            price = result.find('span',class_="a-price-whole").text
            product_url = 'https://amazon.com'+result.h2.a['href']
            items.append([product_url,product_name,rating,review,price])
        except AttributeError:
            continue
    sleep(0.5)
df = pd.DataFrame(items,columns=['product_url','product_name','rating','review','price'])
df.to_csv('{0}.csv'.format(search_query),index = False)
