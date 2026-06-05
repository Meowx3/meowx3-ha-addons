import glob
import json

def detect_gps():
    devices = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    return devices

def detect_pps():
    return glob.glob("/dev/pps*")

if __name__ == "__main__":
    print(json.dumps({
        "gps": detect_gps(),
        "pps": detect_pps()
    }))
