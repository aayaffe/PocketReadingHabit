# PocketReadingHabit
A simple python script to help create a reading habit with Pocket. I created this script to help me move along with my reading list.
This script connects to [Pocket](getpocket.com) and selects a random article to send to your email.

Beware this script is a first draft and is quite **fragile**.

## Setup

* Change the name `config_template.py` to `config.py`
* Fill in all the missing configuration constants and credentials according to instruction laid in the comments.
* Download [Selenium ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and save in the same directory as the script.
* **Warning: Do not** upload this file into a version control for it contains private information.
* Add a scheduled task ([Task scheduler](https://blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip/) for windows or Cron for Linux) to run the script as many times a day as you require.

The script was only tested on a Windows 10 machine.
