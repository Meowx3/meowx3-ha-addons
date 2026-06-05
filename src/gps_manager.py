import subprocess
import json
import re

class GPSManager:
    def __init__(self):
        self.device_path = None
        self.last_fix_quality = 0
        self.last_satellite_count = 0

    def get_gps_data(self):
        """
        Fetches a single snapshot of current GPS data from gpsd.
        Uses gpspipe to grab the most recent JSON packet.
        """
        try:
            # -w returns the latest formatted JSON packet
            result = subprocess.check_output(['gpspipe', '-w'], timeout=2)
            data = json.loads(result.decode('utf-8'))
            return data
        except Exception as e:
            print(f"Error reading from GPSD: {e}")
            return None

    def check_device_connected(self):
        """Detects if a USB GPS device is currently plugged in."""
        try:
            # Check for common UBLOX/GPS USB paths
            result = subprocess.check_output(['ls', '/dev/ttyUSB*', '/dev/ttyACM*'], stderr=subprocess.STDOUT)
            self.device_path = result.decode('utf-8').split()[0]
            return True
        except subprocess.CalledProcessError:
            self.device_path = None
            return False

    def get_antenna_diagnostics(self, gps_data):
        """
        Analyzes SNR (Signal to Noise Ratio) for antenna placement recommendations.
        GPSD provides satellite data in the 'sats' or 'satellites' key depending on version.
        """
        if not gps_data or 'sats' not in gps_data:
            return {"status": "Unknown", "recommendation": "Wait for GPS fix..."}

        sats = gps_data['sats']
        snr_values = []
        
        for sat in sats:
            # Extract SNR (usually provided as a float)
            if 'snr' in sat:
                snr_values.append(sat['snr'])

        if not snr_values:
            return {"status": "Poor", "recommendation": "No signals detected. Ensure antenna is outdoors."}

        avg_snr = sum(snr_values) / len(snr_values)
        max_snr = max(snr_values)

        # Diagnostic Logic:
        # SNR < 30: Poor signal (indoors or obstructed)
        # SNR 30-40: Acceptable for location, risky for timing
        # SNR > 40: Excellent for Stratum 1 NTP servers
        if avg_snr < 30:
            return {
                "status": "Poor", 
                "recommendation": "Very low signal. Move antenna away from walls and electronics."
            }
        elif avg_snr < 40:
            return {
                "status": "Fair", 
                "recommendation": "Signal is acceptable, but might be unstable for high-precision timing."
            }
        else:
            return {
                "status": "Excellent", 
                "recommendation": "Optimal placement. High signal quality detected."
            }

    def get_chrony_stats(self):
        """
        Parses 'chronyc tracking' to check the health of the NTP clock.
        This helps determine if PPS is actually locking the system time.
        """
        try:
            result = subprocess.check_output(['chronyc', 'tracking']).decode('utf-8')
            stats = {}
            # Use regex to find key values in chrony output
            patterns = {
                "refid": r"Reference ID\s+:\s+(\S+)",
                "stratum": r"Stratum\s+:\s+(\d+)",
                "system_offset": r"System time\s+:\s+([\d\.\-]+)",
                "last_offset": r"Last offset\s+:\s+([\d\.\-]+)"
            }
            for key, pattern in patterns.items():
                match = re.search(pattern, result)
                stats[key] = match.group(1) if match else "N/A"
            return stats
        except Exception as e:
            return {"error": f"Could not retrieve Chrony stats: {e}"}

    def get_constellation_breakdown(self, gps_data):
        """
        Filters satellites by their constellation ID for the Web UI.
        Usually: GPS=0, GLONASS=1, GALILEO=2, BEIDOU=3
        """
        if not gps_data or 'sats' not in gps_data:
            return {"GPS": 0, "GLONASS": 0, "Galileo": 0}

        breakdown = {"GPS": 0, "GLONASS": 0, "Galileo": 0}
        for sat in gps_data['sats']:
            # This depends on the GPSD version and UBLOX output mapping
            cid = sat.get('cid', -1)
            if cid == 0: breakdown["GPS"] += 1
            elif cid == 1: breakdown["GLONASS"] += 1
            elif cid == 2: breakdown["Galileo"] += 1
        
        return breakdown
