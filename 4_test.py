import cv2
import math
import numpy as np
import mediapipe as mp
from keras.models import load_model

# Loading Model
model = load_model('model/model-1.h5')

capture = cv2.VideoCapture(0)
imgSize = 300
imgTestSize = 64

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9)

while True:
    success, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (0, 0), fx=0.65, fy=0.65, interpolation=cv2.INTER_CUBIC)
    img_croped = frame.copy()
    img_height, img_width, _ = frame.shape

    if not success:
        continue

    ############ Logic Started ################
    frame.flags.writeable = False
    img_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_RGB)  # Takes RGB

    img_RGB.flags.writeable = True
    img_BGR = cv2.cvtColor(img_RGB, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            #: Draw Landmarks & Skeleton
            # mp_drawing.draw_landmarks(
            #     img_BGR,
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style()
            # )

            # Drawing BoundingBox
            x_pos = []
            y_pos = []

            for i in mp_hands.HandLandmark:
                # Finding x & y Landmarks
                x = hand_landmarks.landmark[i.value].x * img_width
                y = hand_landmarks.landmark[i.value].y * img_height

                # Appending Landmarks into Separate List
                x_pos.append(x)
                y_pos.append(y)

                offset = 25
                # min-x
                x_min = int(min(x_pos)) - offset
                x_max = int(max(x_pos)) + offset

                # min-y
                y_min = int(min(y_pos)) - offset
                y_max = int(max(y_pos)) + offset

            start_pos = (x_min, y_min)
            end_pos = (x_max, y_max)
            color = (255, 0, 0)
            thikness = 2

            center_x = int((x_max + x_min) / 2)
            center_y = int((y_max + y_min) / 2)
            halfofimg = int(imgSize / 2)

            img_BGR = cv2.rectangle(img_BGR, start_pos, end_pos, color, thikness)
            img_croped = img_BGR[y_min + thikness: y_max - thikness, x_min + thikness: x_max - thikness]

            # Resizing Hand image
            img_bg = np.ones([imgSize, imgSize, 3], dtype=np.uint8) * 255

            h = (y_max - thikness) - (y_min + thikness)
            w = (x_max - thikness) - (x_min + thikness)

            aspectRatio = h / w
            try:
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(img_croped, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    img_bg[:, wGap: wGap + wCal] = imgResize


                elif aspectRatio < 1:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(img_croped, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    img_bg[hGap: hGap + hCal, :] = imgResize
            except Exception as e:
                print(e)

            img_bg = cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)
            img_final = cv2.resize(img_bg, (imgTestSize, imgTestSize))
            img_flatten = img_final.flatten()
            img_array = np.array(img_flatten)
            img_array = np.expand_dims(img_array, axis=0)
            img_normal = img_array / 255

            y_predicted = model.predict(img_normal)
            y_predicted_labels = np.argmax(y_predicted[0])

            letters = ["A", "B", "C", "D", "E"]

            # cv2.imshow("Final Image", final_img)

            try:
                print(letters[y_predicted_labels])
            except:
                pass

            cropped_window = "Cropped Image"
            cv2.imshow(cropped_window, img_bg)
            cv2.setWindowProperty(cropped_window, cv2.WND_PROP_TOPMOST, 1)

    ############### Logic End #################

    main_window = "Main Frame"
    cv2.imshow(main_window, img_BGR)
    cv2.setWindowProperty(main_window, cv2.WND_PROP_TOPMOST, 1)

    if cv2.waitKey(1) == ord('c'):
        break

capture.release()
cv2.destroyAllWindows()
