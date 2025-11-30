

def errorRes(error_message):
    return {"data": error_message, "status": False}


def successRes(data):
    return {"data": data, "status": True}
