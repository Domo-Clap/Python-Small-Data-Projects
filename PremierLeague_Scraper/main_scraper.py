import pandas


from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

class Stats_Scraper:

    def __init__(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # Sometimes needed for headless mode
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        # Web Driver used to connect to our website
        self.driver = webdriver.Chrome(options=chrome_options)

        self.statStructureDict = {0: "Rank",
                              1: "Player",
                              2: "Club",
                              3: "Nationality",
                              4: "Stat"}


    def stat_scrape(self, url):

        WEB_URL = url

        self.driver.get(WEB_URL)

        all_stats = {}
        playerSum = 0

        try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "tr"))
                )

                goalsTable = self.driver.find_elements(By.TAG_NAME, "tr")

                for row in goalsTable[1:]:

                    indivDict = {}

                    statInfo = row.find_elements(By.TAG_NAME, "td")

                    i = 0

                    for td in statInfo:

                        # print(td.text)

                        if i in self.statStructureDict:

                            key = self.statStructureDict[i]
                            value = td.text

                            indivDict[key] = value

                        i += 1

                    playerSum += 1

                    all_stats[playerSum] = indivDict

                print(all_stats)

                return all_stats

        except Exception as e:
            print(f"Error: {e}")
            return

    def stopDriver(self):
        self.driver.quit()

