AM - a Discord Music Bot from The Atomic Corporation
====================================

This is a Python based music bot that works exclusively with YouTube. The bot's installation process is designed to be seamless and easy to install for Windows, Mac, Linux, or other UNIX based computers.

It functions by downloading the video as a .webm file to it's folder, and then plays that .webm file through a voice channel. The file is downloaded contains JUST audio, no video.

Once playback has ended, been stopped, skipped, or when the bot shuts down, the .webm file will be deleted. It does NOT directly interact with the YouTube video stream. Because of this, I can not guarantee it will work on your computer, or your internet connection.

You will know if the bot works on your computer or not by looking at your Terminal/Console. If you see an HTTP error (probably 403), it likely means that it unfortunately does not.

(UPDATE as of v2.0.0: The 403 error should be fixed). If it still occurs, I am most likely unable to fix it as it is caused by a direct "wall" put up by YouTube themselves, and varies depending on which machine the bot runs on.

Important: Make sure you have adequate space for the bot to function!

IMPORTANT II: As of Version 2.0.4, no installation is needed for Windows. Simply download the Windows release, run the "AM.exe" file, and the "UpdateRequirements.exe" file periodically.



Installation Instructions:
==========================
Before starting, create a discord bot, set up its permissions as Admin, and get it's token. (There are numerous videos and articles on how to do this). Then, open the bot_settings.txt file and replace "your_token_here" with your bot's token. (OPTIONAL) If you want to change the bot's prefix, you can do it in the same bot_settings file. That's the first line in the file.

IMPORTANT: Do NOT change the positioning of the information in bot_settings.
____________________________________________________________________________

FOR LINUX/MAC/UNIX BASED MACHINES:
--------------------------------

0. Download the AM.zip file from GitHub

1. Extract the AM folder from the downloaded zip file.

2. Through the Terminal, CD to the AtomicMusicBot folder.

3. Open InstallerPackage.sh through the Terminal by running the command "./InstallerPackage.sh" (without quotes) -- this will install the Bot's dependencies.

3.1. (OR) Run the Bot through Terminal directly. -- CD to the folder, and type "python3 AM.py" (without quotes)

4. Open UpdatePackage.sh through the Terminal by running the command "./UpdatePackage.sh" (without quotes) -- this will update dependencies (if there is an update)

5. Double click the "runBot.sh" file, and select "Run in Terminal".

6. Periodically run "UpdatePackage.sh" to keep dependencies up to date.




Troubleshooting:
--------------
1. The bot doesn't play anymore! --> Run either UpdatePackage.sh (for Linux) or UpdateRequirements.exe (for Windows).
2. The bot STILL doesn't play! --> Wait for an updated version of the bot, re-install the bot, and try again.



Closing Statement:
-----------------
This bot is Open-Source. You are free to make any and all modifications to this program as desired. If you have a fix or an improvement that you made, and would like to have it added, let me know.

This bot was made by using existing libraries and modules found on GitHub. Credit for usage of these goes back to their respective owners.

As of 3/11/2025, "Atomic Incorporated" does not exist (at least under me). There are no copyright holders. I do not have a copyright on this program. The name is for visuals exclusively.

https://www.atomiccorp.org/
