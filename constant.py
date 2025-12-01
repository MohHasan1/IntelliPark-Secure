# config.py

CONST = {
    "total_spots": 4,

    "delays": {
        "entry_delay": 2,
        "lot_scan_delay": 3,
        "parking_delay": 4,
        "exit_delay": 2,
    },

    "scenes": {
        "1": {
            "entry": "./img/car1.jpeg",
            "lot_before": "./img/park0.png",
            "lot_after": "./img/park1.png",
            "exit": None,
            "type": "entry"
        },
        "2": {
            "entry": "./img/car2.jpeg",
            "lot_before": "./img/park1.png",
            "lot_after": "./img/park2.png",
            "exit": None,
            "type": "entry"
        },
        "3": {
            "entry": "./img/car3.png",
            "lot_before": "./img/park2.png",
            "lot_after": "./img/park3.png",
            "exit": None,
            "type": "entry"
        },
        "4": {
            "entry": "./img/car4.png",
            "lot_before": "./img/park3.png",
            "lot_after": "./img/park4.png",
            "exit": None,
            "type": "entry"
        },
        "5": {
            "entry": None,
            "lot_before": "./img/park4.png",
            "lot_after": "./img/park3.png",
            "exit": "./img/car4.png",
            "type": "exit",
        },
        "6": {
            "entry": None,
            "lot_before": "./img/park3.png",
            "lot_after": "./img/park2.png",
            "exit": "./img/car3.png",
            "type": "exit",
        },
        "7": {
            "entry": None,
            "lot_before": "./img/park2.png",
            "lot_after": "./img/park1.png",
            "exit": "./img/car2.jpeg",
            "type": "exit"
        },
        "8": {
            "entry": None,
            "lot_before": "./img/park1.png",
            "lot_after": "./img/park0.png",
            "exit": "./img/car1.jpeg",
            "type": "exit"
        },
    },
}
