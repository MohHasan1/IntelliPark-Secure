from ParkingSystem import ParkingSystem
import cv2

ps = ParkingSystem()

# ---- 1. ENTRY EVENT ----
gate_img = cv2.imread("./img/car1.jpeg")
plate = ps.handle_entry("./img/car1.jpeg")

print("DB after entry:", ps.get_db())


# ---- 2. SCAN LOT REPEATEDLY ----
lot1 = cv2.imread("./img/park0.png")
ps.scan_parking_lot(lot1)     # baseline scan

lot2 = cv2.imread("./img/park1.png")
ps.scan_parking_lot(lot2)     # new spot detected automatically

print("DB after parking:", ps.get_db())


# ---- 3. EXIT EVENT ----
# exit_img = cv2.imread("./img/car1.jpg")
ps.handle_exit("./img/car1.jpeg")

# ---- 4. VIEW DATABASE ----
print("Final DB:", ps.get_db())
