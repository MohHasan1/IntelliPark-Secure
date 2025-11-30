# SceneController.py

import cv2
import time
from ParkingSystem import ParkingSystem


class SceneController:
    def __init__(self):
        self.ps = ParkingSystem()

        # Preset demo scenes
        self.scenes = {
            "1": {
                "entry": "./img/car1.jpeg",
                "lot_before": "./img/park0.png",
                "lot_after": "./img/park1.png",
                "exit": None
            },
            "2": {
                "entry": "./img/car2.jpeg",
                "lot_before": "./img/park1.png",
                "lot_after": "./img/park2.png",
                "exit": None
            },
            "3": {
                "entry": None,
                "lot_before": "./img/park2.png",
                "lot_after": "./img/park1.png",
                "exit": "./img/car2.jpeg"
            },
            "4": {
                "entry": None,
                "lot_before": "./img/park1.png",
                "lot_after": "./img/park0.png",
                "exit": "./img/car1.jpeg"
            }
        }

    # -------------------------
    # ANIMATION HELPERS
    # -------------------------

    def pause(self, seconds, message):
        """Smooth animation delay."""
        print(message, end="", flush=True)
        for _ in range(seconds):
            print(".", end="", flush=True)
            time.sleep(1)
        print()  # new line

    # -------------------------
    # RUN SCENE
    # -------------------------

    def run_scene(self, key):
        if key not in self.scenes:
            return {"error": f"Scene '{key}' does not exist."}

        config = self.scenes[key]
        summary_log = []

        print(f"\n=========== Running Scene {key} ===========")

        # ---- ENTRY ----
        if config["entry"]:
            self.pause(2, "Detecting car at gate")
            plate = self.ps.handle_entry(config["entry"])
            summary_log.append({"entry": plate})

            self.pause(2, "Car moving toward parking area")

        # ---- BEFORE PARK IMAGE ----
        if config["lot_before"]:
            img = cv2.imread(config["lot_before"])
            summary = self.ps.scan_parking_lot(img)
            summary_log.append({"before": summary})

        # ---- SIMULATE PARKING ----
        if config["lot_after"]:
            self.pause(3, "Car searching for spot")
            img = cv2.imread(config["lot_after"])
            summary = self.ps.scan_parking_lot(img)
            summary_log.append({"after": summary})

        # ---- EXIT ----
        if config["exit"]:
            self.pause(2, "Car approaching exit gate")
            plate = self.ps.handle_exit(config["exit"])
            summary_log.append({"exit": plate})

        print(f"Scene {key} complete.")
        print("=====================================\n")

        return {
            "scene": key,
            "log": summary_log,
            "db": self.ps.get_db()
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
