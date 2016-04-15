"""
Doing basic data processing
of Yahoo! music rating data.
"""
import csv
from sys import argv
if __name__ == '__main__':
    file_name = argv[1]
    all_ratings = {}
    with open(file_name, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t')
        ctr = 0
        for row in csv_reader:
            nums = list(map(int, row))
            all_ratings.append(nums)
            ctr += 1
            if(ctr % 1000000 == 0):
                print('ctr %d'%(ctr))
    print('total of %d rows'%(ctr))
