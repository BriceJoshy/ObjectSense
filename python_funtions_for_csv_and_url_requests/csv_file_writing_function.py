# This file shows the basics of reading data from the csv file


import csv


def csv_file_reading():
    data = ["hi", "hello", "welcome"]
    with open("output", mode="w", newline="") as file:
        csvfile = csv.writer(file, lineterminator="\n")
        # that returns the reader object that iterates throughout the lines in the specified CSV document.
        for lines in data:
            csvfile.writerows([lines])

        #  i is used to print as elements and not as array
