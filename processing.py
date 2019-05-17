# This is here so it can be retroactively loaded
from cv2 import *
import timeit
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
import heapq
from tsp_solver.greedy import solve_tsp
from copy import deepcopy


def process(image):
    start = timeit.default_timer()
    new_image = inRange(image, (0, 0, 150), (255, 255, 245))  # Value thresholding is the easiest first step
    new_image = medianBlur(new_image, 13)
    new_image = morphologyEx(new_image, MORPH_OPEN, np.ones((13, 10)), iterations=2)
    new_image = morphologyEx(new_image, MORPH_CLOSE, np.ones((13, 10)), iterations=5)

    contours, hierarchy = findContours(new_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    new_image = cvtColor(image, COLOR_BGR2RGB)
    # new_image = drawContours(new_image, contours, -1, (0, 255, 0), 3)
    sausages = []
    for i in contours:  # Draw rectangles
        # Check if box is sausage shape/size
        x, y, width, height = boundingRect(i)

        if height > 400 and width < 200:
            rectangle(new_image, (x, y), (x + width, y + height), (0, 255, 0), 5)
            print(f"Sausage: Wid:{height}  \tHei:{width} \t {x} {y}")
            sausages.append([int(x + (width / 2)), int(y + (height / 2))])
        else:
            rectangle(new_image, (x, y), (x + width, y + height), (255, 0, 0), 5)
            # print(f"Not sausage: Wid:{height}  \tHei:{width} \t {x} {y}")

    crosshair_size = 30
    for i in sausages:
        # Draw crosshairs in the centers of the sausages
        line(new_image, (i[0] + crosshair_size, i[1]), (i[0] - crosshair_size, i[1]),
             (0, 0, 255), thickness=3, lineType=8, shift=0)
        line(new_image, (i[0], i[1] + crosshair_size), (i[0], i[1] - crosshair_size),
             (0, 0, 255), thickness=3, lineType=8, shift=0)

        putText(new_image, f"{i[0]}, {i[1]}", (i[0] + 20, i[1] + 100), FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, LINE_AA)

    end = timeit.default_timer()
    print(f"Found the sausage in: {end - start}")
    return new_image, sausages


def path(image, sausages):
    sausages.insert(0, [0, 0])
    print(sausages)
    dist = pd.DataFrame(distance_matrix(sausages, sausages))
    start = timeit.default_timer()
    order = solve_tsp(dist.values)
    path_length, order = recur_greedy(list(range(len(sausages))), dist, 1, 0)
    end = timeit.default_timer()

    path_length = 0
    prev = None
    for cur in order:

        if prev is None:
            prev = cur
        else:
            path_length += dist.values[cur][prev]
            line(image, (sausages[prev][0], sausages[prev][1]), (sausages[cur][0], sausages[cur][1]),
                 (0, 255, 0), thickness=3, lineType=8, shift=0)
            prev = cur

    putText(image, f"Total distance: {path_length:.2f}px", (int(image.shape[1]*0.6), int(image.shape[0]*0.9)),
            FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, LINE_AA)

    print(f"Efficiently touched the sausages in: {end - start}. Shortest path: {path_length}")
    return image, order


""" Calculates the shortest path using {iterations} many nearest neighbours. Starts at {prev} index
points      - An array of the indexes of each point (use {list(range( len(points) ))})
dist_mat    - the square distance matrix
iterations  - How many nearest neighbours to check
origin      - The starting point
prev        - Stores the point that the function came from
cur_len     - Stores the currently used length 
"""


def recur_greedy(points, dist_mat, iterations, origin, prev=None, cur_len=0):
    # If it's the first loop, update prev
    prev = origin if prev is None else prev

    # Remove the previous point from the array to only look forward
    points.remove(prev)

    # Check if at the end of a path
    if not len(points):
        return cur_len, [origin]

    # Find the smallest {iterations} distances
    dist_attached = heapq.nsmallest(iterations, [[i, points[cnt]] for cnt, i in enumerate(dist_mat[prev][points])])

    # Call the function and store all the resulting distances and paths
    item = [[recur_greedy(deepcopy(points), dist_mat, iterations, origin, prev=deepcopy(i[1]),
                          cur_len=cur_len + i[0]), i[1]] for i in dist_attached]

    # Find the shortest path, then return it to pas it to the next level up
    best = heapq.nsmallest(1, item)[0]
    best[0][1].insert(1, best[1])  # Add the new point into the path

    # Return the data to the next level up
    return best[0], best[0][1]
