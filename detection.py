import cv2
import mediapipe as mp
import pyautogui 

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_w = 0
index_h = 0
while True:
    _,frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_height,frame_width,_ =  frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            # drawing_utils.draw_landmarks(frame,hand)
            landmarks = hand.landmark
            for id , landmark in enumerate(landmarks):
                
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                
                if id == 8:
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
                    # drawing_utils.draw_landmarks(frame,hand)
                    # print({"x" : x , "y": y})
                    index_w = screen_width/frame_width * x
                    index_h = screen_height/frame_height * y
                    pyautogui.moveTo(index_w,index_h)

                if id == 4:
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
                    # drawing_utils.draw_landmarks(frame,hand)
                    # print({"x" : x , "y": y})
                    thumb_w = screen_width/frame_width * x
                    thumb_h = screen_height/frame_height * y
                    # pyautogui.moveTo(index_w,index_h)

                    if abs(index_h - thumb_h) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)

    cv2.imshow("finger detection",frame)
    cv2.waitKey(1)