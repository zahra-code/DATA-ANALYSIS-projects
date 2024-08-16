import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
from config import HOST,DB_PASSWORD,DB_USERNAME
def lamundi_scraper():
    try:
        # creating selenium chrome driver
        service = Service(executable_path="../../chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        #Connecting to the database using python mysql-connector
        connection=mysql.connector.connect(
            host=HOST,
            username=DB_USERNAME,
            password=DB_PASSWORD,
            database="real_estate_database"
        )
        cursor=connection.cursor()
    except Exception as e:
        print(f"ERROR:{e}")

    # list for rent/buy
    query_category={
        "houses-for-sale": "For Sale",
        "houses-to-rent": "For Rent"
    }
    #list for cities we want to get data of
    query_city = {
        1: "Lahore",
        2: "Karachi",
        3: "Islamabad",
        16: "Faisalabad",
        41: "Rawalpindi"
    }
    try:
        driver.implicitly_wait(5)
        #making driver to get data from the url for each city and each category
        for city_id in query_city:
            for category in query_category:
                city_name=query_city[city_id]
                driver.get(f'https://www.lamudi.pk/search/{city_name}/{category}-{city_id}/')
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div[class="card-horizontal_cardHorizontal__OzX3s"]')
                    )
                )
                print(f"\tcity={city_name} ,category={category}")
                elements=driver.find_elements(By.CSS_SELECTOR,'div[class="card-horizontal_cardHorizontal__OzX3s"]')
                for element in elements:
                    #getting the html using selenium
                    html=element.get_attribute("outerHTML")
                    #making soup using beautiful soup
                    soup = BeautifulSoup(html, "lxml")

                    #getting price of property
                    if soup.find("h4", attrs={'class': "card-horizontal_cardTitle__dHyrR price_price__oxYSY heading_h4__5Kb_J"}) == None:
                        price = "-"
                    else:
                        price = soup.find("h4", attrs={
                            'class': "card-horizontal_cardTitle__dHyrR price_price__oxYSY heading_h4__5Kb_J"}).text
                    #getting location of property
                    if soup.find("div", attrs={"class": "card-horizontal_cardSubTitle__3FJyc"}) == None:
                        location = "-"
                    else:
                        location = soup.find("div", attrs={"class": "card-horizontal_cardSubTitle__3FJyc"}).text

                    if soup.find("div", attrs={'class': "card-horizontal_cardSpecs__3U-Ym"}) == None:
                        div_tags = "-"
                    else:
                        div_tags = soup.find("div", attrs={'class': "card-horizontal_cardSpecs__3U-Ym"})

                    tag = div_tags.find_all("div")
                    if len(tag)>1:
                        # getting area of property
                        area = tag[0].text
                        # getting number of bedrooms of property
                        beds = tag[1].text
                    else:
                        # getting area of property
                        area = tag[0].text
                        # getting number of bedrooms of property
                        beds = "-"
                    #storing data into database using mysql python query
                    cursor.execute(
                        "INSERT INTO housing_data (city,location,area,bedrooms,price,property_purpose) VALUES (%s,%s,%s,%s,%s,%s)",
                        (city_name, location, area, beds, price, query_category[category])
                    )
                    connection.commit()
                    print("Data successfully inserted into database")
                time.sleep(2)
    except Exception as e:
        print(f"ERROR:{e}")
    finally:
        driver.close()
        cursor.close()
        connection.close()