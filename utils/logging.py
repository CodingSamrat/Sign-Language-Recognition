import csv
import cv2 as cv


def log_keypoints(key, landmark_list):
    """

    :param key: Keyboard key (latter)
    :param landmark_list: Preprocessed landmark list
    :return: None
    """

    csv_path = 'model/keypoint.csv'
    index = -1
    if 65 <= key <= 90 or 97 <= key <= 122:

        #: Calculating index of letters
        if 65 <= key <= 90:
            index = key - 65
        elif 97 <= key <= 122:
            index = key - 97

        print(index)

        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([index, *landmark_list])

    return


def _get_alphabet_index(key):
    """

    :param key: Keyboard key (latter)
    :return: Index of alphabate
    """
    cap_ascii_list = [
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
        78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90
    ]
    sm_ascii_list = [
        97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
        110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122
    ]

    index = 0
    return index


def get_mode(key, _mode):
    """
    :param key: Pressed key
    :param mode: Mode of program
    :return: mode
    """
    mode = _mode
    if key == 48:
        mode = 0
    elif key == 49:
        mode = 1

    return mode
