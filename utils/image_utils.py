
import cv2
import numpy as np

def load_image(path):
    return cv2.imread(path)

def detect_hand_and_food_area(img):
    hand_area_px = 7000  # placeholder-værdi
    food_area_px = 21000
    return hand_area_px, food_area_px

def compute_scale_cm2(hand_area_px, hand_area_cm2=180):
    return hand_area_cm2 / hand_area_px
