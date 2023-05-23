#  this file shows how to read and show an image from an url in the csv file

import cv2 as cv
import numpy as np
import requests
import csv

with open("images.csv", mode="r") as file:
    csvfile = csv.reader(file)
    # that returns the reader object that iterates throughout the lines in the specified CSV document.
    i = 0
    index = 0
    url = []
    for lines in list(csvfile):
        if i < len(list(csvfile)):
            url = lines
            # using the .get()  from requests to get the data as bytes and raw i.e without any change
            response = requests.get(url[i], stream=True).raw
            # .read reads the data into a bytstream and the datatype is changes to uint8
            image = np.asarray(bytearray(response.read()), dtype="uint8")
            #  reading the image as it is without any change
            image = cv.imdecode(image, cv.IMREAD_COLOR)
            i = i + 1
            print(i)
            cv.imshow(f"url_image_{index}", image)
            index += 1
            cv.waitKey(0)
            cv.destroyAllWindows()
