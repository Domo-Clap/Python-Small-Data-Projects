########################################################################################################################
########################################################################################################################
########################################################################################################################


# This file has a class that holds the main logic to scrape the website for the raw NBA data.
# We initialize a NBAScrapper object, which then allows us to call our startScrape and stopDriver functions to get the data
# and close the web driver

# After that, this file creates an object from the MoveData file, which allows us to turn the data into a pandas dataframe,
# clean up the data a bit by removing nulls, and move it into a SQL Server database

# Last updated: 9/15/2024 - Dominic Clapper - First Version for scrapping site

# Future Updates: Could possibly add in some more data transformations to make the data appear more clear (Might add
# season column). Also, want to add in functionality to allow for different seasons to be tracked and stored in different
# tables.


########################################################################################################################
########################################################################################################################
########################################################################################################################

# All imports for this file.
# Selenium to scrape website, and MoveData to bring in data moving logic

import MoveData

from selenium import webdriver
from selenium.webdriver.common.by import By

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Website we are scrapping the data from
WEB_URL = "https://www.basketball-reference.com/leagues/NBA_2024_totals.html"

class NBAScrapper:

    # Here, you can set whatever webdriver options you want such as changing the webdriver from Chrome to firefox,
    # or making it run in a headless environment, etc...
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        # I use a chome webdriver here since it is what I learned to use for selenium during my research
        self.driver = webdriver.Chrome(options=chrome_options)

        # This dict can be changed depending on what kind of data you are scrapping
        # All it is really used for is to assign the individual player dicts with key names
        self.statDict = {
            #1: "Rank",
            2: "Player",
            3: "Age",
            4: "Team",
            5: "Position",
            6: "Games Played",
            7: "Games Started",
            8: "Minutes Played",
            9: "Field Goals",
            10: "Field Goals Attempted",
            11: "Field Goal Percentage",
            12: "3 Point Field Goals",
            13: "3 Point Field Goals Attempted",
            14: "3 Point Field Goal Percentage",
            15: "2 Point Field Goals",
            16: "2 Point Field Goals Attempted",
            17: "2 Point Field Goal Percentage",
            18: "Effective Field Goal Percentage",
            19: "Free Throws",
            20: "Free Throws Attempted",
            21: "Free Throw Percentage",
            22: "Offensive Rebounds",
            23: "Defensive Rebounds",
            24: "Total Rebounds",
            25: "Assists",
            26: "Steals",
            27: "Blocks",
            28: "Turnovers",
            29: "Personal_Fouls",
            30: "Total_Points"
        }

        # Final dict that will get sent to the DataMover object to be processed
        self.totStats = {}


    def statScrape(self):

        self.driver.get(WEB_URL)

        try:

            # Get main table
            dataTable = self.driver.find_element(By.XPATH, "//*[@id=\"totals_stats\"]/tbody")

            # Get all the rows in the main table
            dataRows = dataTable.find_elements(By.TAG_NAME, "tr")

            playerSum = 0

            # Loop through all of the rows in the main table
            for row in dataRows:

                indivDict = {}

                #print(row.text)

                i = 2

                # Get all of the td/table data columns in the table row
                spefStats = row.find_elements(By.TAG_NAME, "td")

                # Loop through all of the table data columns in the row
                for td in spefStats:

                    # Assign the key and values for the
                    if i in self.statDict:

                        key = self.statDict[i]
                        value = td.text

                        indivDict[key] = value

                    i += 1

                playerSum += 1

                # Add the individual player data to the larger, overarching dict
                self.totStats[playerSum] = indivDict

            #print(self.totStats)

            return self.totStats


        except Exception as e:
            print(f"Error: {e}")


    # All this does is let us stop the webdriver
    def StopDriver(self):
        self.driver.quit()


########################################################################################################################
########################################################################################################################
########################################################################################################################

# Simple enough. This is where the code starts, and we create our class objects to call the needed functions
if __name__ == '__main__':
    statScraper = NBAScrapper()

    nbaDict = statScraper.statScrape()

    statScraper.StopDriver()

    dataPipeline = MoveData.DataMover()

    nbaDF = dataPipeline.TransformDataToDF(nbaDict)

    #print(nbaDF)

    dataPipeline.createMainTable()

    dataPipeline.insertNBAData(nbaDF)
