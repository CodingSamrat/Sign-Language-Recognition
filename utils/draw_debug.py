import copy
import numpy as np
import cv2 as cv


def draw_bounding_rect(use_brect, image, brect, outline_color=(255, 255, 255), pad=6):
    """
    Draw bounding box draw the bounding box around the detected hand(s)

    :param use_brect: bool
    :param image: Debug image
    :param brect: B-Box coordinates
    :param outline_color: Color of the lines
    :return: Debug image
    :param pad: Padding
    """

    if use_brect:
        #: Outer rectangle
        cv.rectangle(
            image,
            (brect[0] - pad, brect[1] - pad),
            (brect[2] + pad, brect[3] + pad),
            outline_color,
            1
        )

    return image


def draw_info_text(image, brect, handedness, hand_sign_text):
    """
    Takes the following params and write information about
    detected hand gesture on the debug image.

    :param image: Debug image
    :param brect: B-Box coordinates
    :param handedness: Detected hand
    :param hand_sign_text: Classified hand sign
    :return: Debug image
    """

    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22), (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    # if hand_sign_text != "":
    #     info_text = info_text + ':' + hand_sign_text

    cv.putText(
        image,
        info_text,
        (brect[0] + 5, brect[1] - 4),
        cv.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1,
        cv.LINE_AA
    )

    return image


def get_result_image():
    """

    :param image:
    :return:
    """
    image = np.ones([200, 400, 3], dtype=np.uint8) * 255

    #: Heading
    cv.putText(image, "Left", (10, 30),
                cv.FONT_HERSHEY_SIMPLEX,
        0.6, (0, 0, 0), 1, cv.LINE_AA
    )

    cv.putText(image, "Right", (210, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        0.6, (0, 0, 0), 1, cv.LINE_AA
    )

    return image


def show_result(image, handedness, hand_sign_text):
    """
    :param hand_sign_text: Detected sign
    :param handedness: Detected hand
    :param image: Result to draw
    :return: Result image
    """

    #: Creating two different copy of image
    left_image, right_image = copy.deepcopy(image), copy.deepcopy(image)

    #: Detecting hand
    hand = handedness.classification[0].label[0:]

    #: Position of text
    position = (00, 00)

    #: Check if hand sign is empty or not
    #: Checking for right hand or left
    if hand_sign_text != "":
        if hand == "Right":
            position = (210, 60)
        elif hand == "Left":
            position = (10, 60)

        cv.putText(
            image,
            hand_sign_text,
            position,
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            1,
            cv.LINE_AA
        )

    return image
