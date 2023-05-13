import copy
import csv
from collections import Counter
from collections import deque

import cv2 as cv
import mediapipe as mp
import numpy as np

from utils import get_args
from utils import CvFpsCalc

from utils import draw_landmarks
from utils import draw_bounding_rect
from utils import draw_info_text
from utils import show_result
from utils import get_result_image

from utils import calc_bounding_rect
from utils import calc_landmark_list
from utils import pre_process_landmark

from model import KeyPointClassifier


def main():
    #: -
    #: Getting all arguments
    args = get_args()

    #: cv Capture
    CAP_DEVICE = args.device
    CAP_WIDTH = args.width
    CAP_HEIGHT = args.height

    #: mp Hands
    USE_STATIC_IMAGE_MODE = args.use_static_image_mode
    MAX_NUM_HANDS = args.max_num_hands
    MIN_DETECTION_CONFIDENCE = args.min_detection_confidence
    MIN_TRACKING_CONFIDENCE = args.min_tracking_confidence

    #: Drawing Rectangle
    USE_BRECT = args.use_brect
    RECORD_MODE = args.record_mode

    #: -
    #: Capturing image
    cap = cv.VideoCapture(CAP_DEVICE)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)

    #: -
    #: Setup hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=USE_STATIC_IMAGE_MODE,
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE
    )

    #: -
    #: Load Model
    keypoint_classifier = KeyPointClassifier()

    #: Loading labels
    keypoint_labels_file = "model/label.csv"
    with open(keypoint_labels_file, encoding="utf-8-sig") as f:
        key_points = csv.reader(f)
        keypoint_classifier_labels = [row[0] for row in key_points]

    #: -
    #: FPS Measurement
    cv_fps = CvFpsCalc(buffer_len=10)

    #: -
    #: Coordinate history or Finger gesture history
    history_length = 16
    finger_gesture_history = deque(maxlen=history_length)

    #: -
    #: Main Loop Start Here...
    while True:
        #: FPS of open cv frame or window
        fps = cv_fps.get()

        #: Setup Quit key for program
        key = cv.waitKey(10)
        if key == 27:   # ESC key
            break

        #: Camera capture
        ret, image = cap.read()
        if not ret:
            break

        #: Flip Image for mirror display
        image = cv.flip(image, 1)
        debug_image = copy.deepcopy(image)
        result_image = get_result_image()

        #: Converting to RBG from BGR
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)  #: Hand's landmarks
        image.flags.writeable = True

        #: Start Detection
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

                #: Calculate  BoundingBox
                use_brect = True
                brect = calc_bounding_rect(debug_image, hand_landmarks)

                #: Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                #: Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                #: -
                #: Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                hand_sign_text = keypoint_classifier_labels[hand_sign_id]
                # print(hand_sign_text)
                result_image = show_result(result_image, handedness, hand_sign_text)

                #: -
                #: Drawing debug info
                debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(
                    debug_image,
                    brect,
                    handedness,
                    hand_sign_text
                    # "Demo"
                )

        cv.imshow("Left", result_image)

        cv.imshow("Sing Language Recognition", debug_image)

    cap.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    main()
