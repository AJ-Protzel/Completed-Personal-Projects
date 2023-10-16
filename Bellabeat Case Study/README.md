# Ask - Defining the task:
Chief Creative Officer of Bellabeat, Urska Srsen, has asked me to help inform marketing strategies. I am to look at usage data of current inhouse smart devices and outside devices for any insights to new products or features. I am then supposed to report my findings to the Bellabeat marketing team.

# Prepare - Describe data sources:
Fitbit data from March 2016 to May 2016 provided by Bellabeat and Fitabase. A total of 30 eligible, anonymous, volunteer users provided this data, including minute level output. Recordings of physical activity, heart rate, sleep monitoring, daily activity, steps. CSV file format, mixed long and wide format. Files: Steps, Daily Activity, Sleep, Heart Rate, Intensity, Calories Burned, MET, Weight.
https://www.kaggle.com/datasets/arashnic/fitbit/

**Bellabeat products:**
**Bellabeat app:** Tracks activity, sleep, stress, menstrual cycle, mindfulness habits, hydration levels; Links to all smart wellness products.
**Bellabeat membership:** Subscription for personalized 24/7 guidance on nutrition, activity, sleep, health, beauty, and mindfulness based on users lifestyle and goals.
**Leaf:** Tracks activity, sleep, stress; Wearable as bracelet, necklace, or clip; Syncs to app.
**Time:** Tracks activity, sleep, stress; Classic watch; Syncs to app.
**Spring:** Tracks daily water intake; Water bottle; Syncs to app.

**Ivy:** Tracks activities, steps, sleep, heart rate, meditation, calories burned; Wearable as bracelet; Syncs to app.

The Fitbit data can be compared to Ivy the best however by the number of items tracked. Ivy was found as a listing on Bellabeats site rather than on the provided list of products. Therefore, Ivy will not be considered for products to improve. Time is the next closest product to a Fitbit and will be used in this comparison.

**Other sources:** Fitabase (Fitbit) Data Dictionary. Explanation of values and descriptions.
https://fitabase.com/media/1930/fitabasedatadictionary102320.pdf

# Process - Cleaning and manipulating data:
1. Importing into Excel
2. Separated Time column into days and hour
3. Added UID (unique ID) to each table using concat(ID,ActivityDay)
4. Merged daily files into one file on UID
5. Merged hourly files into one file on UID
6. Added UID to weightLogInfo_merged and minuteSleep_merged
7. Renamed files ###_merged and saved all in long format
8. Put merged files into “Working Files” folder
9. Added TimeInBedAwake = TotalTimeInBed-TotalMinutesAsleep
10. Added DeviceLeftBehind T/F

# Analyze - Identifying trends and relationships:
The more steps taken equals a longer distance traveled per day. And most people walk about 9000 a day with an outlier of someone that walked an equivalent distance of a marathon. The trends mostly match distance and number of steps so there is low likelihood of cheated steps.

![Daily Distance vs  Steps Taken](https://github.com/AJ-Protzel/Personal-Projects/assets/31741271/ad6e398e-b50b-4604-a5c9-c9f679fcf863)

The graph proves that people who spend less time in bed and not sleeping have higher calories burned throughout the day. Most people spend about an hour a day in bed while not sleeping.

![Calories Burned While In Bed Awake](https://github.com/AJ-Protzel/Personal-Projects/assets/31741271/43ef1dab-e358-42ba-b024-3c5427d352b1)

This shows a trend of sleeping versus walking activity. While people who spend less time in bed have larger step counts. Sleeping too much or too little also affects how active the user is. The average person will sleep for about 7.5 hours which is also an ideal time for energy as distances walked trend downwards after more sleeping.

![Daily Distances vs  Min  of Sleep](https://github.com/AJ-Protzel/Personal-Projects/assets/31741271/4d5f065c-bb48-4320-be91-8a08f2ba6760)

Distance walked is both tracked and manually logged by the user. And so by checking the tracked + logged distance to the total recorded distance shows that the data is inaccurate. Meaning distance logged is most likely not added to total distance.

![Tracked+Logged Distance = Total Distance](https://github.com/AJ-Protzel/Personal-Projects/assets/31741271/6362e366-9ec4-402b-b57f-ccea502dcd4d)

This shows what days  have the most steps taken. The middle of the week (Tuesday and Thursday) are the most active amongst the users.

![Total Steps By Day](https://github.com/AJ-Protzel/Personal-Projects/assets/31741271/0296eb32-f713-4fbd-a794-a4f844f447fb)

The days when the Fitbit were most often forgotten or misplaced were on weekends.

![Days When Device Was Forgotten](https://github.com/AJ-Protzel/Personal-Projects/assets/31741271/2987d86a-f438-463b-90bb-e599a6386145)

# Share - Providing Insights and Recommendations:
Not all users are diligently logging all activities. The device does automatically track and record activity but users are also either forgetting to wear the device or take them off for inaccurate data collection. There are clear days of motivation to wear and or log on to the Fitbit.

Looking at the data, I would say that people do wear their Fitbits to sleep. And days that have no activity are most likely from needing to take off the device to change and then forgetting or leaving it while they continue their day. It is also a possibility of either fashion and necessity, not needing the function of a watch or activity tracker on weekends while they relax at home away from work. Or the device does not suit their outfits and so they elect to leave it at home. More data would need to be gathered to determine if the aesthetics of the device needs improvement.More data will need to be viewed to determine how often the user views their own data and on what device. Sales between the Ivy and Time may tell us what users prefer, simple automated activity tracking, or more general device usage.

During the week and while the device is worn. Users tend to prefer their data to be tracked automatically. So I would recommend focusing on improving automated activity tracking and battery life. 

However, apart from the data that shows when the Fitbit is most likely forgotten or not worn. The data does not tell us the most used features or most wanted features of the Fitbit.

# Act - Final Conclusion:
The marketing team can emphasize a longer battery life and ease of use or automated activity tracking. There can also be a new selection of designs or colors for the device.


