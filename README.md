# G-Suite Downloader

A tool for auto-downloading documents from Google Drive, such as a spreadsheet 
people are working on that you would like to sync to a study drive.

## Setup

Based on https://developers.google.com/drive/api/v3/quickstart/python

First, go to the quickstart and enable the Drive API for your wisc.edu Google
account. It will make you pick a name. For OAuth app kind, choose "Desktop 
app". Save the `credentials.json` in this dir.

Save your Client ID and Client Secret somewhere safe, like in a `CLIENT_ID` 
and `CLIENT_SECRET` file that are only readable by people in your study's
raw-data group.

With your conda active (`set_study YOURSTUDY`), do:

    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Then you can run

    python gsuite-downloader.py "Filename pattern in drive"

For the OAuth dance on the Brain Imaging infrastructure, you WILL need X11 
running so the library can run Firefox on the server where it is running. Just 
wait at the "Please visit this URL" prompt and eventually firefox will open.

## Notes

I got as far as `Encountered 403 Forbidden with reason "insufficientPermissions"`
but I'm not sure what permission needs to be granted.

