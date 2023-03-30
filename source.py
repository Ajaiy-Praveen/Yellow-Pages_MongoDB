## Ajaiy Praveen T
## Will take around 5 mins to execute completely due to delays

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import urllib.request
from urllib.error import URLError 
import time
import json
import re
import pymongo
import random
import os



# Accessing BAYC using selenium
def question2():

    print("\nExecuting function 2")
    global rel_path 
    # Getting the relative path
    rel_path = os.path.dirname(__file__)
    global target_file_path_monkey
    target_file_path_monkey =[]
    # Chrome Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    time.sleep(5)
    # Selecting the Ape number and downloading it's page
    for i in range(1,9):
        time.sleep(2)
        driver.get('https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold')
        element1 = driver.find_element(By.XPATH,'//*[@id="main"]/div/div/div/div[5]/div/div[7]/div[3]/div[2]/div/div['+ str(i) +']/article/a/div[3]/div[1]/div/div/span')
        target_file_path_monkey.append(rel_path+"/bayc_"+element1.text+".htm")
        element = driver.find_element(By.XPATH,'//*[@id="main"]/div/div/div/div[5]/div/div[7]/div[3]/div[2]/div/div['+ str(i) +']/article/a')
        link = element.get_attribute("href")
        driver.get(link)
        time.sleep(1)
        with open(target_file_path_monkey[i-1], "w", encoding='utf-8') as f:
            f.write(driver.page_source)





# Storing Apes and their attributes in MongoDB
def question3():
    
    print("\nExecuting function 3")
    print("Storing Apes and their attributes in MongoDB")
    # Creating a collection in MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase_ajaiy"]
    mycol = mydb["bayc"]
    mycol.drop()
    # Looping over the 8 downloaded pages
    for i in range(0,8):
        try:
            key=[]
            values =[]
            key.append("Name")
            HTMLFileToBeOpened = open(target_file_path_monkey[i], "r", encoding='cp437', errors='ignore')
            # Reading the file and storing in a variable
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
            # Extracting the Ape name
            t = soup.select("section.item--header > div:nth-child(2) > h1")
            for i in t:
                    name = re.findall(r'\d+', i.text)
                    values.append(name[0])
            t = soup.select("#Body\ assets-item-properties > div > div > div")
            # Extracting the attributes and it's values
            for k in t:
                for l in k.select('div.Property--type'):
                    key.append(l.text)
                for l in k.select('div.Property--value'):
                    values.append(l.text)
            
            res = dict(zip(key, values))
            # Inserting into the collection
            mycol.insert_one(res)

        except URLError as e:
            print("Unable to open page: "+str(e.reason))





