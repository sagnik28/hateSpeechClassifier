This file contains instructions on how to run the work done by group 19 of Web Data Processing Systems, 2020 at Vrije Universiteit Amsterdam.

Option 1 (Recommended for computers with less than 8GB RAM):
	Run the notebooks using google colab as they provide upto 13GB free RAM. We used this too as we run computers with 4GB and 8GB RAMs: 
		1. Correct the path in the beginning of the notebook "refinetweets.ipynb". This path should point to the raw data file, in our case, "ElectionTweetsFinal.JSON".
		2. Simply run this notebook. This provides a dataframe of cleantweets which will be used as the input for the next notebook. in our case, "cleanedElectiontweetsFinal.csv".
		3. Correct the path in the beginning of the notebook "featureEngineeringandModeling.ipynb". This path should point to the file containing the clean set of tweets, in our case, "cleanedElectiontweetsFinal.csv".
		4. Simply run this notebook.


Option 2:
	Use the src files:
		1. Correct the path in "refinetweets.py" to point to the raw data file. Build and run.
		2. Correct the path in "featureEngineeringandModeling.py" to point to the file containing the clean set of tweets. Then build and run.
		3. If using the "listener.py" to scrape tweets, edit the authentication credentials and path. Then build and run.