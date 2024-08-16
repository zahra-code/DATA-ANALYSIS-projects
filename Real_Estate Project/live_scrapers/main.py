import time
from zameen_com_scraper import zameen_scraper
from lamundi_pk_scraper import lamundi_scraper
if __name__ == "__main__":
    zameen_scraper()
    lamundi_scraper()
    #scrap after 1 day
    time.sleep(24*60*60)