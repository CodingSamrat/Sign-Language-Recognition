import cv2 as cv
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

background = cv.imread("resources/background.png")
while True:
  
  suc, frame = cap.read()
  if not suc: break
  background[170:170+480, 50:50+640] = frame
  
  # cv.imshow("n", frame)
  cv.imshow("Sign Language Recognition", background)
  
  key = cv.waitKey(10)
  if key == 27: break