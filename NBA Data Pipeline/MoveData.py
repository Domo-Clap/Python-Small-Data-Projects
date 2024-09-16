########################################################################################################################
########################################################################################################################
########################################################################################################################


# This file has a class that holds the main logic that operates our data pipeline.
# Basically, we take the data that was scraped, and use the class in this file, DataMover, to transform the data.
# Then we move the data into the database table we create by calling the createMainTable function.

# For this class, you will need to get your own info for a SQL Server database
# I used a local database version of SQL Server for my work, but the data related to my db will be omitted.
# Again, you will need to supply your own database for this if you want to run the script
# Also, there are other dbs you can use, but you would need to edit the data types and other info to create a data pipeline

# Last updated: 9/15/2024 - Dominic Clapper - First Version for cleaning and moving data

# Future Updates: Possibly add functions that break the dataframe down by team and store them in separate tables.


########################################################################################################################
########################################################################################################################
########################################################################################################################

# All imports for this file.
# Pandas to handle the data transformation process, and pyodbc to move the data to the SQL Server DB

import pandas as pd
import pyodbc

########################################################################################################################
########################################################################################################################
########################################################################################################################

class DataMover:

    def __init__(self):

        # Not used for the code - Needed it to prevent error in pycharm
        self.dubmint = 0


    # Loads the data from the passed in dict into a pandas df
    # Makes it easier to move things into the database
    def TransformDataToDF(self, playerDict):

        data = []

        for i, player in playerDict.items():
            playername = player.get("Player", None)
            age = player.get("Age", None)
            teamName = player.get("Team", None)
            position = player.get("Position", None)
            gamesPlayed = player.get("Games Played", None)
            gamesStarted = player.get("Games Started", None)
            minsPlayed = player.get("Minutes Played", None)
            FGs = player.get("Field Goals", None)
            FGAs = player.get("Field Goals Attempted", None)
            FGPercent = player.get("Field Goal Percentage", None)
            threePointsMade = player.get("3 Point Field Goals", None)
            threePointsAttemp = player.get("3 Point Field Goals Attempted", None)
            threePointsPercent = player.get("3 Point Field Goal Percentage", None)
            twoPointsMade = player.get("2 Point Field Goals", None)
            twoPointsAttemp = player.get("2 Point Field Goals Attempted", None)
            twoPointsPercent = player.get("2 Point Field Goal Percentage", None)
            effectiveFG = player.get("Effective Field Goal Percentage", None)
            FTs = player.get("Free Throws", None)
            FTAs = player.get("Free Throws Attempted", None)
            FTPercent = player.get("Free Throw Percentage", None)
            OR = player.get("Offensive Rebounds", None)
            DR = player.get("Defensive Rebounds", None)
            TR = player.get("Total Rebounds", None)
            assists = player.get("Assists", None)
            steals = player.get("Steals", None)
            blocks = player.get("Blocks", None)
            TOs = player.get("Turnovers", None)
            personal_fouls = player.get("Personal_Fouls", None)
            points = player.get("Total_Points", None)

            data.append([playername, age, teamName, position, gamesPlayed, gamesStarted, minsPlayed, FGs, FGAs, FGPercent,
                         threePointsMade, threePointsAttemp, threePointsPercent, twoPointsMade, twoPointsAttemp, twoPointsPercent,
                         effectiveFG, FTs, FTAs, FTPercent, OR, DR, TR, assists, steals, blocks, TOs, personal_fouls, points])

        df = pd.DataFrame(data, columns=["Player Name", "Age", "Team Name", "Position", "Games Played", "Games Started",
                                             "Minutes Played", "Field Goals", "Field Goals Attempted", "Field Goal Percentage",
                                             "3 Point Field Goals", "3 Point Field Goals Attempted", "3 Point Field Goal Percentage",
                                             "2 Point Field Goals", "2 Point Field Goals Attempted", "2 Point Field Goal Percentage",
                                             "Effective Field Goal Percentage", "Free Throws", "Free Throws Attempted", "Free Throw Percentage",
                                             "Offensive Rebounds", "Defensive Rebounds", "Total Rebounds", "Assists",
                                             "Steals", "Blocks", "Turnovers", "Personal_Fouls", "Total_Points"])

        # Needed to drop the last row of the df since it was just league averages
        df = df.drop(df.index[-1])

        # Also made sure to clean any null values
        df = df.dropna()

        return df


    # Just creates our connection to the database and attempts to make a new table if it doesn't exist
    # We also close the db connection
    def createMainTable(self):

        tableName = "NBAStats_2023_2024"

        SERVER = "SERVERNAME"
        DATABASE = "DBNAME"
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        conn = pyodbc.connect(connectionString)

        createTableQRY = f"""IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tableName}')
            BEGIN
                EXEC('CREATE TABLE {tableName} (
                    Player_ID int IDENTITY(1,1) PRIMARY KEY,
                    Player_Name varchar(75),
                    Age INT,
                    Team_Name varchar(10),
                    Position varchar(10),
                    Games_Played INT,
                    Games_Started INT,
                    Minutes_Played INT,
                    Field_Goals INT,
                    Field_Goals_Attempted INT,
                    Field_Goal_Percentage varchar(10),
                    Three_Point_Field_Goals INT,
                    Three_Point_Field_Goals_Attempted INT,
                    Three_Point_Field_Goal_Percentage varchar(10),
                    Two_Point_Field_Goals INT,
                    Two_Point_Field_Goals_Attempted INT,
                    Two_Point_Field_Goal_Percentage varchar(10),
                    Effective_Field_Goal_Percentage varchar(10),
                    Free_Throws INT,
                    Free_Throws_Attempted INT,
                    Free_Throw_Percentage varchar(10),
                    Offensive_Rebounds INT,
                    Defensive_Rebounds INT,
                    Total_Rebounds INT,
                    Assists INT,
                    Steals INT,
                    Blocks INT,
                    Turnovers INT,
                    Personal_Fouls INT,
                    Total_Points INT,
                );')
            END
        """

        cursor = conn.cursor()

        cursor.execute(createTableQRY)

        conn.commit()

        conn.close()


    # Opens db connection and inserts the data from the df.
    # We close the df after everything is committed.
    def insertNBAData(self, statsDF):
        tableName = "NBAStats_2023_2024"

        SERVER = "SERVERNAME"
        DATABASE = "DBNAME"
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        conn = pyodbc.connect(connectionString)

        cursor = conn.cursor()

        for _, row in statsDF.iloc[:-1].iterrows():

            cursor.execute(f"""INSERT INTO {tableName} (
                Player_Name,
                Age,
                Team_Name,
                Position,
                Games_Played,
                Games_Started,
                Minutes_Played,
                Field_Goals,
                Field_Goals_Attempted,
                Field_Goal_Percentage,
                Three_Point_Field_Goals,
                Three_Point_Field_Goals_Attempted,
                Three_Point_Field_Goal_Percentage,
                Two_Point_Field_Goals,
                Two_Point_Field_Goals_Attempted,
                Two_Point_Field_Goal_Percentage,
                Effective_Field_Goal_Percentage,
                Free_Throws,
                Free_Throws_Attempted,
                Free_Throw_Percentage,
                Offensive_Rebounds,
                Defensive_Rebounds,
                Total_Rebounds,
                Assists,
                Steals,
                Blocks,
                Turnovers,
                Personal_Fouls,
                Total_Points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (
                                row["Player Name"],
                                row["Age"],
                                row["Team Name"],
                                row["Position"],
                                row["Games Played"],
                                row["Games Started"],
                                row["Minutes Played"],
                                row["Field Goals"],
                                row["Field Goals Attempted"],
                                row["Field Goal Percentage"],
                                row["3 Point Field Goals"],
                                row["3 Point Field Goals Attempted"],
                                row["3 Point Field Goal Percentage"],
                                row["2 Point Field Goals"],
                                row["2 Point Field Goals Attempted"],
                                row["2 Point Field Goal Percentage"],
                                row["Effective Field Goal Percentage"],
                                row["Free Throws"],
                                row["Free Throws Attempted"],
                                row["Free Throw Percentage"],
                                row["Offensive Rebounds"],
                                row["Defensive Rebounds"],
                                row["Total Rebounds"],
                                row["Assists"],
                                row["Steals"],
                                row["Blocks"],
                                row["Turnovers"],
                                row["Personal_Fouls"],
                                row["Total_Points"],
                           ))

        conn.commit()

        conn.close()
