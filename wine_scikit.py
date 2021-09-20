import csv
import math
from collections import Counter
import numpy as np
import random

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


filename = "datasets/winequality-red.csv"

# initializing the titles and rows list
fields = []
total_set = [] #first half training, second half testing
normalized_set = []
qualities = []

def correlate_freqs(v1,v2):

    num_correct = 0

    for i in range(len(v1)):
        
        if (v1[i] == v2[i]):
            num_correct += 1
            # print("YAY")

    return num_correct


def normalization(array):
    # maximum = max(array)
    # minimum = min(array)
    normalized_list = []

    #print(total_set)

    maximum = np.maximum.reduce(total_set)
    minimum = np.minimum.reduce(total_set)

    for i in range(len(array)):
        e = array[i]

        normalized_list.append((e - minimum[i]) / (maximum[i] - minimum[i]))

    return normalized_list

#https://www.geeksforgeeks.org/working-csv-files-python/
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
      
    # extracting field names through first row
    fields = next(csvreader)
  
    shuffled = []

    # extracting each data row one by one
    for row in csvreader:

        shuffled.append(row)

    random.seed(4)

    random.shuffle(shuffled)


    for row in shuffled:
        spliced_row = row[0].split(";")
        floated_row = [float(i) for i in spliced_row]
        qualities.append(floated_row.pop())
        total_set.append(floated_row)

    # print(total_set)

    for row in range(len(total_set)):
        #print(total_set[row])
        normalized_set.append(normalization(total_set[row]))


mid = len(normalized_set)//2
k = int(math.pow(len(qualities[:mid]), 1/2))

# print(normalized_set)

#W/O Weights

X_train, X_test, y_train, y_test = train_test_split(normalized_set, qualities, test_size=0.5, random_state=1)

# Create KNN classifier
knn_unweighted = KNeighborsClassifier(n_neighbors = k, weights='uniform')
# Fit the classifier to the data
knn_unweighted.fit(X_train,y_train)

print(knn_unweighted.score(X_test, y_test))


X_train_w, X_test_w, y_train_w, y_test_w = train_test_split(normalized_set, qualities, test_size=0.5, random_state=1)

knn_weighted = KNeighborsClassifier(n_neighbors = k, weights='distance')
# Fit the classifier to the data
knn_weighted.fit(X_train_w,y_train_w)

print(knn_weighted.score(X_test_w, y_test_w))