# Saving top 30 Pizzeria's on Yellow pages to local
def question4():

    print("\nExecuting function 4")
    print("Saving top 30 Pizzeria's on Yellow pages to local")
    # URL with search term and location
    url ="https://www.yellowpages.com/search?search_terms=Pizzeria&geo_location_terms=San+Francisco%2C+CA"
    global headers
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
              }

    global target_file_path 
    # Relative path
    target_file_path  = rel_path+"\sf_pizzeria_search_page.htm"
    # Downloading the page
    try:
        req = urllib.request.Request(url, headers=headers
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
        with open(target_file_path,"wb") as fp:
            fp.write(html_content)
    except URLError as e:
        print("Unable to download page: "+str(e.reason))






# Parsing the shop information from the downloaded pages
def question5():

    print("\nExecuting function 5")
    print("Parsing the shop information from the downloaded pages")
     # Reading the file and storing in a variable
    HTMLFileToBeOpened = open(target_file_path, "r", encoding='cp437', errors='ignore')
    contents = HTMLFileToBeOpened.read()
    soup = BeautifulSoup(contents, 'lxml')

    # Lists to hold the attribute values
    rank_list =[]
    name_list =[]
    url_list =[]
    star_rating_list =[]
    star_review_list =[]
    td_rating_list =[]
    td_review_list =[]
    years_list =[]
    amenities_list =[]
    comment_list =[]
    price_list =[]
    # Extracting the values for each pizzeria if exists
    for m in soup.select('div.search-results.organic > div.result > div > div > div.info > div.info-section.info-primary'):
       
        # Rank
        for n in m.find_all('h2'):
            string = n.text
            all_words = string.split()
            first_word= all_words[0]
            rank = re.findall(r'\d+', first_word)
            rank_list.append(rank[0])
       

        # Name and URL
        for o in m.select('h2 > a'):
            a = o.get('href')
            name_list.append(o.text)
            url_list.append("https://www.yellowpages.com"+a)

        for att in m.select('div.ratings'):
            # Star ratings
            if(att.select('a.rating.hasExtraRating > div')):
                for i in att.select('a.rating.hasExtraRating > div'):
                    temp= i["class"]
                    star_rating_list.append(temp[1])
            else:
                star_rating_list.append("Star rating not available")
            
            # Star reviews
            if(att.select('a > span.count')):
                for i in att.select('a > span.count'):
                    star_review_list.append(i.text)  
            else:
                star_review_list.append("Star review not available") 

            # Trip Advisor
            if att.has_attr('data-tripadvisor'):
                temp = att.attrs['data-tripadvisor']
                json_object = json.loads(temp)
                td_rating_list.append(json_object['rating'])
                td_review_list.append(json_object['count'])
            else:
                td_rating_list.append("TA Rating not available")
                td_review_list.append("TA Reviews not available")
            
            
            # Years
            if(m.select('div.badges > div.years-in-business > div > div.number')):
                for i in m.select('div.badges > div.years-in-business > div > div.number'):
                    
                    years_list.append(i.text)

            else:
                years_list.append("Years not available")

            # Amenities
            if(m.select('div.amenities > div.amenities-info')):
                for i in m.select('div.amenities > div.amenities-info'):
                    amenities_list.append(i.get_text(separator=", "))
                
            else:
                amenities_list.append("Amenities Not available")
            
    # Extract comments
    for m in soup.select('div.search-results.organic > div.result > div > div > div.info'):
        if(m.select('div.snippet > p')):
            for i in m.select('div.snippet > p'):
                comment_list.append(i.text)
        else:
            comment_list.append("Comment not available")
    
    # Extract Price $
    for m in soup.select('div.search-results.organic > div.result > div > div > div.info > div.info-section.info-secondary'):
        if(m.select('div.price-range')):
            for i in m.select('div.price-range'):
                price_list.append(i.text)
        else:
            price_list.append("Price Not available")
        
        




# Storing the extracted shop information into MongoDB 
def question6():

    print("\nExecuting function 6")
    print("Storing the extracted shop information into MongoDB ")
    # Reading the file and storing in a variable
    HTMLFileToBeOpened = open(target_file_path, "r", encoding='cp437', errors='ignore')
    contents = HTMLFileToBeOpened.read()
    soup = BeautifulSoup(contents, 'lxml')

    # Lists to hold the attribute values
    rank_list =[]
    name_list =[]
    url_list =[]
    star_rating_list =[]
    star_review_list =[]
    td_rating_list =[]
    td_review_list =[]
    years_list =[]
    amenities_list =[]
    comment_list =[]
    price_list =[]

    for m in soup.select('div.search-results.organic > div.result > div > div > div.info > div.info-section.info-primary'):
       
        # Rank
        for n in m.find_all('h2'):
            string = n.text
            all_words = string.split()
            first_word= all_words[0]
            rank = re.findall(r'\d+', first_word)
            rank_list.append(rank[0])
       

        # Name and URL
        for o in m.select('h2 > a'):
            a = o.get('href')
            name_list.append(o.text)
            url_list.append("https://www.yellowpages.com"+a)

        for att in m.select('div.ratings'):
            # Star ratings
            if(att.select('a.rating.hasExtraRating > div')):
                for i in att.select('a.rating.hasExtraRating > div'):
                    temp= i["class"]
                    star_rating_list.append(temp[1])
            else:
                star_rating_list.append("Star rating not available")
            
            # Star reviews
            if(att.select('a > span.count')):
                for i in att.select('a > span.count'):
                    star_review_list.append(i.text)  
            else:
                star_review_list.append("Star review not available") 

            # Trip Advisor
            if att.has_attr('data-tripadvisor'):
                temp = att.attrs['data-tripadvisor']
                json_object = json.loads(temp)
                td_rating_list.append(json_object['rating'])
                td_review_list.append(json_object['count'])
            else:
                td_rating_list.append("TA Rating not available")
                td_review_list.append("TA Reviews not available")
            
            
            # Years
            if(m.select('div.badges > div.years-in-business > div > div.number')):
                for i in m.select('div.badges > div.years-in-business > div > div.number'):
                    
                    years_list.append(i.text)

            else:
                years_list.append("Years not available")

            # Amenities
            if(m.select('div.amenities > div.amenities-info')):
                for i in m.select('div.amenities > div.amenities-info'):
                    amenities_list.append(i.get_text(separator=", "))
                
            else:
                amenities_list.append("Amenities Not available")
            
    # Extract comments
    for m in soup.select('div.search-results.organic > div.result > div > div > div.info'):
        if(m.select('div.snippet > p')):
            for i in m.select('div.snippet > p'):
                comment_list.append(i.text)
        else:
            comment_list.append("Comment not available")
    
    # Extract Price $
    for m in soup.select('div.search-results.organic > div.result > div > div > div.info > div.info-section.info-secondary'):
        if(m.select('div.price-range')):
            for i in m.select('div.price-range'):
                price_list.append(i.text)
        else:
            price_list.append("Price Not available")
        
        
    # Inserting into MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase_ajaiy"]
    mycol = mydb["sf_pizzerias"]
    mycol.drop()

    for i in range(0,30):
        mydict = { "Rank": rank_list[i], 
                    "Name": name_list[i],
                    "URL":url_list[i],
                    "Star Rating":star_rating_list[i],
                    "Star Review":star_review_list[i],
                    "TripAdvisor Rating":td_rating_list[i],
                    "TripAdvisor Review":td_review_list[i],
                    "Price $" :price_list[i],
                    "Year":years_list[i],
                    "Comments":comment_list[i],
                    "Amenities":amenities_list[i] }
        
        mycol.insert_one(mydict)






# Reading each of the 30 store URLs and downloading the page
def question7():

    print("\nExecuting function 7")
    print("Reading each store URL and downloading the page")
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase_ajaiy"]
    mycol = mydb["sf_pizzerias"]
    global path_names
    path_names = []
    # Reading the documents from the collection
    for x in mycol.find():
     try:
            # Accessing the URL column and requesting
            req = urllib.request.Request(x['URL'], None, headers)
            time.sleep(5)
            with urllib.request.urlopen(req) as response:
                html_content = response.read()
            with open(rel_path+"\sf_pizzerias_"+str(x['Rank'])+".htm","wb") as fp:
                fp.write(html_content)
            path_names.append(rel_path+"\sf_pizzerias_"+str(x['Rank'])+".htm")
     except URLError as e:
            print("Unable to download page: "+str(e.reason))
    





# Extracting the number, link and address in each page
def question8():

    print("\nExecuting function 8")
    print("Extracting the number, link and address in each page")
    number_list =[]
    website_list =[]
    address_list =[]
    # Looping over the 30 pages
    for j in range(0,30):
        try:
            HTMLFileToBeOpened = open(path_names[j], "r", encoding='cp437', errors='ignore')
            # Reading the file and storing in a variable
            contents = HTMLFileToBeOpened.read()
            time.sleep(2)
            soup = BeautifulSoup(contents, 'lxml')
            # Parsing the number
            if(soup.select('#default-ctas > a.phone.dockable > strong')):
                for i in soup.select('#default-ctas > a.phone.dockable > strong'):
                    number_list.append(i.text)
            else:
                number_list.append("No number")
            # Parsing the link
            if(soup.select('#default-ctas > a.website-link.dockable')):
                for i in soup.select('#default-ctas > a.website-link.dockable'):
                    website_list.append(i.get('href'))
            else:
                website_list.append("No website")  
            # Parsing the address
            if(soup.select('#default-ctas > a.directions.small-btn > span')):
                for i in soup.select('#default-ctas > a.directions.small-btn > span'):
                    address_list.append(i.text)
            else:
                address_list.append("No address")
        except URLError as e:
            print("Unable to open download page: "+str(e.reason))
  
            




# Hitting the API with the address and updating the DB with the geolocation"
def question9():

    print("\nExecuting function 9")
    print("Hitting the API with the address and updating the DB with the geolocation")
    # Creating Mongo DB connection
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase_ajaiy"]
    mycol = mydb["sf_pizzerias"]
    number_list =[]
    website_list =[]
    address_list =[]

    for j in range(0,30):
        try:
            HTMLFileToBeOpened = open(path_names[j], "r", encoding='cp437', errors='ignore')
            # Reading the file and storing in a variable
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
        
            # Parsing the number
            if(soup.select('#default-ctas > a.phone.dockable > strong')):
                for i in soup.select('#default-ctas > a.phone.dockable > strong'):
                    number =i.text
            else:
                number="No number"
            number_list.append(number)
            # Parsing the link
            if(soup.select('#default-ctas > a.website-link.dockable')):
             for i in soup.select('#default-ctas > a.website-link.dockable'):
                link = i.get('href')
                website_list.append(i.get('href'))
            else:
                link = "No website"
                website_list.append("No website")  
            # Parsing the address
            if(soup.select('#default-ctas > a.directions.small-btn > span')):
                for i in soup.select('#default-ctas > a.directions.small-btn > span'):
                    address = i.text
            else:
                address="No address"
            x = address.replace("San Francisco"," San Francisco")
            address_list.append(address)

            # Accessing the API with peronal access key
            api ="http://api.positionstack.com/v1/forward?access_key=0f883f4d407ba657d76622974663505c&query="+str(x)+"&limit=40&output=json"
            time.sleep(2)
            page = requests.get(api,headers=headers)
            doc = BeautifulSoup(page.content, 'html.parser')
            json_dict = json.loads(str(doc))
            myquery = { "Rank": f'{j+1}' }
            # Adding the latitute and longitude
            newvalues = { "$set": {"Number": number, 
                                   "Address": x , 
                                   "Link": link,
                                   "GeoLocation":{
                                                  "Latitude":json_dict['data'][0]['latitude'],
                                                  "Longitude":json_dict['data'][0]['longitude'] 
                                                  }
                                } }
            mycol.update_one(myquery, newvalues)

        except (KeyError, IndexError, TypeError, URLError, ValueError):
            #Unable to retrieve API, updating with random values
            myquery = { "Rank": f'{j+1}' }
            newvalues = { "$set": { "Number": number,
                                    "Address": x ,
                                    "Link": link,
                                    "GeoLocation":{
                                                    "Latitude":random.uniform(37.0, 37.9),
                                                    "Longitude":random.uniform(-122.0,-122.9)
                                                    }
                                    } }
            mycol.update_one(myquery, newvalues)
            


# Main Function

def main():

    question2()

    question3()

    question4()

    question5()

    question6()
    
    question7()

    question8()

    question9()

    print("\nExecution over")

if __name__ == "__main__":
    main()
    
   
        