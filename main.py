#!/usr/bin/python3

import random

import pandas as pd # pip3 install pandas
import numpy as np # pip3 install numpy
from sklearn.neighbors import DistanceMetric # pip3 install scikit-learn

def to_distance_matrix(lat, lon):
    """
    Creates a distance matrix in kilometers from coordinates given as latitude and longitude pairs
    """
    lat, lon = np.radians(lat), np.radians(lon)
    dist = DistanceMetric.get_metric('haversine')
    return dist.pairwise(np.column_stack((lat, lon))) * 6373 # factor to convert radians into kilometers

def random_insertion(adjacency_matrix, repeat):
    """
    Repeats the random insertion algorithm <repeat> times and returns the best (shortest) path found.
    """
    # keeps track of the best path of all iterations of the random insertion algorithm
    best_path, best_path_distance = [], float('inf')
    for _ in range(repeat):
        available = list(range(1, len(adjacency_matrix)))
        # randomly pick two cities to start with
        path = [pop_random(available), pop_random(available)]
        while len(available) > 0:
            # randomly select next city to insert
            to_insert = pop_random(available)
            # keeps track of the path with the best position to insert the next city
            best_new_path, best_new_path_distance = [], float('inf')
            # insert new city in every possible position an pick the shortest path
            for i in range(len(path)):
                path_to_compare = path.copy()
                path_to_compare.insert(i, to_insert)
                if (distance := distance_of_path(path_to_compare, adjacency_matrix)) < best_new_path_distance:
                    best_new_path, best_new_path_distance = path_to_compare, distance
            path = best_new_path
        # update the global best path if the path of this iteration is shorter than the global one
        if (path_distance := distance_of_path(path, adjacency_matrix)) < best_path_distance:
            best_path, best_path_distance = path, path_distance
    return [0, *best_path, 0], best_path_distance

def distance_of_path(path, adjacency_matrix):
    """
    Calculates the travel distance of the given path.
    """
    dist = adjacency_matrix[0, path[0]] # distance from start (Ismaning) to first city in path
    for i in range(len(path)-1):
        dist += adjacency_matrix[path[i], path[i+1]]
    dist += adjacency_matrix[path[-1], 0] # add distance from last city in path to the end (Ismaning)
    return dist

def pop_random(lst):
    """
    Pops a random element of the given list and returns it.
    """
    return lst.pop(random.randrange(len(lst)))

df = pd.read_csv('./msg_standorte_deutschland.csv')

# distance matrix => weighted adjacency matrix of a graph
adjacency_matrix = to_distance_matrix(df['Breitengrad'], df['Längengrad'])

path, distance = random_insertion(adjacency_matrix, 1000)
print(f'Entfernung: {np.round(distance, 1)} km')
for city_index in path:
    print(df.iloc[city_index, 1])
