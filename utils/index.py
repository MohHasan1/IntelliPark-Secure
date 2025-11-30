import re
from datetime import datetime


def errorRes(error_message):
    return {"data": error_message, "status": False}


def successRes(data):
    return {"data": data, "status": True}


def now():
    return datetime.now().isoformat()


def slug_plate(plate: str):
    """Convert license plate into a clean slug format."""
    if not plate:
        return None
    plate = plate.upper().strip()
    plate = re.sub(r"[^A-Z0-9]", "-", plate)   # convert separators to '-'
    plate = re.sub(r"-+", "-", plate)          # collapse multiple dashes
    return plate.lower()
