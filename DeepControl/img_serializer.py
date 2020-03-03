"""
Serializes and deserializes images 
after converted to the DataFrame format
"""
import cv2
import numpy as np
import json

# Deserializes image from data frame dump
def deserialize_image(df_dump, width=148, height=102, depth=3, config='/content/gdrive/My Drive/racecar/settings.json'):
    # [1:-1] is used to remove '[' and ']' from dataframe string
    df_dump = np.fromstring(df_dump[1:-1], sep=', ', dtype='uint8')
    #print(df_dump.shape)
    with open(config) as d:
        SETTINGS = json.load(d)
    width=SETTINGS['width']
    height=SETTINGS['height']
    depth=SETTINGS['depth']
    df_dump = np.resize(df_dump, (height, width, depth))

    return df_dump

