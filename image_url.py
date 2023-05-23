#  this file contains the basics of requets,url,reponse stuff
#  reading and showing the image from image url usinf requests package

import cv2 as cv
import numpy as np
import requests

url = r"https://images.wallpapersden.com/image/download/landscape-pixel-art_bGhnaGeUmZqaraWkpJRtZWWta2Vl.jpg"
response = requests.get(url, stream=True).raw
image = np.asarray(bytearray(response.read()), dtype="uint8")
image = cv.imdecode(image, cv.IMREAD_COLOR)

cv.imshow("url_image", image)
cv.waitKey(0)
cv.destroyAllWindows()
