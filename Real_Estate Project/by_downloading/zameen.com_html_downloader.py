#Homes for buy ---Rentals for rent
#1 for lahore--2 for Karachi--3 for Islamabad--16 for Faislabad--41 for Rawalpindi
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service=Service(executable_path="../../chromedriver.exe")
driver=webdriver.Chrome(service=service)
# list for rent/buy
query_category={
    "Houses_Property": "For Sale",
    "Rentals_Houses_Property": "For Rent"
}
query_city = {
    1: "Lahore",
    2: "Karachi",
    3: "Islamabad",
    16: "Faisalabad",
    41: "Rawalpindi"
}
file=0
try:
    driver.implicitly_wait(5)
    for city_id in query_city:
        for category in query_category:
            # category="Homes"
            # city=3
            city_name=query_city[city_id]
            driver.get(f"https://www.zameen.com/{category}/{city_name}-{city_id}-1.html")
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'li[role="article"]')
                )
            )
            elements=driver.find_elements(By.CSS_SELECTOR,'li[role="article"]')
            for element in elements:
                html=element.get_attribute("outerHTML")
                with open(f"zameen_com_htmls/{city_name}-{file}","w",encoding="utf-8") as f:
                    f.write(html)
                file+=1
            time.sleep(2)
            print(f"{file} writing done for city={city_name} ,category={category}")
except Exception as e:
    print(f"ERROR:{e}")
finally:
    driver.close()
