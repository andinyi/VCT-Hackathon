import pymysql
import csv

class mysqlConnect():

    def __init__(self, user, password):
        self.host = 'database-1.cbq6wokaea8i.us-east-1.rds.amazonaws.com'
        self.user = user
        self.password = password
        self.database = 'VCT-Data'
        self.connection = None
        self.cursor = None

    def connectToDB(self):
        try:
            connect = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                local_infile=True
            )
            self.connect = connect
            self.cursor = connect.cursor()
        except Exception as e:
            print('Some exception occurred during connection. Please check if the user and password is correct and if the server is online.')
    
    def connectCheck(self):
        if(self.cursor == None):
            print('Your connection has yet to be made. Please connect using connectToDB before attempting to run methods.')
            return False
        return True

    def createAndLoadTables(self, table_name, file_name): #generic script to create necessary tables
        self.connectCheck()

        if(table_name == 'Players'):
            #Creates Table
            self.cursor.execute(f'DROP TABLE IF EXISTS `{table_name}`')
            query = f'''
                    CREATE  TABLE `{table_name}` (
                    `Player` text,
                    `Team` text,
                    `Games` int DEFAULT NULL,
                    `SignatureAgentsRankedByUsage` text,
                    `RoundsPlayed` int DEFAULT NULL,
                    `Rating` double DEFAULT NULL,
                    `AverageCombatScore` double DEFAULT NULL,
                    `KillsDeath` double DEFAULT NULL,
                    `KAST` text,
                    `ADPR` double DEFAULT NULL,
                    `KPR` double DEFAULT NULL,
                    `APR` double DEFAULT NULL,
                    `FKPR` double DEFAULT NULL,
                    `FDPR` double DEFAULT NULL,
                    `HeadshotPercent` text,
                    `ClutchSuccessPercent` text,
                    `Kills` int DEFAULT NULL,
                    `Deaths` int DEFAULT NULL,
                    `Assists` int DEFAULT NULL,
                    `FirstKills` int DEFAULT NULL,
                    `FirstDeaths` int DEFAULT NULL,
                    `Year` int DEFAULT NULL,
                    `League` text,
                    `IGL` text,
                    `CleanedRating` double DEFAULT NULL,
                    `AdjustedRating` double DEFAULT NULL,
                    `SelflessIndex` double DEFAULT NULL,
                    `Region` text
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            '''.replace('\n', '').replace('\r', '')

            try:
                self.cursor.execute(query)
                self.cursor.execute(f'''LOAD DATA LOCAL INFILE 'C:/Users/handy/Desktop/Codebase/VCT-Hackathon/src/export/toSQL/{file_name}' INTO TABLE {table_name} FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'  IGNORE 1 ROWS;''')
                self.connect.commit()
            except Exception as e:
                print(f"Something occurred during table creation and loading of {table_name} and {file_name}, verify your tablename and file paths are correct.")
                print(e)
        elif(table_name == 'TeamData'):
            self.cursor.execute(f'DROP TABLE IF EXISTS `{table_name}`')
            query = '''
                    CREATE TABLE `TeamData` (
                    `TeamId` int DEFAULT NULL,
                    `Name` text,
                    `Country` text,
                    `Wins` int DEFAULT NULL,
                    `Loses` int DEFAULT NULL,
                    `Winrate` double DEFAULT NULL,
                    `GameChangerWins` int DEFAULT NULL,
                    `GameChangerLoses` int DEFAULT NULL,
                    `Region` text,
                    `Status` text
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                '''.replace('\n', '').replace('\r', '')
            try:
                self.cursor.execute(query)

                self.cursor.execute(f'''LOAD DATA LOCAL INFILE 'C:/Users/handy/Desktop/Codebase/VCT-Hackathon/src/export/toSQL/{file_name}' INTO TABLE {table_name} FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'  IGNORE 1 ROWS;''')
                self.connect.commit()
            except Exception as e:
                print(f"Something occurred during table creation and loading of {table_name} and {file_name}, verify your tablename and file paths are correct.")
        elif(table_name == 'PlayerAgentPerformance'):
            self.cursor.execute(f'DROP TABLE IF EXISTS `{table_name}`')
            query = '''
                    CREATE TABLE `PlayerAgentPerformance` (
                    `Player` text,
                    `Team` text,
                    `Agent` text,
                    `Usage` double DEFAULT NULL,
                    `RoundsPlayed` int DEFAULT NULL,
                    `Rating` double DEFAULT NULL,
                    `AverageCombatScore` double DEFAULT NULL,
                    `KillsDeath` double DEFAULT NULL,
                    `ADPR` double DEFAULT NULL,
                    `KAST` text,
                    `KPR` double DEFAULT NULL,
                    `APR` double DEFAULT NULL,
                    `FKPR` double DEFAULT NULL,
                    `FDPR` double DEFAULT NULL,
                    `Kills` int DEFAULT NULL,
                    `Deaths` int DEFAULT NULL,
                    `Assists` int DEFAULT NULL,
                    `FirstBloods` int DEFAULT NULL,
                    `FirstDeaths` int DEFAULT NULL,
                    `Games` int DEFAULT NULL,
                    `CleanedRating` double DEFAULT NULL,
                    `AdjustedRating` double DEFAULT NULL,
                    `SelflessIndex` double DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                '''.replace('\n', '').replace('\r', '')
            try:
                self.cursor.execute(query)
                self.cursor.execute(f'''LOAD DATA LOCAL INFILE 'C:/Users/handy/Desktop/Codebase/VCT-Hackathon/src/export/toSQL/{file_name}' INTO TABLE {table_name} FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'  IGNORE 1 ROWS;''')
                self.connect.commit()
            except Exception as e:
                print(f"Something occurred during table creation and loading of {table_name} and {file_name}, verify your tablename and file paths are correct.")
        elif(table_name == 'PlayerTeamMap'):
            try:
                self.cursor.execute(f'DROP TABLE IF EXISTS `{table_name}`')
                query = '''
                CREATE TABLE `PlayerTeamMap` (
                `TeamId` int DEFAULT NULL,
                `Player` text,
                `Status` text
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                '''.replace('\n', '').replace('\r', '')

                self.cursor.execute(query)
                self.cursor.execute(f'''LOAD DATA LOCAL INFILE 'C:/Users/handy/Desktop/Codebase/VCT-Hackathon/src/export/toSQL/{file_name}' INTO TABLE {table_name} FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'  IGNORE 1 ROWS;''')
                self.connect.commit()
            except Exception as e:
                print(f"Something occurred during table creation and loading of {table_name} and {file_name}, verify your tablename and file paths are correct.")


        




