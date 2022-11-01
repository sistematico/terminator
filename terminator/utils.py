from datetime import datetime

def hora_certa() -> str:
    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M:%S")
    return currentTime