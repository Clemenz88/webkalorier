def predict_food(image_path):
    results = model(image_path)
    if not results or not hasattr(results[0], "boxes"):
        return "ukendt"
    
    boxes = results[0].boxes
    if boxes is None or boxes.cls is None or len(boxes.cls) == 0:
        return "ukendt"

    try:
        top_class_id = int(boxes.cls[0].item())
        labels = results[0].names
        return labels.get(top_class_id, "ukendt")
    except Exception:
        return "ukendt"
