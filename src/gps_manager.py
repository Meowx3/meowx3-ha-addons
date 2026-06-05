import subprocess
import json
import re
from datetime import datetime

class GPSManager:
    def __init__(self):
        self.device_path = None
        self.last_fix_quality = 0
        self.last_satellite_count = 0

    # ... [Previous methods: get_gps_data, check_device_connected, etc.] ...
    # Keep all previous methods (get_gps_data, get_antenna_diagnostics, etc.) here

    def get_gps_data(self):
        try:
            result = subprocess.check_output(['gpspipe', '-w'], timeout=2)
            return json.loads(result.decode('utf-8'))
        except Exception as e:
            print(f"Error reading from GPSD: {e}")
            return None

    def get_antenna_diagnostics(self, gps_data):
        if not gps_data or 'sats' not in gps_data:
            return {"status": "Unknown", "recommendation": "Wait for GPS fix..."}
        sats = gps_data['sats']
        snr_values = [sat['snr'] for sat in sats if 'snr' in sat]
        if not snr_values:
            return {"status": "Poor", "recommendation": "No signals detected."}
        avg_snr = sum(snr_values) / len(snr_values)
        if avg_snr < 30: return {"status": "Poor", "recommendation": "Move antenna away from walls."}
        elif avg_snr < 40: return {"status": "Fair", "recommendation": "Signal is acceptable, but unstable."}
        else: return {"status": "Excellent", "recommendation": "Optimal placement."}

    def get_chrony_stats(self):
        try:
            result = subprocess.check_output(['chronyc', 'tracking']).decode('utf-8')
            stats = {}
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
            return {"error": str(e)}

    def get_constellation_breakdown(self, gps_data):
        if not gps_data or 'sats' not in gps_data:
            return {"GPS": 0, "GLONASS": 0, "Galileo": 0}
        breakdown = {"GPS": 0, "GLONASS": 0, "Galileo": 0}
        for sat in gps_data['sats']:
            cid = sat.get('cid', -1)
            if cid == 0: breakdown["GPS"] += 1
            elif cid == 1: breakdown["GLONASS"] += 1
            elif cid == 2: breakdown["Galileo"] += 1
        return breakdown

    def get_ntp_clients(self):
        """
        Queries the Linux conntrack table to find IPs that have sent packets
        to UDP port 123. Returns a list of unique IPs and their last seen time.
        """
        try:
            # We search for UDP packets where the destination port is 123 (NTP)
            # -p udp : filter by protocol
            # --dport 123 : filter by destination port
            cmd = ['conntrack', '-L', '-p', 'udp', '--dport', '123']
            result = subprocess.check_output(cmd).decode('utf-8')
            
            clients = {}
            # Example line: udp 6 udp ct state established src 192.168.1.50 dst 192.168.1.10 sport ...
            for line in result.splitlines():
                # Extract the source IP using regex
                match = re.search(r'src (\d{1,3}(?:\.\d{1,3}){3})', line)
                if match:
                    ip = match.group(1)
                    # We use current time as the 'last seen' because conntrack 
                    # entries are active/recent.
                    clients[ip] = datetime.now().strftime("%H:%M:%S")

            # Convert dictionary to list of objects for the Web UI
            return [{"ip": ip, "time": timestamp} for ip, timestamp in clients.items()]
        except Exception as e:
            print(f"Conntrack error: {e}")
            return []
