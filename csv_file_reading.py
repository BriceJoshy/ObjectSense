# This file shows the basics of reading data from the csv file


import csv

# The ‘with’ keyword is used along with the open() method as it simplifies exception handling and automatically closes the CSV file.
# At first, the CSV file is opened using the open() method in ‘r’ mode(specifies read mode while opening a file)
# which returns the file object then it is read by using the reader() method of CSV module
with open("images.csv", mode="r") as file:
    csvfile = csv.reader(file)
    # that returns the reader object that iterates throughout the lines in the specified CSV document.
    for lines in csvfile:
        print(lines)
