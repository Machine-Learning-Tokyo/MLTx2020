import pandas as pd
import matplotlib.pyplot as plt

# dedicated object
import tweetGenerator as tw
import camera

# Create Camera object (obtained from registration)
camera1 = camera.camera(1, 80, 200, "C1", "entrance A", "stadium")
camera2 = camera.camera(2, 500, 200,"C2", "entrance B", "stadium")

# Load the database (currently dummy data)
dummydatabase = pd.read_csv('facedata.csv',delimiter=";")
print(dummydatabase.head())

# Get the number of people and waiting time at each camera (time can be set in the query)
TIME = '10:00:00'

# Camera1
query = dummydatabase.loc[dummydatabase['camera'] == 'C1'].loc[dummydatabase['time']== TIME]
waitingtimeCamera1 = query.waiting
waitingtimeCamera1 = waitingtimeCamera1.reset_index(drop=True)[0]
nbpeopleC1 = query.nbpeople
nbpeopleC1 = nbpeopleC1.reset_index(drop=True)[0]
print(waitingtimeCamera1)
print(nbpeopleC1)

# Camera 2
query = dummydatabase.loc[dummydatabase['camera'] == 'C2'].loc[dummydatabase['time']== TIME]
waitingtimeCamera2 = query.waiting
waitingtimeCamera2 = waitingtimeCamera2.reset_index(drop=True)[0]
nbpeopleC2 = query.nbpeople
nbpeopleC2 = nbpeopleC2.reset_index(drop=True)[0]
print(waitingtimeCamera2)
print(nbpeopleC2)

### Generate the heatmap of the stadium (all the numerical value are here to make the display looks better)
heatmapC1 = plt.Circle((camera1.coorX, camera1.coorY), nbpeopleC1*8, color='r')
heatmapC2 = plt.Circle((camera2.coorX, camera2.coorY), nbpeopleC2*8, color='g')

img = plt.imread("staduim1.PNG")
fig, ax = plt.subplots()
ax.add_artist(heatmapC1)
ax.add_artist(heatmapC2)
plt.axis('off')

plt.text(camera1.coorX - 20, camera1.coorY, str(waitingtimeCamera1) + "min", fontsize=12)
plt.text(camera2.coorX - 20, camera2.coorY, str(waitingtimeCamera2) + "min", fontsize=12)
ax.imshow(img)

plt.savefig('savedheatmap/heatmap.png')

### Tweet generation
tweetAPI = tw.TweetGenerator()
englishText = tweetAPI.ruleBaseGenerator(camera1, nbpeopleC1, camera2, nbpeopleC2)
tweetAPI.multilanguageTweet(englishText)    

### Fancy Bussniss statictics: for demography / live advertissement tunning based on gender / age
dummydatabase.groupby("camera").plot()

