#  this file shows how to read and show an image from an url in the csv file

import cv2 as cv
import numpy as np
import requests
import csv


image_list_from_csv = []
with open("images.csv", newline="", mode="r") as file:
    csvfile = csv.reader(file)
    # that returns the reader object that iterates throughout the lines in the specified CSV document.
    for row in csvfile:
        image_list_from_csv.append(row[0])
    print(image_list_from_csv)
