import pandas as pd
import requests
import json
import os

# Change to appropriate directory
#os.chdir(r'C:\Users\Daniel\Desktop\Python Projects\Twitch Project\Twitch_data\ICWSM19_data')

# Returns a list of all global Twitch emotes.

global_response = requests.get('https://api.twitch.tv/kraken/chat/emoticon_images?emotesets=0', headers={
                               'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': '4f7ls48eaq2lly25dyuiead8o5ydev'})
json_data_global = json.loads(global_response.text)
global_emotes = json_data_global.get('emoticon_sets').get('0')
X_global = [i.get("code") for i in global_emotes]


# Finds channel id from dataframe

def streamer_df(streamer):
    df = pd.read_pickle(streamer+'.pkl')
    return df


def channel_id(streamer):
    df = streamer_df(streamer)
    return str(df['channel_id'].iloc[0])

# Returns global emotes and channel specific emotes together in a list


def streamer_emotes(streamer):
    response = requests.get('https://api.twitchemotes.com/api/v4/channels/' + channel_id(streamer))
    json_data = json.loads(response.text)
    emotes = json_data.get("emotes")
    X = [i.get("code") for i in emotes]

    return X


def global_streamer_emotes(streamer):
    return X_global + streamer_emotes(streamer)
