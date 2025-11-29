# SceneController.py

import cv2
from ParkingSystem import ParkingSystem


class SceneController:
    def __init__(self):
        self.ps = ParkingSystem()

        # PRESET IMAGE PATHS FOR SCENES
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
                "lot_after": "./img/park1.png",
                "exit": None
            },
            "3": {
                "entry": None,
                "lot_before": None,
                "lot_after": None,
                "exit": "./img/car1.jpeg"
            },
            "4": {
                "entry": None,
                "lot_before": None,
                "lot_after": None,
                "exit": "./img/car2.jpeg"
            }
        }

    def run_scene(self, key):
        if key not in self.scenes:
            print(f"❌ Scene '{key}' does not exist.")
            return

        print(f"\n=========== Running {key} ===========")

        config = self.scenes[key]

        # 1. Entry
        if config["entry"] is not None:
            self.ps.handle_entry(config["entry"])

        # 2. Lot before parking
        if config["lot_before"] is not None:
            img = cv2.imread(config["lot_before"])
            self.ps.scan_parking_lot(img)

        # 3. Lot after parking
        if config["lot_after"] is not None:
            img = cv2.imread(config["lot_after"])
            self.ps.scan_parking_lot(img)

        # 4. Exit
        if config["exit"] is not None:
            self.ps.handle_exit(config["exit"])

        print("DB:", self.ps.get_db())
        print("=====================================\n")

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
