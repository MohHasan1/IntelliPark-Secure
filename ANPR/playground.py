import cv2
import imutils
import easyocr
import numpy as np
from matplotlib import pyplot as plt

# 1. Read the image
img = cv2.imread("./img/test/car1.png")

# Check if image loaded
if img is None:
    print("❌ Image not found. Check path.")
    exit()

# 2. Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
# plt.title("Gray Image")
# plt.show()

# 3. Noise reduction
bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

# 4.Edge detection
edged = cv2.Canny(bfilter, 30, 200)

# 5. Find Contours & Pick the Plate Shape
keypoints = cv2.findContours(
    edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None

for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
# plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
# plt.title("Edged image")
# plt.show()

# 6. Mask the Plate
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0, 255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)
# plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
# plt.title("Masked Plate")
# plt.show()

# 7.Crop the Plate for OCR
(x, y) = np.where(mask == 255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))

cropped = gray[x1:x2+1, y1:y2+1]
# plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
# plt.title("Cropped Plate")
# plt.show()


# 8. OCR (EasyOCR)
reader = easyocr.Reader(['en'])
result = reader.readtext(cropped)

print(result)
if not result:
    print("No text found")
else:
   # Select the best OCR result
    best = max(result, key=lambda r: r[2])
    text = best[1]
    print("Plate:", text)

# 9. Render result on original image
output = img.copy()

# Draw rectangle around plate
cv2.drawContours(output, [location], -1, (0, 255, 0), 3)

# Put text slightly above plate
x, y = location[0][0]
cv2.putText(
    output,
    text,
    (x, y - 10),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.0,
    (0, 255, 0),
    2,
    cv2.LINE_AA
)

plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
