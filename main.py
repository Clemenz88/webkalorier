import streamlit as st
from utils.matcher import oversæt_fuzzy
import pandas as pd
from PIL import Image
import csv
import os

from utils.image_utils import load_image, detect_hand_and_food_area, compute_scale_cm2

df = pd.read_csv("kaloriedata.csv")
food_list = df["food"].tolist()

st.title("Kalorieestimering fra billede")

uploaded_file = st.file_uploader("Upload et billede med hånd og mad", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = load_image(uploaded_file)
    st.image(img, caption="Dit billede", use_container_width=True)

    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.read())

    # Simuleret AI-output
    food_raw = "salmon"
    st.write("Genkendt af billedanalysen:", food_raw)

    # Brugeren kan rette
    corrected = st.text_input("Er dette korrekt? Ret gerne til:", value=food_raw)
    food_label = oversæt_fuzzy(corrected, food_list)

    row = df[df["food"] == food_label]
    if not row.empty:
        kcal_per_gram = float(row["kcal_per_gram"].values[0])
        gram_per_cm2 = float(row["g_per_cm2"].values[0])
        st.write("Kalorier pr. gram:", kcal_per_gram)
        st.write("g/cm²:", gram_per_cm2)
    else:
        st.warning("Fødevaren findes ikke i databasen.")

    # Feedback-knap
    if st.button("Send feedback"):
        with open("feedback_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([food_raw, corrected])
        st.success("Tak for din feedback!")
