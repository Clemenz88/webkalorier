def predict_food(image_path):
    results = model(image_path)
    detections = results[0].boxes
    if len(detections) == 0:
        return "ukendt"
    top_class_id = int(detections.cls[0].item())  # første detektion
    labels = results[0].names
    return labels[top_class_id]
