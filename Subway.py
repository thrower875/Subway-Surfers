import cv2
import mediapipe as mp
import pyautogui
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
tipIds = [4, 8, 12, 16, 20]
game_started = 1
charac_pos = [0,1,0]
index_pos = 1
fixedx = None
fixedy = None
rec = None
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5,upper_body_only=True) as holistic:
        while True:
            success, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (440,330))
            height, width, channel = frame.shape
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_holistic = holistic.process(img)
            results_hands = hands.process(img)
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            width_hf = int(width/2)
            height_hf = int(height/2)
            # Extracting Shoulder Landmarks
            if results_holistic.pose_landmarks:
                right_x = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * width)-7
                right_y = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * height)
                # cv2.circle(img, (right_x, right_y), 5, (0, 0, 0), 2)
                left_x = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * width)+7
                left_y = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * height)
                # cv2.circle(img, (left_x, left_y), 5, (0, 0, 0), 2)
                # cv2.line(img, (left_x,left_y), (right_x,right_y), (255, 0, 255), 2)
                mid_x = left_x + int(abs(right_x - left_x) / 2)
                mid_y = int(abs(right_y + left_y) / 2)
                # cv2.circle(img, (mid_x, mid_y), 2, (255, 255, 0), 2)
                if rec != None:
                    # Sideways movement command
                    if right_x < width_hf and index_pos > 0 and charac_pos[index_pos-1] == 0:
                        charac_pos[index_pos] = 0
                        charac_pos[index_pos-1] = 1
                        pyautogui.press('left')
                        index_pos -= 1
                        print("Left key")
                        print(charac_pos)
                    if left_x > width_hf and index_pos < 2 and charac_pos[index_pos+1] == 0:
                        print("Right key")
                        charac_pos[index_pos] = 0
                        charac_pos[index_pos+1] = 1
                        pyautogui.press('right')
                        index_pos += 1
                        print(charac_pos)
                    if right_x > width_hf and left_x < width_hf and index_pos == 0:
                        charac_pos[index_pos] = 0
                        charac_pos[index_pos +1] = 1
                        index_pos += 1
                        pyautogui.press('right')
                        print(charac_pos)
                        print('left to center')
                    if right_x > width_hf and left_x < width_hf and index_pos == 2:
                        charac_pos[index_pos] = 0
                        charac_pos[index_pos -1] = 1
                        index_pos -= 1
                        pyautogui.press('left')
                        print('right to center')
                        print(charac_pos)

            hand_cor_list_right = []
            hand_cor_list_left = []
            hand_type1 = None
            hand_type2 = None
            fingers_right = []
            fingers_left = []
            # Detection of both hands and extracting both hand landmarks
            try:
                hand_type1 = results_hands.multi_handedness[0].classification[0].label
                hand_type2 = results_hands.multi_handedness[1].classification[0].label
                for hand_no, hand_landmarks in enumerate(results_hands.multi_hand_landmarks):
                    if hand_no == 0:
                        if hand_type1 == 'Left':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * width), int(lm.y * height)
                                # cv2.circle(img, (cx,cy),2, (100,255,100),2)
                                hand_cor_list_left.append([id,cx,cy])
                        elif hand_type1 == 'Right':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * width), int(lm.y * height)
                                # cv2.circle(img, (cx,cy),2, (100,255,100),2)
                                hand_cor_list_right.append([id,cx,cy])
                    if hand_no == 1:
                        if hand_type2 == 'Left':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * width), int(lm.y * height)
                                # cv2.circle(img, (cx,cy),2, (100,255,100),2)
                                hand_cor_list_left.append([id,cx,cy])
                        elif hand_type2 == 'Right':
                            for id, lm in enumerate(hand_landmarks.landmark):
                                cx, cy = int(lm.x * width), int(lm.y * height)
                                # cv2.circle(img, (cx,cy),2, (100,255,100),2)
                                hand_cor_list_right.append([id,cx,cy])
                if hand_cor_list_right != []:
                    # Right Hand Thumb open Detection
                    if hand_cor_list_right[tipIds[0]][1] < hand_cor_list_right[tipIds[0] - 1][1]:
                        fingers_right.append(1)
                    else:
                        fingers_right.append(0)

                    # Right Hand 4 Fingers open Detection
                    for id in range(1, 5):
                        if hand_cor_list_right[tipIds[id]][2] < hand_cor_list_right[tipIds[id] - 2][2]:
                            fingers_right.append(1)
                        else:
                            fingers_right.append(0)
                    totalFingers_right = fingers_right.count(1)

                if hand_cor_list_left != []:
                    # Left hand Thumb open detection
                    if hand_cor_list_left[tipIds[0]][1] > hand_cor_list_left[tipIds[0] - 1][1]:
                        fingers_left.append(1)
                    else:
                        fingers_left.append(0)

                    # Left Hand 4 Fingers open Detection
                    for id in range(1, 5):
                        if hand_cor_list_left[tipIds[id]][2] < hand_cor_list_left[tipIds[id] - 2][2]:
                            fingers_left.append(1)
                        else:
                            fingers_left.append(0)
                    totalFingers_left = fingers_left.count(1)
            except:
                pass
            # Command to Start the game
            if fingers_right.count(1) == 2 and fingers_left.count(1) == 2 and fingers_right[1] == 1 and fingers_right[2] == 1 and fingers_left[1] == 1 and fingers_left[1] == 1:
                fixedx = left_x + int(abs(right_x - left_x) / 2)
                fixedy = int(abs(right_y + left_y) / 2)
                rec = 35
                pyautogui.press('space')

            # Up and Down command
            if fixedy is not None:
                if (mid_y- fixedy) <= -24:
                    pyautogui.press('up')
                    print('jump')
                elif (mid_y - fixedy) >= 40:
                    pyautogui.press('down')
                    print('down')
            center_arrow = 10
            cv2.circle(img,(width_hf,height_hf),2,(0,255,255),2)
            cv2.line(img,(width_hf,height_hf -center_arrow),(width_hf,height_hf+center_arrow),(0,255,0),2)
            cv2.line(img,(width_hf -center_arrow,height_hf),(width_hf+center_arrow,height_hf),(0,255,0),2)
            # Lines to be crossed to detect up and down movement
            # if rec is not None:
            #     cv2.line(img, (0, fixedy), (width, fixedy), (0, 0, 0), 2)
            #     cv2.line(img, (0, fixedy - 24), (width, fixedy - 24), (0, 0, 0), 2)
            #     cv2.line(img, (0, fixedy + rec), (width, fixedy + rec), (0, 0, 0), 2)

            cv2.imshow('Subway Surfers',img)
            cv2.waitKey(1)

