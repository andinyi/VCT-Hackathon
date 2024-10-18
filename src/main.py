import igl 
import playerGrab
import inDepthMatchPull
import aggregationFile
from mysql import mysqlConnect


def main():
    #fetchVLR.matchListFetch() #Writes Data to Current Folder
    #aggregationFile.aggregation('players_chunked')
    #aggregationFile.aggregateTeams()
    #aggregationFile.joinRegions()
    connection = mysqlConnect('admin', input('Enter Password'))
    connection.connectToDB()
    connection.createAndLoadTables('Players', 'player.csv')
    connection.createAndLoadTables('TeamData', 'team_data.csv')
    connection.createAndLoadTables('PlayerAgentPerformance', 'player_agent_performance.csv')
    connection.createAndLoadTables('PlayerTeamMap', 'player_team_map.csv')
    


if __name__ == "__main__":
    main()