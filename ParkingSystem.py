import os
from ANPR.ANPR import ANPR
from APSD.APSD import APSD
from tinydb import TinyDB, Query
from APSD.ParkingSpotAnalyzer import ParkingSpotAnalyzer
from utils.index import now, slug_plate


class ParkingSystem:
    def __init__(self, apsd_model="./APSD/apsd.pt", db_path="parking_sessions.json"):
        self.anpr = ANPR()
        self.apsd = APSD(apsd_model)
        self.analyzer = ParkingSpotAnalyzer()

        self.db_path = db_path
        self.db = TinyDB(db_path)

        self.sessions = self.db.table("sessions")
        self.allowed = self.db.table("allowed_cars")
        self.meta = self.db.table("meta")

        self.previous_empty_spots = None
        self.security_enabled = True

        self.next_session_id = self._get_next_session_id()
        self.next_scan_id = self._get_next_scan_id()

    # ------------------------------------------------------------------
    # SECURITY TOGGLE METHODS
    # ------------------------------------------------------------------

    def enable_security(self):
        self.security_enabled = True
        return True

    def disable_security(self):
        self.security_enabled = False
        return True

    def toggle_security(self):
        self.security_enabled = not self.security_enabled
        return self.security_enabled

    def is_security_enabled(self):
        return self.security_enabled

    # ------------------------------------------------------------------
    # UTIL: session
    # ------------------------------------------------------------------

    def _get_next_session_id(self):
        if len(self.sessions) == 0:
            return 1
        return max(row["session_id"] for row in self.sessions.all()) + 1

    def _get_next_scan_id(self):
        Meta = Query()
        row = self.meta.get(Meta.key == "scan_counter")
        if row and "value" in row:
            return row["value"]
        return 1

    def _bump_scan_id(self):
        Meta = Query()
        current = self.next_scan_id
        self.next_scan_id += 1
        self.meta.upsert(
            {"key": "scan_counter", "value": self.next_scan_id},
            Meta.key == "scan_counter"
        )
        return current

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
        plate_raw = self.anpr.detect(gate_image_path)
        plate = slug_plate(plate_raw)

        # Save
        try:
            folder = "./output/anpr/entry"
            os.makedirs(folder, exist_ok=True)
            prefix = f"entry_scan_{self._bump_scan_id()}"
            self.anpr.save(folder=folder, prefix=prefix)
        except Exception as e:
            print(f"[WARN] Failed to save ANPR entry images: {e}")

        Car = Query()

        # 🚨 SECURITY CHECK
        if self.security_enabled:
            if not self.is_allowed(plate):
                return {
                    "error": "ACCESS DENIED",
                    "message": "Car is not on the allowed list",
                    "plate": plate
                }

        # Prevent duplicate entry
        active_session = self.sessions.get(
            (Car.plate == plate) & (Car.status != "exited")
        )

        if active_session:
            return {
                "error": "Car already inside",
                "plate": plate,
                "session_id": active_session["session_id"],
                "status": active_session["status"]
            }

        # Create new session
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

        return plate

    # ------------------------------------------------------------------
    # EVENT 2: PARKING LOT SCAN
    # ------------------------------------------------------------------

    def scan_parking_lot(self, lot_image):
        results = self.apsd.predict(lot_image)
        self.analyzer.add_image_direct(lot_image)
        self.analyzer.annotate_image(results)

        # save with persistent scan index
        OUTPUT_FOLDER = "./output/apsd/"
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        scan_id = self._bump_scan_id()
        base_name = f"scan_{scan_id}"
        output_path = os.path.join(OUTPUT_FOLDER, f"{base_name}_annotated.jpg")

        try:
            self.analyzer.save(output_path=output_path)
        except TypeError:
            self.analyzer.save(output_path)

        # calculate
        summary = self.analyzer.get_parking_summary()
        empty_spots = summary["empty_spots"]

        if self.previous_empty_spots is None:
            self.previous_empty_spots = empty_spots.copy()
            return summary.copy()

        newly_taken = list(set(self.previous_empty_spots) - set(empty_spots))

        if len(newly_taken) == 1:
            self._assign_new_spot(newly_taken[0])

        self.previous_empty_spots = empty_spots.copy()

        return summary.copy()

    # ------------------------------------------------------------------
    # Assign spot
    # ------------------------------------------------------------------

    def _assign_new_spot(self, spot_number):
        Car = Query()
        entering = self.sessions.search(Car.status == "entering")

        if not entering:
            return

        latest = sorted(
            entering, key=lambda x: x["session_id"], reverse=True)[0]

        self.sessions.update({
            "spot": spot_number,
            "status": "parked",
            "park_time": now()
        }, Car.session_id == latest["session_id"])

    # ------------------------------------------------------------------
    # EVENT 3: EXIT
    # ------------------------------------------------------------------

    def handle_exit(self, exit_image_path):
        plate_raw = self.anpr.detect(exit_image_path)
        plate = slug_plate(plate_raw)

        Car = Query()

        latest = self._latest_session(plate)
        if latest is None:
            return None

        self.sessions.update({
            "status": "exited",
            "exit_time": now(),
            "previous_spot": latest["spot"],
            "spot": None
        }, Car.session_id == latest["session_id"])

        # Save ANPR debug outputs for exit
        try:
            anpr_folder = "./output/anpr/exit"
            os.makedirs(anpr_folder, exist_ok=True)
            prefix = f"exit_scan_{self._bump_scan_id()}"
            self.anpr.save(folder=anpr_folder, prefix=prefix)
        except Exception as e:
            print(f"[WARN] Failed to save ANPR exit images: {e}")

        return plate

    # ------------------------------------------------------------------
    # DB ACCESS HELPERS
    # ------------------------------------------------------------------

    def reload_db(self):
        """Reload TinyDB and tables to reflect latest JSON state."""
        self.db = TinyDB(self.db_path)
        self.sessions = self.db.table("sessions")
        self.allowed = self.db.table("allowed_cars")
        self.meta = self.db.table("meta")
        self.next_scan_id = self._get_next_scan_id()

    def get_db(self):
        self.reload_db()
        return self.sessions.all()

    def get_current_sessions(self):
        self.reload_db()
        Car = Query()
        return self.sessions.search((Car.status == "entering") | (Car.status == "parked"))

    def get_past_sessions(self):
        self.reload_db()
        Car = Query()
        return self.sessions.search(Car.status == "exited")

    def get_sessions_of_plate(self, plate: str):
        self.reload_db()
        Car = Query()
        return self.sessions.search(Car.plate == slug_plate(plate))

    def get_last_session_of_plate(self, plate: str):
        self.reload_db()
        rows = self.get_sessions_of_plate(plate)
        if not rows:
            return None
        return sorted(rows, key=lambda x: x["session_id"], reverse=True)[0]

    # ------------------------------------------------------------------
    # ALLOWED CAR CHECK
    # ------------------------------------------------------------------

    def is_allowed(self, plate: str) -> bool:
        Car = Query()
        return self.allowed.contains(Car.plate == plate)

    def add_allowed(self, plate: str):
        plate = slug_plate(plate)
        Car = Query()

        if not self.allowed.contains(Car.plate == plate):
            self.allowed.insert({"plate": plate})
            return True
        return False

    def remove_allowed(self, plate: str):
        plate = slug_plate(plate)
        Car = Query()
        self.allowed.remove(Car.plate == plate)

    def get_allowed_list(self):
        return self.allowed.all()
