from PIL import Image

def load_image(uploaded_file):
    return Image.open(uploaded_file)

def detect_hand_and_food_area(image):
    return image

def compute_scale_cm2(image):
    return 1.0
