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
    "houses-for-sale": "For Sale",
    "houses-to-rent": "For Rent"
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
    # for city_id in query_city:
    #     for category in query_category:
    category="houses-for-sale"
    city_id=3
    city_name=query_city[city_id]
    driver.get(f'https://www.lamudi.pk/search/{city_name}/{category}-{city_id}/')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[class="card-horizontal_cardHorizontal__OzX3s"]')
        )
    )
    elements=driver.find_elements(By.CSS_SELECTOR,'div[class="card-horizontal_cardHorizontal__OzX3s"]')
    for element in elements:
        html=element.get_attribute("outerHTML")
        with open(f"lamundi_pk_htmls/{city_name}-{file}","w",encoding="utf-8") as f:
            f.write(html)
        file+=1
    time.sleep(2)
    print(f"{file} writing done for city={city_name} ,category={category}")
except Exception as e:
    print(f"ERROR:{e}")
finally:
    driver.close()
