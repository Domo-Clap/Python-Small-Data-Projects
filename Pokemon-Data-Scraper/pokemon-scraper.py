from selenium import webdriver
from selenium.webdriver.common.by import By

import Data_Transformer

# Site we are scraping data from
SITE_URL = "https://pokemondb.net/pokedex/all"


# Class structure for scraping process
# Makes it easier to call certain functions and pass data
class PokemonScraper:

    # Init function to setup headless chrome options for selenium runtime
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # Sometimes needed for headless mode
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        # Sets up Chrome web driver
        self.driver = webdriver.Chrome(options=chrome_options)

        # Dictionary used to map column names to the data we scrape
        self.structureDict = {0: "Dex Num",
            1: "Pokemon Name",
            2: "Type1",
            3: "Total Stats",
            4: "HP Stat",
            5: "Attack Stat",
            6: "Defense Stat",
            7: "Sp. Attack Stat",
            8: "Sp. Defense Stat",
            9: "Speed Stat"}

        # Holds all the pokemon data after the scrape process
        self.pokemonDict = {}

    # Holds all the scraping data logic
    def get_pokemon(self):

        # Gets the url for where we are scraping the data from
        self.driver.get(SITE_URL)

        # Used for when we populate the pokemonDict. Will act as the key/index value
        pokesum = 0

        try:
            # Gets all the table rows from the website and stores them in the var
            pokedexObjRow = self.driver.find_elements(By.TAG_NAME, "tr")

            # For each row in the list of pokedex entries, we loop
            for row in pokedexObjRow[1:]:

                # Here, we create an inner dictionary that holds the individual table column values for each row.
                # Gets reset each pokedex entry/iteration
                innerDict = {key: None for key in self.structureDict.values()}

                # Gets all the individual table column values for the pokemon
                pokemonInfo = row.find_elements(By.TAG_NAME, "td")

                # Loops over the indexes and table column values for each pokemon
                for index, td in enumerate(pokemonInfo):

                    # If the current index (Loop iteration number) is in the structureDict, we then assign values for the innerDict
                    if index in self.structureDict:

                        key = self.structureDict[index]
                        value = td.text

                        # Lastly, if the value does not have a new line in it, we can then check to see if it is an int value and convert if needed
                        if key in ["Total Stats", "HP Stat", "Attack Stat", "Defense Stat", "Sp. Attack Stat", "Sp. Defense Stat", "Speed Stat"]:
                            value = int(value)

                            # Then we just assign the key-value like normal
                        innerDict[key] = value

                #print(innerDict)

                # Counts the total number of rows for us to be used in  the dict
                pokesum += 1

                self.pokemonDict[pokesum] = innerDict

            # print(pokesum)
            print(self.pokemonDict)

            #for i in range(self.loopVar, 1025):
                #pokedexObjRow = self.driver.find_element(By.XPATH, f"//*[@id=\"pokedex\"]/tbody/tr[{i}]")

                #self.pokemonDict[i] = pokedexObjRow.text

                #print(pokedexObjRow.text)

            #print(self.pokemonDict)

        except Exception as e:
            print(f"Error: {e}")


    # Calls the Data_Transformer class so that we can transform our data into a dataframe
    def TransformData(self):

        # Data_Transformer object to call df transformer function
        controller = Data_Transformer.Data_Transformer()

        finalData = controller.TransformToDF(self.pokemonDict)

        # returns a dataframe to be used when sending our data to the database
        return finalData

    # Just used to stop the webdriver when needed
    def stopDriver(self):
        self.driver.quit()


# Main function that creates our web scraper object and gets the pokemon dict for us
if __name__ == '__main__':

    # Creates our scraper object
    newScraper = PokemonScraper()

    # Scrapes the website for all the data we want
    newScraper.get_pokemon()

    # Stops the web driver
    newScraper.stopDriver()

    # Creates a cleaned up dataframe for our Pokemon data
    finDF = newScraper.TransformData()

    # print(finDF)

    # Data_Transformer object used to call the SQL database functions
    SQL_Controller = Data_Transformer.Data_Transformer()

    # Creates our main table if it does not exist
    SQL_Controller.createMainTable()

    # Inserts the data into the SQL table based on the passed in dataframe
    SQL_Controller.insertData(finDF)

