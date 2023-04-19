This folder contains all the versions of the files which are used to create the final results published in my thesis. There are plenty of other versions of these files which have not been included.

oeis.py relates to chapter 1, while all other files relate to the models in chapter 2. Here's a quick overview of how I ran the models.

The raw data downloaded from ausmash.com.au is aggregated in Melee matches.csv (I did some processing to combine a few hundred files into a single file). Melee matches2.csv is the same file with character IDs replaced with names. Melee players.csv was also scraped using the ausmash API.

splitwl2.py then uses Melee matches2.csv to create Melee winners3.csv and Melee losers3.csv

BTv2.R contains all the code used in the final models. These models take several hours to run each, so an image with the final results has been saved in BTFinal.RData.
