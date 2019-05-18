import os
import time

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import urlopen


os.chdir("./Scraped Data")


def SCRAPER(url):

	# Collect data #

	html = urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")
    
	AwayTeam = soup.find_all('td', attrs = {'class':'away-team'})
	AwayTeamClean = []
	for x in AwayTeam:
		AwayTeamClean.append(x.text)
    
	HomeTeam = soup.find_all('td', attrs = {'class':'home-team'})
	HomeTeamClean = []
	for x in HomeTeam:
		HomeTeamClean.append(x.text)
    
	Scores = soup.find_all('a', attrs = {'class':'match-score'})
	ScoresClean = []
	for x in Scores:
		ScoresClean.append(x.text)
    
	Dates = soup.find_all('td', attrs = {'class':'match-date'})
	DatesClean = []
	for x in Dates:
		DatesClean.append(x.text)
        
	Ground = soup.find_all('td', attrs = {'class':'ground'})
	GroundClean = []
	for x in Ground:
		GroundClean.append(x.get_text(separator=' '))
        

	# Convert to dataframe #
	
	DATA = pd.DataFrame(list(zip(HomeTeamClean, ScoresClean, AwayTeamClean, DatesClean, GroundClean)), columns = ['HomeTeam', 'Score','AwayTeam', 'Date', 'Ground'])    
    
	# Output data #
	
	return(DATA)
	


NATIONS = ['england', 'france', 'italy', 'wales', 'ireland', 'scotland']

# loop through different sites. we are going to do this twice so that we get combinations of countries. 

ExistingPairs = []

for nation1 in NATIONS:
	for nation2 in NATIONS: 
		
		# Check if we are doing both nations twice # 
		if nation1 == nation2: 
		
			continue
			
		else:
			if nation2+nation1 in ExistingPairs:
            	
				continue
            
			else:
				ExistingPairs.append(nation1+nation2 )
    			
				url = "http://www.rugbydata.com/" + nation1 + "/" + nation2 + "/gamesplayed/"
    
    			# We wrote the scraper code above, so we are going to call that function and run the scraper #
    			
				data = SCRAPER(url)
    			
    			# Save the data as a CSV file # 
    			 
				filename = "RugbyData_Matchup_" + nation1 + " v " + nation2 + ".csv"
    
				data.to_csv(filename, mode = 'w')			