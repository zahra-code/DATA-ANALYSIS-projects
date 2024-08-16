import os
from bs4 import BeautifulSoup
import mysql.connector
from config import HOST,DB_PASSWORD,DB_USERNAME
try:
    connection=mysql.connector.connect(
        host=HOST,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        database="real_estate_database"
    )
    cursor=connection.cursor()
except Exception as e:
    print(f"ERROR:{e}")
try:
    for file in os.listdir("zameen_com_htmls"):
        with open(f"by_downloading/zameen_com_htmls/{file}") as f:
            html=f.read()
        soup=BeautifulSoup(html,"lxml")

        if soup.find("span",attrs={"aria-label":"Price"})==None:
            price="-"
        else:
            price=soup.find("span",attrs={"aria-label":"Price"}).text

        if soup.find("div",attrs={'aria-label':"Location"})==None:
            location="-"
        else:
            location=soup.find("div",attrs={'aria-label':"Location"}).text

        if soup.find("span",attrs={'aria-label':'Beds'})==None:
            beds="-"
        else:
            beds=soup.find("span",attrs={'aria-label':'Beds'}).text

        if soup.find("span",attrs={'aria-label':"Area"})==None:
            area="-"
        else:
            area=soup.find("span",attrs={'aria-label':"Area"}).text
        cursor.execute(
            "INSERT INTO housing_data (location,area,bedrooms,price) VALUES (%s,%s,%s,%s)",(location,area,beds,price)
        )
        connection.commit()
        print("Data successfully inserted into database")
except Exception as e:
    print(f"ERROR:{e}")
finally:
    cursor.close()
    connection.close()
