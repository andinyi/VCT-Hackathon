import igl 
import playerGrab
import inDepthMatchPull
import aggregationFile

def main():
    #fetchVLR.matchListFetch() #Writes Data to Current Folder
    aggregationFile.aggregation('players_chunked')
    #aggregationFile.aggregateTeams()

if __name__ == "__main__":
    main()