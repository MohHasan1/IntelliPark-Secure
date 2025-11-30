# SceneController.py

import cv2
import time
from ParkingSystem import ParkingSystem
from constant import CONST


class SceneController:
    def __init__(self):
        self.ps = ParkingSystem()

        # Load directly from config.py
        self.scenes = CONST["scenes"]
        self.delays = CONST["delays"]
        
        self.ps.add_allowed("a8o8-xyz")

    def pause(self, seconds, message):
        print(message, end="", flush=True)
        for _ in range(seconds):
            print(".", end="", flush=True)
            time.sleep(1)
        print()

    def run_scene(self, key):
        if key not in self.scenes:
            return {"error": f"Scene '{key}' does not exist."}

        config = self.scenes[key]
        summary_log = []

        print(f"\n=========== Running Scene {key} ===========")

        # ---- ENTRY ----
        if config["entry"]:
            self.pause(self.delays["entry_delay"], "Detecting License Plate at gate.")
            plate = self.ps.handle_entry(config["entry"])
            summary_log.append({"entry": plate})
            
            if isinstance(plate, dict) and "error" in plate:
                print(plate)
                return 

            self.pause(self.delays["lot_scan_delay"], "Looking for a Spot")

        # ---- BEFORE PARK ----
        if config["lot_before"]:
            img = cv2.imread(config["lot_before"])
            summary = self.ps.scan_parking_lot(img)
            summary_log.append({"before": summary})

        # ---- PARKING ----
        if config["lot_after"]:
            self.pause(self.delays["parking_delay"], "Car Parking")
            img = cv2.imread(config["lot_after"])
            summary = self.ps.scan_parking_lot(img)
            summary_log.append({"after": summary})

        # ---- EXIT ----
        if config["exit"]:
            self.pause(self.delays["exit_delay"], "Car approaching exit gate")
            plate = self.ps.handle_exit(config["exit"])
            summary_log.append({"exit": plate})

        return {
            "scene": key,
            "log": summary_log,
            "db": self.ps.get_db(),
        }


# Testing the Scene controller #
def main():
    sc = SceneController()

    print("\n=========== PARK VISION SCENE SIMULATOR ===========")
    print("Available scenes:")
    print(" scene1 — Car enters + parks")
    print(" scene2 — Second car enters + parks")
    print(" scene3 — Third car enters + parks")
    print(" scene4 — One car exits")
    print("---------------------------------------------------")
    print("Type 'q' to quit.")
    print("===================================================\n")

    while True:
        cmd = input("Enter scene name: ").strip().lower()

        if cmd == "q":
            break

        sc.run_scene(cmd)

    print("\nSystem shutting down. Goodbye.")


if __name__ == "__main__":
    main()
