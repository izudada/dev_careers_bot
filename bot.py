import tweepy
from decouple import config
import smtplib
from datetime import datetime


CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
ACCESS_KEY = config('ACCESS_KEY')
ACCESS_SECRET = config('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

name = 'dev_careers'

tweets = api.user_timeline(screen_name=name, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )

sender = 'from@fromdomain.com'
receiver = 'tonyudeagbala@gmail.com'

message = """From: My Devcareer's Bot <{}>
To: Me <{}>
Subject: @dev_careers Tweeted

Omo! @dev_careers just tweeted oo
@dev_careers:  
    {}
    At {} 
""".format(sender, receiver, tweets[0].full_text,  tweets[0].created_at)

EMAIL_HOST_USER = 'tonyudeagbala@gmail.com'

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

date_time_str = '2021-09-21 19:52:50' # Date I commence monitoring their tweet

new_date = datetime.strptime(str(tweets[0].created_at), '%Y-%m-%d %H:%M:%S')

last_date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

if new_date > last_date:
    try:
        api.retweet(tweets[0].id)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD )
        server.sendmail(sender, receiver, message)         
        print("Successfully sent email")
        last_date = new_date
    except Exception as e:
        print(e)
        print("Error: unable to send email")
else:
    print('Already got a notification for this')