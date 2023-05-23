#  this file shows how to read and show an image from an url in the csv file

import cv2 as cv
import numpy as np
import requests
import csv

#  creating a empty list for storing the rows of the single column of the csv file
image_from_csv_list = []
#  setting the indexx for the image name so as to prevent the images from crashing while 'imshow' because of the same name
index = 0
with open("images.csv", mode="r") as file:
    csvfile = csv.reader(file)
    # that returns the reader object that iterates throughout the lines in the specified CSV document.
    # for every line adding the column[0] as the list row for the empty list created above
    for lines in csvfile:
        image_from_csv_list.append(lines[0])

    print(image_from_csv_list)
    for i in range(0, len(image_from_csv_list)):
        url = image_from_csv_list[i]
        # using the .get()  from requests to get the data as bytes and raw i.e without any change
        response = requests.get(url, stream=True).raw
        # .read reads the data into a bytstream and the datatype is changes to uint8
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        #  reading the image as it is without any change
        image = cv.imdecode(image, cv.IMREAD_COLOR)
        cv.imshow(f"url_image_{index}", image)
        index += 1

    cv.waitKey(0)
    cv.destroyAllWindows()
