# MixDrink

![iOS App Demo](https://github.com/akun1/MixDrink/blob/master/5edc7fca320x568r%20(1).gif?raw=true)

XCode app and everything related to the UI is listed under MixDrinkClient, and server including scrapers and recommender code is under MixDrinkServer.

Dependencies:
Client Dependencies:
Mac Machine and XCode

Server Dependencies:
dependencies listed under MixDrinkServer/recipe-scrapers/requirements.txt

# Class Demo Video

[MixDrink Demo](https://youtu.be/HaqLkxOMtHM)

# Setup
1. Clone the repository

# Client setup
1. Open the .xcworkspace in XCode.

2. Setup your Apple credentials by logging in with your Apple id and changing 'Team' field in project settings to your id team.

3. Be sure you've allowed the app access to your keychain login for AppleId (restart computer to generate popup if necessary)

4. At the top bar, select a simulator iPhone or plug in your iPhone and select that.

5. Click 'Run' or Debug>Run on the top bar.

# Server Setup

1. Run ./setup.sh to install all the server dependencies if on linux  
   Use ./setupmac.sh for mac (you will need Homebrew)

2. sudo python3 aggregator.py
