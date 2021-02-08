# AutoCommercial
 A project to automatically launch Twitch commercial by comparing 1 image to a reference commercial/break asset
 
 ## How to
* Install python https://www.python.org/downloads/ WITH the option "ADD PYTHON TO PATH"
* Install the needed python librairies launching SETUP PIP.bat
* Get your tokens from https://twitchtokengenerator.com
=> Available Token Scopes : check all, then generate token !

* Copy "config_example.py" file into a new file named "config.py" (just renaming is ok)

* Change your credentials in new config.py file with these informations :

* client_id = your client ID
* oauth_token = your access token
* channel_name = your twitch channel name
* difftrigger = 10 # the maximum percentage difference between 2 image to trigger the commercial
* rtmp = the final rtmp adress where we extract the image
* Configure the final cropping of image to match your reference.png
* left = 0
* top = 0
* right = 1920
* bottom = 1080


* Create a reference.png image with an extract from of your own stream's commercial break


* launch with LAUNCH.bat


get updates on https://github.com/painteau/AutoCommercial
