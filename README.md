# G-Suite Downloader

A tool for auto-downloading documents from Google Drive, such as a spreadsheet 
people are working on that you would like to sync to a study drive.

## Setup

Based on https://developers.google.com/drive/api/v3/quickstart/python

First, go to the quickstart and enable the Drive API for your wisc.edu Google
account. It will make you pick a name. Call it something like "Study drive 
downloader". For OAuth app kind, choose "Desktop app".

Save the `credentials.json` in this dir, and make it only readable by you.

With your conda active (`set_study YOURSTUDY`), do:

    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Then you can run

    python gsuite-downloader.py "Filename pattern in drive"

For the OAuth dance on the Brain Imaging infrastructure, you WILL need X11 
running so the library can run Firefox on the server where it is running. Just 
wait at the "Please visit this URL" prompt and eventually firefox will open.

If you get weird `xdg-open` errors, try `export BROWSER=firefox`.

## Notes

This has only been tested with exporting spreadsheets to `.xslx` so far.

