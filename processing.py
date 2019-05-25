# This is here so it can be retroactively loaded
import cv2

def process(image):
    print("Hi")
    box_image = image

    frame_hsl = cv2.cvtColor(box_image, cv2.COLOR_BGR2HLS)
    frame_threshold = cv2.inRange(frame_hsl, (0, 0, 136), (255, 255, 221))

    final_image = cv2.cvtColor(frame_threshold, cv2.COLOR_HSL2BGR)  # done when licence plate has been found
    box_image = final_image

    lic_image = image
    return box_image, lic_image
