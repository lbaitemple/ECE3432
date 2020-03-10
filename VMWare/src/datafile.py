import pandas as pd
import numpy as np
import json
import cv2
import sys

def deserialize_image(df_dump, config='settings.json'):
    # [1:-1] is used to remove '[' and ']' from dataframe string
    df_dump = np.fromstring(df_dump[1:-1], sep=', ', dtype='uint8')
   # print(df_dump.shape)
    with open(config) as d:
        SETTINGS = json.load(d)

    width=SETTINGS['width']
    height=SETTINGS['height']
    depth=SETTINGS['depth']
    df_dump = np.resize(df_dump, (height, width, depth))

    return df_dump

if __name__ == "__main__":

    data = pd.read_csv(sys.argv[1])

    for i in range(len(data)):
        cur_img = data['image'][i]
        cur_throttle = int(data['servo'][i]*100)
        print("cur_throttle:",cur_throttle)

    #    cur_motor = float(data['motor'][i])
        cur_img_array = deserialize_image(cur_img)

    #   print(len(cur_img_array))
        cur_img_array = cv2.resize(cur_img_array, (640, 320), interpolation=cv2.INTER_CUBIC)
        cv2.line(cur_img_array, (240, 300), (240 - 20*(15 - cur_throttle), 200), (255, 0, 0), 3)
        cv2.imshow('picture {}'.format(i), cv2.cvtColor(cur_img_array, cv2.COLOR_RGB2BGR))

        if (cv2.waitKey(0) & 0xFF == ord('q')):
            break
