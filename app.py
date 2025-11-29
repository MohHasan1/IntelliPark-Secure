# main.py

from ParkingSystem import ParkingSystem
import cv2
import os


def load_image_from_user(prompt):
    """Repeatedly ask user for a valid image path."""
    while True:
        path = input(prompt).strip()

        if path.lower() == "q":
            return "q", None

        if not os.path.exists(path):
            print("❌ File not found. Try again.")
            continue

        img = cv2.imread(path)
        if img is None:
            print("❌ Could not load image. Try again.")
            continue

        return path, img


def main():
    ps = ParkingSystem()

    print("\n=========== PARK VISION SYSTEM STARTED ===========\n")
    print("Press 'q' at any time to quit.\n")

    while True:

        print("\n---- ENTRY EVENT ----")
        gate_path, gate_img = load_image_from_user("Entry gate image path: ")

        if gate_path == "q":
            break

        plate = ps.handle_entry(gate_path)
        print("DB:", ps.get_db())

        print("\n---- PARKING LOT SCAN 1 (Before parking) ----")
        lot1_path, lot1_img = load_image_from_user("Parking lot BEFORE parking: ")

        if lot1_path == "q":
            break

        ps.scan_parking_lot(lot1_img)

        print("\n---- PARKING LOT SCAN 2 (After parking) ----")
        lot2_path, lot2_img = load_image_from_user("Parking lot AFTER parking: ")

        if lot2_path == "q":
            break

        ps.scan_parking_lot(lot2_img)

        print("DB after parking:", ps.get_db())

        print("\n---- EXIT EVENT ----")
        exit_path, exit_img = load_image_from_user("Exit gate image path: ")

        if exit_path == "q":
            break

        ps.handle_exit(exit_path)

        print("\nCurrent DB:", ps.get_db())
        print("\n➡ Ready for next car...\n")
        print("----------------------------------------------")

    print("\n=========== SYSTEM SHUTDOWN ===========\n")


if __name__ == "__main__":
    main()
