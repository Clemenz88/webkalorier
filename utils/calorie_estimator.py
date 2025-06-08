
import pandas as pd

def load_kalorie_data(path='kaloriedata.csv'):
    return pd.read_csv(path)

def estimate_calories(food_label, food_area_cm2, food_db):
    row = food_db[food_db['food'] == food_label]
    if row.empty:
        return None

    kcal_per_gram = row.iloc[0]['kcal_per_gram']
    density = row.iloc[0]['g_per_cm3']
    height_cm = 2

    volume_cm3 = food_area_cm2 * height_cm
    weight_g = volume_cm3 * density
    return round(weight_g * kcal_per_gram, 1)
