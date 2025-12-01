import os
import cv2


class ParkingSpotAnalyzer:
    """
    Takes YOLO parking-spot detection results and:
    - Loads images (file or direct)
    - Sorts detected spots (top→bottom, left→right)
    - Assigns spot numbers
    - Determines empty vs parked
    - Annotates the image
    - Allows saving and displaying separately
    """

    def __init__(self, class_list=None):
        self.original_image = None
        self.last_annotated_image = None

        self.class_list = class_list if class_list else ["car", "free"]

        self.all_spots = []
        self.empty_spot_numbers = []
        self.parked_spot_numbers = []

    # ------------------------------------------------------------
    # IMAGE LOADING
    # ------------------------------------------------------------

    def add_image_using_path(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image path does not exist: {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from: {image_path}")

        self.original_image = image.copy()
        return image

    def add_image_direct(self, image):
        if image is None or not hasattr(image, "shape"):
            raise ValueError("Invalid OpenCV image provided.")
        self.original_image = image.copy()

    # ------------------------------------------------------------
    # SORTING
    # ------------------------------------------------------------

    def sort_spots_top_to_bottom_left_to_right(self, spots):
        if not spots:
            return []

        spots = sorted(spots, key=lambda s: s["coords"][1])
        heights = [s["coords"][3] - s["coords"][1] for s in spots]
        avg_height = sum(heights) / len(heights)
        row_threshold = avg_height * 0.6

        rows = []
        for spot in spots:
            y_min = spot["coords"][1]
            placed = False

            for row in rows:
                if abs(y_min - row[0]["coords"][1]) < row_threshold:
                    row.append(spot)
                    placed = True
                    break

            if not placed:
                rows.append([spot])

        sorted_spots = []
        for row in rows:
            sorted_spots.extend(sorted(row, key=lambda s: s["coords"][0]))

        return sorted_spots

    # ------------------------------------------------------------
    # ANNOTATION
    # ------------------------------------------------------------

    def annotate_image(self, results):
        if self.original_image is None:
            raise ValueError(
                "No image loaded. Use add_image() or add_image_direct().")

        self.all_spots.clear()
        self.empty_spot_numbers.clear()
        self.parked_spot_numbers.clear()

        image = self.original_image.copy()

        # Extract YOLO detections
        for result in results:
            for box, conf, class_id in zip(
                result.boxes.xyxy,
                result.boxes.conf,
                result.boxes.cls
            ):
                x_min, y_min, x_max, y_max = map(int, box)

                self.all_spots.append({
                    "coords": (x_min, y_min, x_max, y_max),
                    "class_id": int(class_id),
                    "confidence": float(conf)
                })

        self.all_spots = self.sort_spots_top_to_bottom_left_to_right(
            self.all_spots)

        # Draw annotation
        for i, spot in enumerate(self.all_spots, start=1):
            x_min, y_min, x_max, y_max = spot["coords"]
            class_name = self.class_list[spot["class_id"]]

            cv2.rectangle(image, (x_min, y_min),
                          (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(image, str(i), (x_min, y_min - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            if class_name == "free":
                self.empty_spot_numbers.append(i)
            else:
                self.parked_spot_numbers.append(i)

        self.last_annotated_image = image
        return image

    # ------------------------------------------------------------
    # GETTERS
    # ------------------------------------------------------------

    def get_empty_spots(self):
        return self.empty_spot_numbers

    def get_parked_spots(self):
        return self.parked_spot_numbers

    def get_all_spots(self):
        return self.all_spots

    def get_parking_summary(self):
        return {
            "total_spots": len(self.all_spots),
            "parked_count": len(self.parked_spot_numbers),
            "empty_count": len(self.empty_spot_numbers),
            "empty_spots": self.empty_spot_numbers.copy(),
            "parked_spots": self.parked_spot_numbers.copy(),
        }

    # ------------------------------------------------------------
    # SAVE + SHOW 
    # ------------------------------------------------------------

    def save(self, output_path="annotated.jpg"):
        """Save only – no display."""
        if self.last_annotated_image is None:
            raise ValueError("No annotated image. Run annotate_image() first.")

        cv2.imwrite(output_path, self.last_annotated_image)
        return output_path

    def show(self, resize_dim=(900, 900)):
        """Show only – no file saving."""
        if self.last_annotated_image is None:
            raise ValueError("No annotated image. Run annotate_image() first.")

        resized = cv2.resize(self.last_annotated_image, resize_dim)
        cv2.imshow("Parking Spot Detection", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
