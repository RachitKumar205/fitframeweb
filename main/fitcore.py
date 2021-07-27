import gzip

import cv2
import base64
import numpy as np
import mediapipe as mp
from .models import *
from django.contrib.auth.models import User

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose



def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def from_b64(uri):
    '''
        Convert from b64 uri to OpenCV image
        Sample input: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    encoded_data = uri.split(',')[1]
    data = base64.b64decode(encoded_data)
    np_arr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


def gzip_zip(content):
    """
         gzip compresses data
         : Param content: To compress objects
         : Return: [0, 1]: 0: to be compressed; 1: After compression
    """
    bytes_com = gzip.compress(str(content))
    return bytes_com

def to_b64(img):
    '''
        Convert from OpenCV image to b64 uri
        Sample output: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    _, buffer = cv2.imencode('.jpg', img)
    uri = base64.b64encode(buffer).decode('utf-8')
    return f'data:image/jpg;base64,{uri}'


def pose_gen(frame):
    pnum = Choice.objects.get(name=User.username)
    pchosen = Pose.objects.get(id=pnum.number)
    counter = 0
    stage = None
    fo = cv2.FONT_HERSHEY_SIMPLEX
    co1 = (0, 255, 0)
    co2 = (0, 0, 255)
    x = 1  # random variable
    er = 10  # error percent
    r = 10  # radius of circle
    rid = 1  # aasan number

    ls1 = int(pchosen.angle1)
    rs1 = int(pchosen.angle2)
    lh1 = int(pchosen.angle3)
    rh1 = int(pchosen.angle4)
    lk1 = int(pchosen.angle5)
    rk1 = int(pchosen.angle6)


    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates
        shoulder_L = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow_L = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist_L = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        shoulder_R = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow_R = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist_R = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]
        hip_R = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]
        hip_L = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
        knee_R = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y]
        knee_L = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
        ankle_R = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y]
        ankle_L = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]

        # Calculate angle
        angle_bshoul_L = calculate_angle(shoulder_R, shoulder_L, elbow_L)
        angle_bshoul_R = calculate_angle(shoulder_L, shoulder_R, elbow_R)
        angle_ashoul_R = calculate_angle(elbow_R, shoulder_R, hip_R)
        angle_ashoul_L = calculate_angle(elbow_L, shoulder_L, hip_L)
        angle_ahip_L = calculate_angle(shoulder_L, hip_L, knee_L)
        angle_ahip_R = calculate_angle(shoulder_R, hip_R, knee_R)
        angle_aknee_L = calculate_angle(hip_L, knee_L, ankle_L)
        angle_aknee_R = calculate_angle(hip_R, knee_R, ankle_R)

        # Visualize angle
        cv2.putText(image, str(angle_ashoul_L),
                    tuple(np.multiply(shoulder_L, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )
        cv2.putText(image, str(angle_ashoul_R),
                    tuple(np.multiply(shoulder_R, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )
        cv2.putText(image, str(angle_ahip_R),
                    tuple(np.multiply(hip_R, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )
        cv2.putText(image, str(angle_ahip_L),
                    tuple(np.multiply(hip_L, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )
        cv2.putText(image, str(angle_aknee_R),
                    tuple(np.multiply(knee_R, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )
        cv2.putText(image, str(angle_aknee_L),
                    tuple(np.multiply(knee_L, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )
        if (ls1 + er > angle_ashoul_L and ls1 - er < angle_ashoul_L):
            cv2.circle(image, tuple(np.multiply(shoulder_L, [640, 480]).astype(int)), r, co1, r)
        else:
            cv2.circle(image, tuple(np.multiply(shoulder_L, [640, 480]).astype(int)), r, co2, r)
        if (rs1 + er > angle_ashoul_R and rs1 - er < angle_ashoul_R):
            cv2.circle(image, tuple(np.multiply(shoulder_R, [640, 480]).astype(int)), r, co1, r)
        else:
            cv2.circle(image, tuple(np.multiply(shoulder_R, [640, 480]).astype(int)), r, co2, r)
        if (lh1 + er > angle_ahip_L and lh1 - er < angle_ahip_L):
            cv2.circle(image, tuple(np.multiply(hip_L, [640, 480]).astype(int)), r, co1, r)
        else:
            cv2.circle(image, tuple(np.multiply(hip_L, [640, 480]).astype(int)), r, co2, r)
        if (rh1 + er > angle_ahip_R and rh1 - er < angle_ahip_R):
            cv2.circle(image, tuple(np.multiply(hip_R, [640, 480]).astype(int)), r, co1, r)
        else:
            cv2.circle(image, tuple(np.multiply(hip_R, [640, 480]).astype(int)), r, co2, r)
        if (lk1 + er > angle_aknee_L and lk1 - er < angle_aknee_L):
            cv2.circle(image, tuple(np.multiply(knee_L, [640, 480]).astype(int)), r, co1, r)
        else:
            cv2.circle(image, tuple(np.multiply(knee_L, [640, 480]).astype(int)), r, co2, r)
        if (rk1 + er > angle_aknee_R and rk1 - er < angle_aknee_R):
            cv2.circle(image, tuple(np.multiply(knee_R, [640, 480]).astype(int)), r, co1, r)
        else:
            cv2.circle(image, tuple(np.multiply(knee_R, [640, 480]).astype(int)), r, co2, r)

    except:
        pass
    #cv2.rectangle(image, (0, 0), (450, 35), (0, 0, 0, 0), -1)

    # Rep data
    #cv2.putText(image, 'FitCore Engine Testing Edition (C) FitFrame 2021', (15, 12),
    #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 29), 1, cv2.LINE_AA)

    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )

    return image


def grayscale(data):
    try:
        img = from_b64(data)
        # Do some OpenCV Processing
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # End for OpenCV Processing

        return to_b64(pose_gen(img))
    except:
        # just in case some process is failed
        # normally, for first connection
        # return the original data
        return data
