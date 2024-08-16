from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
from config import HOST,DB_PASSWORD,DB_USERNAME
def zameen_scraper():
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
        "Houses_Property": "For Sale",
        "Rentals_Houses_Property": "For Rent"
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
                driver.get(f"https://www.zameen.com/{category}/{city_name}-{city_id}-1.html")
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'li[role="article"]')
                    )
                )
                print(f"\t city={city_name},purpose={query_category[category]}")
                elements=driver.find_elements(By.CSS_SELECTOR,'li[role="article"]')
                for element in elements:
                    #getting the html using selenium
                    html=element.get_attribute("outerHTML")
                    #making soup using beautiful soup
                    soup = BeautifulSoup(html, "lxml")

                    #getting price of property
                    if soup.find("span", attrs={"aria-label": "Price"}) == None:
                        price = "-"
                    else:
                        price = soup.find("span", attrs={"aria-label": "Price"}).text

                    #getting location of property
                    if soup.find("div", attrs={'aria-label': "Location"}) == None:
                        location = "-"
                    else:
                        location = soup.find("div", attrs={'aria-label': "Location"}).text

                    #getting number of bedrooms of property
                    if soup.find("span", attrs={'aria-label': 'Beds'}) == None:
                        beds = "-"
                    else:
                        beds = soup.find("span", attrs={'aria-label': 'Beds'}).text

                    #getting area of property
                    if soup.find("span", attrs={'aria-label': "Area"}) == None:
                        area = "-"
                    else:
                        area = soup.find("span", attrs={'aria-label': "Area"}).text

                    #storing data into database using mysql python query
                    cursor.execute(
                        "INSERT INTO housing_data (city,location,area,bedrooms,price,property_purpose) VALUES (%s,%s,%s,%s,%s,%s)",
                        (city_name,location, area, beds, price,query_category[category])
                    )
                    connection.commit()
                    print("Data successfully inserted into database")
    except Exception as e:
        print(f"ERROR:{e}")
    finally:
        driver.close()
        cursor.close()
        connection.close()
