import streamlit as st

st.header('Hello 👋! Welcome to our **VCT Hackathon Project**', divider="grey")
st.markdown('##### Made by Handy, Tazrian, and Ridhima 👀')

st.markdown("""### Inspiration and About
>We wanted to create a LLM powered chatbot that will assist with picking competitive Valorant Players based on their stats over a course of competitive games.
>
>We fundamentally believed that a player who is able to reach high tier stages and tournaments has the experience and consistency to excel as a competitive player and thus should be prioritized in our selection process, hence our solution is primarily focused around this fact. 
### What it does
>This is a chatbot interface directly connected to our operational agent from AWS Bedrock. 
>
>The Agent itself is powered by Claude Sonnet 3 and utilizes a knowledge base that contains tabular definitions and stat descriptions.
### How we built it
The different sections of this build are listed below as well as further breakdowns as needed.

 #### 1. Data Fetch and ETL
> - The data was primarily sourced from VLR where we used BS4 to webscrape for the player stats across each tournament. 
> - We then cleaned the data and then imputated missing data with average values to eliminate misleading stats that are caused by missing data.
> - The data was formatted and joined to create our SQL tables and stored in RDS.

 #### 2. Methodology : Data 
 ###### :orange[Big Wall of Text Incoming :warning:]
            
 We quickly identified that there was no real way for us to rank players without oversights, other websites and organizations have previously attempted this but we saw fundamental flaws with a number of the implementations. We saw the vision behind the Rating metric but also see how it may fall short when considering players under the notion of consistency and experience. We also saw a possible favoritism towards players who may supporting agents that do not take front and center on a stat screen as well. Due to this we wanted to run some tests on some of our ideas that circumvent these issues.

 - **Winner Winner** 
            
    We determined that the most fundamental metric to success is the ability for the player to win. With the nature of Valorant, winning the game does not solely rely on a specific player's ability to do well but also has direct relationships with the performance of their teammates as well as their opponents. 
    
    To address this issue we determined that the winnings of the team would be a good substitution for ranking the list of teams for how 'often' or likely they are to win. This is then used to visualize how much a stat directly correlated to a group of players being 'best of the best'.

 - **"I popped off that one game..."** 
    
    We all have our own share of great games, but when we're attempting to select players for the highest level of play, consistency needs to be a factor. A player can easily do well in a couple games but still lose said games. 
                
    In an event like this we wanted to consider **how** much better they did. To address this we introduced a log scaling method called AdjustedRating. This formula scales down the ratings of players that have high ratings but do not have the majority of the rounds to be considered significant. This is then used to create a ratio to the player with the highest amount of rounds played in our tournament so that we are left with an coefficient to adjust our rating by. 
            
    This rating is formulated by the following function. 
            

    $$
        (log(n) / log(m)) * R
    $$

    Where n is the number of rounds, m is the max number of rounds in the event, and R is rating.        

    When this is measured against our winnings chart we can see that the AdjustedRating now has a direct tie to the placement of a player in professional matches.
            
    ![adjustRatingRank](https://public-bucket-andy.s3.us-east-1.amazonaws.com/AdjustedRatingRank.PNG)

- **Supports Rise Up** 
            
    The calculation of rating tends to favor players who play more aggressively and are able to get frags and kills. While all agents can play like this it's a bit unfavorable for players who play a more passive/supportive role. To show our Controllers and Sentinels some love we wanted to introduce a concept called SelflessIndex. 
            
    Conceptually it's a ratio taken by dividing a players APR by their KPR. The ratio created is directly tied to how often a player gets assists compared to kills. While not necessarily a negative trait for supportive roles, we expect to see supportive agents to have a higher SelflessIndex due to the nature of their utility. A player with a high SelflessIndex then can be theoretically said to be a more supportive or utility based player. 

    $$
        apr / kpr
    $$

    This stat then is used by the LLM Agent to select a key supporting roles in the team's composition. A breakdown of Average SelflessIndex by Agent for each agent played during the league is provided below for context.

    ![imageSelflessIndexByAgent](https://public-bucket-andy.s3.us-east-1.amazonaws.com/SelflessIndex.PNG)

#### 3. Methodology : LLM
We utilized Bedrock's wide range of access to different models to create a baseline test attempting to select a model that meets our performant requirements. We concluded on Claude Sonnet 3.0 as it was fast enough to be used for Agents which utilize ReAct Prompting.

The LLM is provided a knowledge base that stores table and column definitions, and access to a Lambda function that runs a query that the LLM will be generating. This allows the LLM to directly pull for the information needed to create a selection of players.

The LLM is prompt engineered to generate this query and also given some insight and selection guidelines for the players it will be selecting.
            
**Insights**
- We originally tried directly ingesting every stat into the knowledge base but this caused a significant problem with consistency, response time, and hallucinations. We also saw some fundamental problems when working through this model where stats and rankings would have to be manually ingested after being calculated as well, for our case this didn't make sense.

- We also originally intended to give more leeway to the Bot to come up with the best answer but this of course opened up a can of worms of hallucinatory effects and incorrect information.           

#### 4. Methodology : Front-End UI / App
> For our user interface / chat interface we finalized on Streamlit as our tool of choice as it provided all the necessary frameworks for a functional chatbot without introducing much more complexity.
>
> We implemented adhoc streaming of the traces so that the agent's thought process can be tracked by the user, this also fundamentally solves our problem with long pending responses.
>
> Status trackers are also added for less pain as users sit around waiting for the agent to complete it's orchestration and generation steps.
> 
> Invokations of other tools is also provided via a debug window for santiy checks.
>
> Overall I believe this makes reading into what the bot is doing much simplier and a lot less painful.            
            """)