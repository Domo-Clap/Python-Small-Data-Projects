import pandas


from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time


WEB_URL = "https://fbref.com/en/comps/9/passing/Premier-League-Stats"

class secondSiteScraper:


    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # Sometimes needed for headless mode
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Web Driver used to connect to our website
        self.driver = webdriver.Chrome(options=chrome_options)

        self.statStructureDict = {0: "Rank",
                                  1: "Player Name",
                                  2: "Nationality",
                                  3: "Position",
                                  4: "Club",
                                  5: "Age",
                                  6: "Year Born",
                                  7: "Full Games Played",
                                  8: "Passes Completed",
                                  9: "Passes Attempted",
                                  10: "Pass Completion Percentage",
                                  11: "Total Passing Distance (yards)",
                                  12: "Progressive Passing Distance (yards)",
                                  13: "Short Passes Completed",
                                  14: "Short Passes Attempted",
                                  15: "Short Pass Completion Percentage",
                                  16: "Medium Passes Completed",
                                  17: "Medium Passes Attempted",
                                  18: "Medium Pass Completion Percentage",
                                  19: "Long Passes Completed",
                                  20: "Long Passes Attempted",
                                  21: "Long Pass Completion Percentage"}

    def getPlayerStats(self):

        all_stats = {}
        playerSum = 0

        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )

        STATS_TABLE = self.driver.find_element(By.ID, "stats_passing")

        table_rows = STATS_TABLE.find_elements(By.TAG_NAME, "tr")



        for row in table_rows[1:]:
            indivDict = {}

            i = 0

            statInfo = row.find_elements(By.TAG_NAME, "td")

            for td in statInfo:

                if i in self.statStructureDict:

                    key = self.statStructureDict[i]
                    value = td.text

                    indivDict[key] = value

                i += 1

                playerSum += 1

                all_stats[playerSum] = indivDict

            print(all_stats)







    def stopDriver(self):
        self.driver.quit()