from ANPR.ANPR import ANPR
from APSD.APSD import APSD
from APSD.ParkingSpotAnalyzer import ParkingSpotAnalyzer
from tinydb import TinyDB, Query
from datetime import datetime


def now():
    return datetime.now().isoformat()


class ParkingSystem:
    def __init__(self, apsd_model="./APSD/apsd.pt", db_path="parking_sessions.json"):
        self.anpr = ANPR()
        self.apsd = APSD(apsd_model)
        self.analyzer = ParkingSpotAnalyzer()

        self.db = TinyDB(db_path)
        self.sessions = self.db.table("sessions")   # one table only

        # For Option A comparison
        self.previous_empty_spots = None

        # Track autoincrement session id
        self.next_session_id = self._get_next_session_id()

    # ------------------------------------------------------------------
    # UTIL: Determine next session ID
    # ------------------------------------------------------------------

    def _get_next_session_id(self):
        if len(self.sessions) == 0:
            return 1
        return max(row["session_id"] for row in self.sessions.all()) + 1

    # ------------------------------------------------------------------
    # UTIL: Get latest session for plate
    # ------------------------------------------------------------------

    def _latest_session(self, plate):
        Car = Query()
        rows = self.sessions.search(Car.plate == plate)
        if not rows:
            return None
        return sorted(rows, key=lambda r: r["session_id"], reverse=True)[0]

    # ------------------------------------------------------------------
    # EVENT 1: ENTRY
    # ------------------------------------------------------------------

    def handle_entry(self, gate_image_path):
        plate = self.anpr.detect(gate_image_path)
        
        # if same plate enters again with out exiting
        Car = Query()

        # If same plate is already inside (entering or parked)
        active_session = self.sessions.get(
            (Car.plate == plate) & (Car.status != "exited")
        )

        if active_session:
            print(f"[WARNING] Duplicate entry blocked: {plate} already inside!")
            return {
                "error": "Car already inside",
                "plate": plate,
                "session_id": active_session["session_id"],
                "status": active_session["status"]
            }


        session_id = self.next_session_id
        self.next_session_id += 1

        self.sessions.insert({
            "session_id": session_id,
            "plate": plate,
            "status": "entering",
            "spot": None,
            "entry_time": now(),
            "park_time": None,
            "exit_time": None
        })

        print(f"[ENTRY] Car entered: {plate} (session {session_id})")

        return plate

    # ------------------------------------------------------------------
    # EVENT 2: PARKING LOT SCAN
    # ------------------------------------------------------------------

    def scan_parking_lot(self, lot_image):
        results = self.apsd.predict(lot_image)
        self.analyzer.add_image_direct(lot_image)
        self.analyzer.annotate_image(results)

        summary = self.analyzer.get_parking_summary()
        empty_spots = summary["empty_spots"]

        print(f"[LOT] Empty spots: {empty_spots}")

        # First scan baseline
        if self.previous_empty_spots is None:
            self.previous_empty_spots = empty_spots.copy()
            print("Baseline empty spots:", self.previous_empty_spots)
            return summary.copy()

        print("PREVIOUS  ->", self.previous_empty_spots)
        print("CURRENT   ->", empty_spots)

        newly_taken = list(set(self.previous_empty_spots) - set(empty_spots))
        print("NEWLY TAKEN ->", newly_taken)

        if len(newly_taken) == 1:
            spot_num = newly_taken[0]
            self._assign_new_spot(spot_num)

        self.previous_empty_spots = empty_spots.copy()

        return summary.copy()

    # ------------------------------------------------------------------
    # Assign spot
    # ------------------------------------------------------------------

    def _assign_new_spot(self, spot_number):
        Car = Query()

        # Find the latest "entering" session
        entering = self.sessions.search(Car.status == "entering")
        if not entering:
            print("[PARK] No entering car to assign spot.")
            return

        # Latest entering = max session id
        latest = sorted(
            entering, key=lambda x: x["session_id"], reverse=True)[0]

        self.sessions.update({
            "spot": spot_number,
            "status": "parked",
            "park_time": now()
        }, Car.session_id == latest["session_id"])

        print(f"[PARK] {latest['plate']} assigned to spot {spot_number}")

    # ------------------------------------------------------------------
    # EVENT 3: EXIT
    # ------------------------------------------------------------------

    def handle_exit(self, exit_image_path):
        plate = self.anpr.detect(exit_image_path)
        Car = Query()

        latest = self._latest_session(plate)
        if latest is None:
            print(f"[EXIT] Unknown car leaving: {plate}")
            return None

        self.sessions.update({
            "status": "exited",
            "exit_time": now(),
            "previous_spot": latest["spot"],
            "spot": None
        }, Car.session_id == latest["session_id"])

        print(f"[EXIT] Car exited: {plate} (session {latest['session_id']})")

        return plate

    # ------------------------------------------------------------------
    # GET DB
    # ------------------------------------------------------------------

    def get_db(self):
        return self.sessions.all()
