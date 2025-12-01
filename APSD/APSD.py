import os
from ultralytics import YOLO


class APSD:
    def __init__(self, model_path="./APSD/apsd.pt", class_list=None):
        self.model_path = model_path
        self.model = YOLO(self.model_path)
        self.class_list = class_list if class_list else ["car", "free"]
        self.last_prediction = None

    # json - result
    def predict(self, image):
        self.last_prediction = self.model.predict(image)
        return self.last_prediction

    def set_model_path(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model path '{path}' does not exist.")
        self.model_path = path
        self.model = YOLO(self.model_path)

    def set_class_list(self, class_list):
        if isinstance(class_list, list):
            self.class_list = class_list
        else:
            raise ValueError("class_list must be a list of strings")

    def get_model_path(self):
        return self.model_path

    def get_class_list(self):
        return self.class_list

    def get_last_pred(self):
        return self.last_prediction
