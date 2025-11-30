from ultralytics import YOLO
from ParkingSpotAnalyzer import ParkingSpotAnalyzer
import cv2
import os


def main():
    # ----------------------------------------------------
    # SETTINGS
    # ----------------------------------------------------
    MODEL_PATH = "./APSD/apsd.pt"             # YOLO model
    IMAGE_PATH = "./APSD/img/park3.png"    # image to process
    OUTPUT_FOLDER = "./APSD/output"                # folder for saving
    SHOW_IMAGE = True                         # toggle display window
    
     # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Extract base name without extension
    image_name = os.path.basename(IMAGE_PATH)         # "parking1.jpg"
    base_name = os.path.splitext(image_name)[0]       # "parking1"

    # Build final save path
    OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, f"{base_name}_annotated.jpg")

    # ----------------------------------------------------
    # LOAD YOLO PARKING-SPOT MODEL
    # ----------------------------------------------------
    print("[INFO] Loading YOLO model...")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    model = YOLO(MODEL_PATH)

    # ----------------------------------------------------
    # LOAD IMAGE
    # ----------------------------------------------------
    print("[INFO] Loading image...")
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    image = cv2.imread(IMAGE_PATH)

    # ----------------------------------------------------
    # RUN PARKING-SPOT DETECTION
    # ----------------------------------------------------
    print("[INFO] Running parking-spot detection...")
    results = model.predict(image)

    # ----------------------------------------------------
    # PROCESS SPOTS (NUMBER + LABEL)
    # ----------------------------------------------------
    print("[INFO] Processing detections...")
    psa = ParkingSpotAnalyzer(class_list=["car", "free"])

    psa.add_image_direct(image)
    psa.annotate_image(results)

    # ----------------------------------------------------
    # PRINT SUMMARY
    # ----------------------------------------------------
    summary = psa.get_parking_summary()

    print("\n------ PARKING SUMMARY ------")
    print(f"Total Spots : {summary['total_spots']}")
    print(f"Parked Cars : {summary['parked_count']} -> {summary['parked_spots']}")
    print(f"Empty Spots : {summary['empty_count']} -> {summary['empty_spots']}")
    print("------------------------------\n")

    # ----------------------------------------------------
    # SAVE OUTPUT
    # ----------------------------------------------------
    print(f"[INFO] Saving annotated image to: {OUTPUT_PATH}")
    psa.save(OUTPUT_PATH)

    # ----------------------------------------------------
    # SHOW OUTPUT (optional)
    # ----------------------------------------------------
    if SHOW_IMAGE:
        print("[INFO] Displaying result...")
        psa.show()


if __name__ == "__main__":
    main()
