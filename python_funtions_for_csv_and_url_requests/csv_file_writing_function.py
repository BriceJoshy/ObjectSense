#  this file shows the python function to write into a csv file
#  used for  storing the images after the images are read from the origianl csv file for background removal
#  and contour cropping then saved as the url in a seperate csv file for storage


import csv

row = ["name_of_image"]
with open("output.csv", mode="w", newline="") as file:
    writter = csv.writer(file)
    writter.writerow(row)
