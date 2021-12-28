# TwitchAPI and BigQuery
Twitch nowadays is one of the most popular live streaming service geared towards gamers. Besides this majority audience, in the last few years Twitch has proven to be a major player in live entertainment, not just for gamers now but for artists, content creators or any other organization looking to livestream their broadcast and connect with their viewers.<br/>
The following project aim to collect data from the top 25 streams with more views, modelling and storing these data every hour on Google BigQuery. Afterwards all the stored data can be retrieved and plotted for data analysis insights.<br/><br/>

-Collecting real and current data through Twitch API (MyAPI.py). <br/>
-Data modelling building a dataframe with all necessary attributes (MyAPI.py).<br/>
-Storing dataframe on Google BigQuery (export.py).<br/>
-Automating the storage process through schedule lib (scheduling.py)<br/>
-Data visualization queued data (plot.py)
