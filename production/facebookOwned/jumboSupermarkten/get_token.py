import requests
import json
import io
import os

stored_file_path = "access_data.json"
stored_app_id = "189107884825866" 
stored_app_secret = "75b2266497016d64a0efdde0dd0d2541"

def accessDataCheck(access_data):
    if os.path.isfile(access_data) and os.access(access_data, os.R_OK):
        # checks if file exists
        print ("File exists and is readable")
        
        #Open access_data file
        with open(access_data, 'r') as fp:
            fb_data = json.load(fp)

        stored_app_id = fb_data["app_id"]
        stored_app_secret = fb_data["app_secret"]
    else:
        print ("Either file is missing or is not readable, creating file...")

def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    req = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print req.text #to test what the FB api responded with    
    response_token = req.json()['access_token']

    #data to be stored
    fb_data = {
        "app_id": stored_app_id,
        "app_secret": stored_app_secret,
        "app_access_token": response_token,
    }

    with open("access_data.json", "w") as fp:
        json.dump(fb_data,fp)
        print("data stored!")

accessDataCheck(stored_file_path)
get_fb_token(stored_app_id,stored_app_secret)