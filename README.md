# PocketReadingHabit
A simple python script to help create a reading habit with Pocket. I created this script to help me move along with my reading list.
This script connects to [Pocket](getpocket.com) and selects a random article to send to your email.

Beware this script is a first draft and is quite **fragile**.

## Setup

* run 'pip install pocket'
* You will need to run the main.py once manually for configuration
* You need to have a pocket consumer key: https://getpocket.com/developer/docs/authentication and a http://www.mailgun.com account
* Add a scheduled task ([Task scheduler](https://blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip/) for windows or Cron for Linux) to run the script as many times a day as you require.

The script was only tested on a Windows 10 machine.