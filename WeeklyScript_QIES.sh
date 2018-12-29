# Exectues Daily Script 5 times to simulate 5 days worth of interactions 

# Variables:
# day = the day to be exectued 

# Purpose:
# Calls Daily Script 5 times to simulate 5 days
for day in {1..5} ;
do 
    ./DailyScript.sh Day"$day"
done

