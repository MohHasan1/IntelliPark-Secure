import cv2
from ANPR.ANPR import ANPR
from APSD.APSD import APSD
from APSD.ParkingSpotAnalyzer import ParkingSpotAnalyzer


class ParkingSystem:
    def __init__(self, apsd_model="./APSD/apsd.pt"):
        self.anpr = ANPR()
        self.apsd = APSD(apsd_model)
        self.analyzer = ParkingSpotAnalyzer()

        # Store all car sessions
        # plateNumber → { plate, status, spot }
        self.db = {}

        # For Option A comparison
        self.previous_empty_spots = None

    # ------------------------------------------------------------------
    # EVENT 1: ENTRY (Gate Camera)
    # ------------------------------------------------------------------

    def handle_entry(self, gate_image):
        """Triggered when a car arrives at the gate."""
        plate = self.anpr.detect(gate_image)

        self.db[plate] = {
            "plate": plate,
            "status": "entering",
            "spot": None
        }

        print(f"[ENTRY] Car entered: {plate}")

        # Once entry occurs → next APSD scan will watch for new spot taken
        return plate

    # ------------------------------------------------------------------
    # EVENT 2: PARKING LOT SCAN (APSD camera)
    # ------------------------------------------------------------------

    def scan_parking_lot(self, lot_image):
        """Triggered periodically until car is parked."""
        results = self.apsd.predict(lot_image)

        self.analyzer.add_image_direct(lot_image)
        self.analyzer.annotate_image(results)

        summary = self.analyzer.get_parking_summary()
        empty_spots = summary["empty_spots"]

        print(f"[LOT] Empty spots: {empty_spots}")

        # First scan → store baseline
        if self.previous_empty_spots is None:
            self.previous_empty_spots = empty_spots.copy() 
            print("previous_empty_spots", self.previous_empty_spots)
            return summary

        # Compare new vs old
        print("PREVIOUS ->", self.previous_empty_spots)
        print("CURRENT  ->", empty_spots)
        newly_taken = list(set(self.previous_empty_spots) - set(empty_spots))
        print("NEWLY TAKEN ->", newly_taken)


        if len(newly_taken) == 1:
            spot_num = newly_taken[0]
            print(f"[LOT] New spot taken: {spot_num}")

            self.assign_new_spot(spot_num)

        # Update baseline
        self.previous_empty_spots = empty_spots.copy()

        return summary

    # ------------------------------------------------------------------
    # Assign spot automatically (Option A)
    # ------------------------------------------------------------------

    def assign_new_spot(self, spot_number):
        """Assign the newly taken spot to the car that is currently entering."""
        for plate, data in self.db.items():
            if data["status"] == "entering" and data["spot"] is None:
                self.db[plate]["spot"] = spot_number
                self.db[plate]["status"] = "parked"

                print(f"[PARK] {plate} → Spot {spot_number}")
                return plate

        print("[ERROR] No 'entering' car found to assign spot.")

    # ------------------------------------------------------------------
    # EVENT 3: EXIT (Gate Camera)
    # ------------------------------------------------------------------

    def handle_exit(self, exit_image):
        """Triggered when car reaches exit gate."""
        plate = self.anpr.detect(exit_image)

        if plate not in self.db:
            print(f"[EXIT] Unknown car leaving: {plate}")
            return None

        self.db[plate]["status"] = "exited"
        self.db[plate]["previou_spot"] = self.db[plate]["spot"]
        self.db[plate]["spot"] = None

        print(f"[EXIT] Car exited: {plate}")
        return plate

    # ------------------------------------------------------------------
    # Utility to inspect database
    # ------------------------------------------------------------------

    def get_db(self):
        return self.db
