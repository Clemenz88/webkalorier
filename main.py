import streamlit as st
from utils.image_utils import load_image, detect_hand_and_food_area, compute_scale_cm2
from utils.calorie_estimator import load_kalorie_data, estimate_calories
from PIL import Image
import tempfile
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def predict_food(image_path):
    results = model(image_path)
    boxes = results[0].boxes
    if boxes is None or getattr(boxes, "cls", None) is None or len(boxes.cls) == 0:
        return "ukendt"
    try:
        top_class_id = int(boxes.cls[0].item())
        labels = results[0].names
        return labels.get(top_class_id, "ukendt")
    except:
        return "ukendt"

st.title("📷 Kalorie‑estimator med billede og hånd")

file = st.file_uploader("Upload billede af mad + hånd", type=["jpg", "png"])
if file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(file.read())
        img_path = tmp.name

    st.image(Image.open(img_path), caption="Analyseret billede", use_column_width=True)
    hand_px, food_px = detect_hand_and_food_area(load_image(img_path))
    scale = compute_scale_cm2(hand_px)
    area_cm2 = food_px * scale

    food = predict_food(img_path)
    db = load_kalorie_data()
    kcal = estimate_calories(food, area_cm2, db)

    if kcal:
        st.success(f"🧠 Genkendt mad: **{food}**\n📏 Område: {round(area_cm2,1)} cm²\n🔥 Kalorier: **{kcal} kcal**")
    else:
        st.warning("🔎 Kunne ikke finde madtype i database.")
