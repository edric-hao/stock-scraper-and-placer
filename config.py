import csv

def get(directory):
    with open('config.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0]==directory:
                return row[1]