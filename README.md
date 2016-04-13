# Bluetooth proximity script

A python script to determine the signal strength of the specified bluetooth address, and call the url with signal strength added to the end. If the device is out of range the value returned is -256, if it is touching the bluetooth dongle it will be around 38. The script uses hci to determine the signal strength.

Example usage:

`./proximity --addresses "DD:4D:E3:F3:81:AB,DD:4D:E3:F3:81:CC" --urls "http://127.0.0.1/bluetooth-proximity?phone=me&value=,http://127.0.0.1/bluetooth-proximity?phone=you&value="`

The tool is based on the work of:
* https://github.com/dagar/bluetooth-proximity
* https://github.com/timhughes/bluetooth-proximity