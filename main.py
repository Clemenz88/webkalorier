
import streamlit as st
from utils.image_utils import load_image, detect_hand_and_food_area, compute_scale_cm2
from utils.calorie_estimator import load_kalorie_data, estimate_calories
from PIL import Image
import tempfile
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Automatisk hentet første gang

def predict_food(image_path):
    results = model(image_path)
    labels = results[0].names
    top = results[0].probs.top1
    return labels[top]

st.title("📷 Kalorie-estimator med billede og hånd")

file = st.file_uploader("Upload et billede af din mad og hånd", type=["jpg", "png"])

if file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(file.read())
        img_path = tmp_file.name

    st.image(Image.open(img_path), caption="Analyseret billede", use_column_width=True)

    hand_area_px, food_area_px = detect_hand_and_food_area(load_image(img_path))
    scale = compute_scale_cm2(hand_area_px)
    food_area_cm2 = food_area_px * scale

    food_label = predict_food(img_path)
    db = load_kalorie_data()
    kcal = estimate_calories(food_label, food_area_cm2, db)

    if kcal:
        st.success(f"🧠 Genkendt mad: **{food_label}**\n📏 Område: {round(food_area_cm2, 1)} cm²\n🔥 Kalorier: **{kcal} kcal**")
    else:
        st.warning("Kunne ikke finde madtype i database.")
