from tkinter import W
import cv2
import mediapipe as mp

from websocket import create_connection
import asyncio
import json
ws = create_connection("ws://localhost:4041")
ws.send(json.dumps({"type": "detection", "message": "connected"}))
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
index_w = 0
index_h = 0

check_t = False

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        check_t = True
        for hand in hands:
            # drawing_utils.draw_landmarks(frame,hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):

                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y),
                               radius=10, color=(0, 255, 255))
                    ws.send(json.dumps(
                        {"type": "detection", "message": "send_data", "x": x, "y": y}))

                    # drawing_utils.draw_landmarks(frame,hand)
                    # print({"x" : x , "y": y})
                    # 480
                    # 640
                    # index_w = screen_width/frame_width * x
                    # index_h = screen_height/frame_height * y

    else:
        if check_t:
            ws.send(json.dumps({"type": "detection", "message": "no_hand"}))
            check_t = False
        else:
            pass

    cv2.imshow("finger detection", frame)
    cv2.waitKey(1)
