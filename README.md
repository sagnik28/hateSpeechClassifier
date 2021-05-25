# hateSpeechClassifier
A hate speech classifier based on tweets surrounding the 2020 US elections.

Data was obtained using "snscrape". 
To use snscrape, ensure your system has snscrape installed and then from your command line, enter:
snscrape --jsonl --progress --max-results 30000 --since 2020-11-26 twitter-hashtag "USElections until:2020-11-28"  BlackFridaytweets.json


