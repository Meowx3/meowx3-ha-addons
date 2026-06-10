# GPSD Chrony Gemma4 T1 Add-on for Home Assistant

This add-on enables your Home Assistant system to interface with a u-blox 7 USB GPS receiver via gpsd.

## Features

* Reads NMEA data from the u-blox 7 GPS receiver
* Streams GPS information (coordinates, time, satellites) to stdout
* Optionally integrates chrony for precise time synchronization
* Supports multiple architectures: amd64, armhf, aarch64

## Configuration

In your `configuration.yaml`, you can specify:

```yaml
gpsd_chrony_gemma4_t1:
  device_path: "/dev/ttyACM0"
  baud_rate: 9600
```

## Usage

Once installed and started, the add-on will output raw NMEA sentences from the GPS receiver to its logs. You can access these logs via the Home Assistant UI or by using `tail -f /config/logs/gpsd_chrony_gemma4_t1.log` if you have set up logging.

## Hardware Requirements

* u-blox 7 USB GPS receiver
* Raspberry Pi or other system with USB and serial support
```

### ✅ Optional: `meowx3-ha-addons/gpsd-chrony-gemma4-t1/rootfs/etc/gpsd/gpsd.conf`
```conf
# /etc/gpsd/gpsd.conf - configuration file for gpsd
DEVICES="/dev/ttyACM0"
GPSD_OPTIONS="-n"