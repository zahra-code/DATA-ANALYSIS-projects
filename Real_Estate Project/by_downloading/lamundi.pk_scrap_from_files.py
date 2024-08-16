import os
from bs4 import BeautifulSoup
try:
    for file in os.listdir("lamundi_pk_htmls"):
        with open(f"by_downloading/lamundi_pk_htmls/{file}") as f:
            html=f.read()
        soup=BeautifulSoup(html,"lxml")
        if soup.find("h4",attrs={'class':"card-horizontal_cardTitle__dHyrR price_price__oxYSY heading_h4__5Kb_J"})==None:
            price="-"
        else:
            price=soup.find("h4",attrs={'class':"card-horizontal_cardTitle__dHyrR price_price__oxYSY heading_h4__5Kb_J"}).text

        if soup.find("div",attrs={"class":"card-horizontal_cardSubTitle__3FJyc"})==None:
            location="-"
        else:
            location=soup.find("div",attrs={"class":"card-horizontal_cardSubTitle__3FJyc"}).text

        if soup.find("div",attrs={'class':"card-horizontal_cardSpecs__3U-Ym"})==None:
            div_tags="-"
        else:
            div_tags=soup.find("div",attrs={'class':"card-horizontal_cardSpecs__3U-Ym"})

        tag=div_tags.find_all("div")
        area=tag[0].text
        beds=tag[1].text

except Exception as e:
    print(f"ERROR:{e}")
