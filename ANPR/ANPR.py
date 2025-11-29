import os
import cv2
import imutils
import easyocr
import numpy as np
from matplotlib import pyplot as plt


class ANPR:
    def __init__(self):
        print("Initializing OCR reader one time...")
        self.reader = easyocr.Reader(['en'])
        self.img = None
        self.gray = None
        self.edged = None
        self.contour = None
        self.cropped = None
        self.text = None

    # --------------------------
    # PRIVATE HELPERS
    # --------------------------

    def _load_image(self, path):
        self.img = cv2.imread(path)
        if self.img is None:
            raise FileNotFoundError("Image not found: " + path)

    def _preprocess_internal(self):
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(self.gray, 11, 17, 17)
        self.edged = cv2.Canny(bfilter, 30, 200)

    def _find_plate_contour(self):
        cnts = cv2.findContours(
            self.edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        for c in cnts:
            approx = cv2.approxPolyDP(c, 10, True)
            if len(approx) == 4:
                self.contour = approx
                return

        self.contour = None

    def _crop_plate(self):
        if self.contour is None:
            self.cropped = None
            return

        mask = np.zeros(self.gray.shape, np.uint8)
        cv2.drawContours(mask, [self.contour], 0, 255, -1)

        (x, y) = np.where(mask == 255)
        (x1, y1), (x2, y2) = (np.min(x), np.min(y)), (np.max(x), np.max(y))

        self.cropped = self.gray[x1:x2 + 1, y1:y2 + 1]

    def _ocr(self):
        if self.cropped is None:
            self.text = "N/A"
            return

        result = self.reader.readtext(self.cropped)
        if not result:
            self.text = "N/A"
        else:
            best = max(result, key=lambda r: r[2])
            self.text = best[1]

    # --------------------------
    # PUBLIC API
    # --------------------------

    def preprocess(self, image_path):
        """Return gray + edged for debugging."""
        self._load_image(image_path)
        self._preprocess_internal()
        return self.gray, self.edged

    def detect(self, image_path):
        """Main ANPR pipeline. Stores everything internally."""
        self._load_image(image_path)
        self._preprocess_internal()
        self._find_plate_contour()
        self._crop_plate()
        self._ocr()
        return self.text

    def render(self, show=True):
        """Return rendered image with plate + text."""
        if self.img is None:
            raise RuntimeError("Run detect() first.")

        output = self.img.copy()

        if self.contour is not None:
            cv2.drawContours(output, [self.contour], -1, (0, 255, 0), 3)
            x, y = self.contour[0][0]
            cv2.putText(output, self.text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 255, 0), 2)

        # Use matplotlib to show the image
        if show:
            plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
            plt.title(f"Detected: {self.text}")
            plt.axis("off")
            plt.show()

        # return output
        return output

    def save(self, folder, prefix="output"):
        """Save rendered, cropped, edged, and gray to folder."""

        # Create folder if doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Save rendered image
        rendered = self.render(show=False)
        cv2.imwrite(os.path.join(folder, f"{prefix}_rendered.jpg"), rendered)

        # Save grayscale
        if self.gray is not None:
            cv2.imwrite(os.path.join(folder, f"{prefix}_gray.jpg"), self.gray)

        # Save edged image
        if self.edged is not None:
            cv2.imwrite(os.path.join(
                folder, f"{prefix}_edged.jpg"), self.edged)

        # Save cropped plate
        if self.cropped is not None:
            cv2.imwrite(os.path.join(
                folder, f"{prefix}_plate.jpg"), self.cropped)

        print(f"Saved outputs to folder: {folder}")
