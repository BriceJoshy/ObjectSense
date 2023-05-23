#  this file contains the basics of requets,url,reponse stuff
#  reading and showing the image from image url usinf requests package

import cv2 as cv
import numpy as np

# package used
import requests


def image_url_display_requests():
    url = r"https://images.wallpapersden.com/image/download/landscape-pixel-art_bGhnaGeUmZqaraWkpJRtZWWta2Vl.jpg"
    # using the .get()  from requests to get the data as bytes and raw i.e without any change
    response = requests.get(url, stream=True).raw
    # .read reads the data into a bytstream and the datatype is changes to uint8
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    #  reading the image as it is without any change
    image = cv.imdecode(image, cv.IMREAD_COLOR)

    cv.imshow("url_image", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
