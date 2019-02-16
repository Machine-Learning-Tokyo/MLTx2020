# Currently using tweepy but will try to use the tweeter API from Rakuten
# Need to try the translation API

import tweepy
from googletrans import Translator
import datetime

#import unirest not supported on python3

class TweetGenerator:
    
    def __init__(self):
        # Setting the key for identification
        self.CONSUMER_KEY ="hEejKZrYXMbN2lsQPmHYnCpvY"
        self.CONSUMER_SECRET = "k9a8nFVaDbmUJyDZBAwwdmc1miqh8sDWjJu1AohJw03oiUnPn2"   
        self.ACCESS_KEY = "1096442165448720385-TYxgNnoYL3z5GmKavNjFgcqvXw4ViA"    
        self.ACCESS_SECRET = "1jNRID3iJhdDqL0Yq2hAlhJCMlA7AubodvZ0997gY5Wfy"
        
        # Set the access:
        self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        
        # Set up the api:   
        self.api = tweepy.API(self.auth)
        
        # Set up the translator:
        self.translator = Translator()
        
    def send_tweet(self, tweetText):
        # Send the status
        self.api.update_status(tweetText)
        
    def trnsl_JP(self, englishText):
        # Somehow call working API to translate
        jpText = self.translator.translate(englishText, dest='ja').text
        jpText = "[JAPANESE] " + jpText
        return jpText
        
    def trnsl_KO(self, englishText):
        # Somehow call working API to translate
        koText = self.translator.translate(englishText, dest='ko').text
        koText = "[KOREAN] " + koText
        return koText
    
    def multilanguageTweet(self, englishText):
        # Translate and send the different tweet
        if(englishText ==''):
            return(0)
            
        koText = self.trnsl_KO(englishText)
        self.send_tweet(koText)
        print("Korean tweet send")
        
        jpText = self.trnsl_JP(englishText)
        self.send_tweet(jpText)
        print("Japanese tweet send")
        
        self.send_tweet("[ENGLISH] " + englishText)
        print("Englsih tweet send")
        
    def ruleBaseGenerator(self, camera1, nbpeopleC1, camera2, nbpeopleC2):
        # Generate the message to tweet based on the camera
        currentDT = datetime.datetime.now()
        englishText =""
        if(nbpeopleC1 > nbpeopleC2):
            englishText = str(currentDT.day) +'/'+ str(currentDT.hour) +" | Please go to " + camera2.name
            
        if(nbpeopleC2 > nbpeopleC1):
            englishText = str(currentDT.day) +'/'+ str(currentDT.hour) +" | Pleae go to " + camera1.name
        
        return englishText
        
        
