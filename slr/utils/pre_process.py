import copy
import itertools
from typing import List

import numpy as np
import cv2 as cv


def calc_bounding_rect(image, landmarks) -> List:
    """
    Takes Captures image and 3D coordinates of hand landmarks
    And Calculate the aria bounding box around the hand

    :param image: Captured Image
    :param landmarks: List of Hand's Landmarks
    :return: List of coordinate of bounding-box
    """

    #: Getting image width & height
    image_width = image.shape[1]
    image_height = image.shape[0]

    #: Creating empty np array
    landmark_array = np.empty((0, 2), int)

    #: Iterating over all the landmarks
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width -1)
        landmark_y = min(int(landmark.y * image_height), image_height -1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x+w, y+h]


def calc_landmark_list(image, landmarks) -> List:
    """
    Takes Captures image and 3D coordinates of hand landmarks
    And Calculate the Key-points of the hand landmarks

    :param image: Captured Image
    :param landmarks: Landmarks
    :return: List of Key-points
    """

    #: Getting image width & height
    image_width = image.shape[1]
    image_height = image.shape[0]

    landmark_point = []

    #: Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        #: landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list) -> List:
    """
    Pre Processing Landmark takes the list of calculated landmarks
    to calculate relative coordinates of all landmarks.

    For this it goes through some step:

    i. Making a deep-copy the list;
    ii. Set 0th landmark _(Wrist)_ as root (0, 0)
    iii. Then calculate other landmark's relative coordinate
    iv. Finally, normalized them all and return as list

    :param landmark_list: Calculated Landmarks
    :return: List of relative coordinates
    """

    temp_landmark_list = copy.deepcopy(landmark_list)

    #: Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        #: Overriding coordinates
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    #: Convert into a one-dimensional list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

    #: Normalization (-1 to 1)
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


