# This is here so it can be retroactively loaded
from cv2 import *
import numpy as np
import timeit
import tsp


def process(image, logging=0):
    sausages = []
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
            print(f"Sausage: Wid:{height}  \tHei:{width}")
            sausages.append([int(x + (width / 2)), int(y + (height / 2))])
        else:
            print("")
            rectangle(new_image, (x, y), (x + width, y + height), (255, 0, 0), 5)
            print(f"Not sausage: Wid:{height}  \tHei:{width}")

    crosshair_size = 30
    for i in sausages:
        # Draw crosshairs in the centers of the sausages
        line(new_image, (i[0] + crosshair_size, i[1]), (i[0] - crosshair_size, i[1]),
             (0, 0, 255), thickness=3, lineType=8, shift=0)
        line(new_image, (i[0], i[1] + crosshair_size), (i[0], i[1] - crosshair_size),
             (0, 0, 255), thickness=3, lineType=8, shift=0)

    end = timeit.default_timer()
    sausages = []
    print(f"Processing done in: {end - start}")
    return new_image, sausages


def path(image, sausages):
    try:
        sausages.insert(0, [0, 0])
        start = timeit.default_timer()

        shortest, order = tsp.tsp(sausages)
        prev = None
        for cur in order:
            if prev is None:
                prev = cur
            else:
                line(image, (sausages[prev][0], sausages[prev][1]), (sausages[cur][0], sausages[cur][1]),
                     (255, 0, 255), thickness=3, lineType=8, shift=0)
                prev = cur

        print(f"Path found: {shortest}p in order {order}")

        end = timeit.default_timer()
        print(f"Pathing done in: {end - start}")
        return image, order
    except Exception as e:
        print(e)
        return image, []
