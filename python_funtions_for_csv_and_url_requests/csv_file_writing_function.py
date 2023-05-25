# This file shows the basics of reading data from the csv file


import csv


def csv_file_reading():
    data = ["hi", "hello", "welcome"]
    with open("output.csv", "w") as file:
        csvfile = csv.writer(file)
        # that returns the reader object that iterates throughout the lines in the specified CSV document.
        csvfile.writerow(data)

        #  i is used to print as elements and not as array
