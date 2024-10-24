# VCT-Hackathon
<p>A basic LLM application for selecting Competitive Valorant Players for an optimized team.<br>
A submission to the following hackathon, https://vcthackathon.devpost.com/.<p/>

## Table of Contents
1. [About](#About)
2. [Tools](#Tools)
3. [Data](#Data)
4. [Methodology](#Methodology)
5. [Challenges](#Challenges)
6. [Attribution](#Attribution)

## About
We wanted to create a LLM powered chatbot that will assist with picking competitive Valorant Players based on their stats over a course of competitive games.

We fundamentally believed that a player who is able to reach hier tier stages and tournaments has the experience and consistency to excel as a competitive player hence our solution is primarily focused around this fact.

## Tools
Our project primarily uses Python and AWS for it's functionality. A further breakdown of this is provided below.

### Python Libraries
- Requests
- BeautifulSoup4
- Pandas
- Matplotlib/SciPy
- PyMySQL

### AWS Services
- Bedrock / Knowledge Bases / Agents / Model: Claude Sonnet 3
- Lambda
- EC2
- RDS
- S3

## Data
The our main source of data comes from VLR.gg, we scraped for player and tournament data to be used with our LLM Model. <br>
We also utilized IGL categorizations and winning team data from Liquidpedia.

## Methodology
<p>Our solution builds on top of previously defined metrics used to measure player performance. Most sites, such as VLR and THESPIKEGG and TRACKER have their own internal formula for calculating 
player performance. These formulas often attempt to take all elements of a players stats into account to generate a rating or elo for the player. We believe that this lays the foundations of 
rating players and determining how 'good' the player is. This rating is heavy focused on in our implementation.</p>

<p>We also identified that this rating system may not give the entire picture as some elements can be missed as they integrate into a singular number. For example we believe that a player who has achieved a high rating from a lower number of games and round in the particular tournament may not present reliable information regarding their performances. We also identified that the rating metric has a tendency to reward aggressive and explosive players more than players who may play a calm and collected game.</p>

To address this issue we wanted to introduce a 2 new metrics:
* *AdjustedRating*
* *SelfishIndex*

These two metrics are then directly calculated for each player's overall performance in an event series and is then used by the LLM model to make selections in regards to team members and players.

A detailed document that goes further in depth regarding this implementation can be found via this following [link](http://jettreviveme.com/). 

## Challenges
As anybody working with data, we struggled a lot with data errors and visualizing a story from the data we had access to. One of the biggest issues we had was determining what was the best realistic way of identifying players that were good. I believe as these type of questions have no real answers we really struggled without the necessary competitive knowledge on this front.

Our domain knowledge, specifically in the competitive field of Valorant, was also very limited. We mostly happen to be low rank bronzies and silvers but we tried our best using what knowledge we had!

This was all of our first time utilizing multiple AWS services to this scale and we also struggled as we were learning new tools and techniques. For this, I want to give special thanks to everyone from AWS who offered help and guidance to all entrants throughout this process!

## Attribution
- In Game Leader Data from Liquidpedia Catergorization, https://liquipedia.net/valorant/Category:Intogame_leaders. Expansion of data accessed via provided player hyperlinks.
- Winnings Data from Liquidpedia, https://liquipedia.net/valorant/Statistics/2024.



