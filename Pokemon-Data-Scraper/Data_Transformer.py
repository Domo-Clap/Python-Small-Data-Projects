import pandas as pd
import pyodbc


# Class structure used to hold logic for transforming data and pushing it into a db
class Data_Transformer:
    def __init__(self):

        #Nothing to see here
        self.dumbInt = 0

    # Function that takes in our raw data dictionary and transforms it into a dataframe in the way we want it
    def TransformToDF(self, pokemonDict):

        data = []

        # Loops over the length of our dictionary, so every Pokemon
        for index, d in pokemonDict.items():

            dexNum = d.get("Dex Num", None)
            pokemonName = d.get("Pokemon Name", None)
            Type1 = d.get("Type1", None)
            Type2 = None
            totStats = d.get("Total Stats", None)
            hpStat = d.get("HP Stat", None)
            attStat = d.get("Attack Stat", None)
            defStat = d.get("Defense Stat", None)
            spAttStat = d.get("Sp. Attack Stat", None)
            spDefStat = d.get("Sp. Defense Stat", None)
            spdStat = d.get("Speed Stat", None)

            # Sometimes a Pokemon has 2 types, so here we check to see if one does, and split it up accordingly
            # The data we scraped has Pokemon with 2 types separated like so: 'POISON\nGRASS'
            if Type1 and '\n' in Type1:

                types = Type1.split('\n')
                Type1 = types[0]
                Type2 = types[1]

            else:
                Type1 = Type1

            data.append([dexNum, pokemonName, Type1, Type2, totStats, hpStat, attStat, defStat, spAttStat, spDefStat, spdStat])

        # Creates our dataframe to be used in database functions
        df = pd.DataFrame(data, columns=["Pokedex Number", "Pokemon Name", "Type_1", "Type_2", "Total Stats", "HP Stat", "Attack Stat",
                                         "Defense Stat", "Sp. Attack Stat", "Sp. Defense Stat", "Speed Stat"])

        return df

    # SQL function that connects to our MSSQL db and creates the needed table for our data
    def createMainTable(self):

        tableName = "AllPokemon"

        SERVER = "SERVERNAME"
        DATABASE = "DB NAME"
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        conn = pyodbc.connect(connectionString)

        createQuery = f"""IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tableName}')
            BEGIN
                EXEC('CREATE TABLE {tableName} (
                    Pokedex_Number varchar(5),
                    Pokemon_Name varchar(50),
                    Type_1 varchar(15),
                    Type_2 varchar(15),
                    Total_Stats INT,
                    HP INT,
                    Attack INT,
                    Defense INT,
                    Special_Attack INT,
                    Special_Defense INT,
                    Speed INT
                );')
            END"""

        cursor = conn.cursor()

        cursor.execute(createQuery)

        conn.commit()

        conn.close()

    # SQL function that connects to our MSSQL db again and inserts the data into the created table
    def insertData(self, pokemonDF):

        tableName = "AllPokemon"

        SERVER = "SERVERNAME"
        DATABASE = "DB NAME"
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        conn = pyodbc.connect(connectionString)

        cursor = conn.cursor()

        for _, row in pokemonDF.iterrows():
            cursor.execute(f"""Insert into {tableName} (
                Pokedex_Number,
                Pokemon_Name,
                Type_1,
                Type_2,
                Total_Stats,
                HP,
                Attack,
                Defense,
                Special_Attack,
                Special_Defense,
                Speed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                        row["Pokedex Number"],
                        row["Pokemon Name"],
                        row["Type_1"],
                        row["Type_2"],
                        row["Total Stats"],
                        row["HP Stat"],
                        row["Attack Stat"],
                        row["Defense Stat"],
                        row["Sp. Attack Stat"],
                        row["Sp. Defense Stat"],
                        row["Speed Stat"],
                ))

        conn.commit()

        conn.close()
