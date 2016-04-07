#!/usr/bin/env python

import fcntl
import struct
import array
import bluetooth
import bluetooth._bluetooth as bt
import urllib2

import time
import os
import sys
import datetime

bluetooth_addresses = sys.argv[1].split(',')
urls = sys.argv[2].split(',')
sleep_if_connected = sys.argv[3]
sleep_if_not_connected = sys.argv[4]
debug = 1

def bluetooth_rssi(addr):
    # Open hci socket
    hci_sock = bt.hci_open_dev()
    hci_fd = hci_sock.fileno()

    # Connect to device (to whatever you like)
    bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    bt_sock.settimeout(10)
    result = bt_sock.connect_ex((addr, 1))  # PSM 1 - Service Discovery

    try:
        # Get ConnInfo
        reqstr = struct.pack("6sB17s", bt.str2ba(addr), bt.ACL_LINK, "\0" * 17)
        request = array.array("c", reqstr )
        handle = fcntl.ioctl(hci_fd, bt.HCIGETCONNINFO, request, 1)
        handle = struct.unpack("8xH14x", request.tostring())[0]

        # Get RSSI
        cmd_pkt=struct.pack('H', handle)
        rssi = bt.hci_send_req(hci_sock, bt.OGF_STATUS_PARAM,
                               bt.OCF_READ_RSSI, bt.EVT_CMD_COMPLETE, 4, cmd_pkt)
        rssi = struct.unpack('b', rssi[3])[0]

        # Close sockets
        bt_sock.close()
        hci_sock.close()

        return rssi

    except:
        return None

# assume phone is initially far away
rssi = []
rssi_prev1 = []
rssi_prev2 = []
for (i, bluetooth_address) in bluetooth_addresses:
    rssi[i] = -256
    rssi_prev1[i] = -256
    rssi_prev2[i] = -256

while True:
    # get rssi reading for address
    for (i, bluetooth_address) in bluetooth_addresses:
        rssi[i] = bluetooth_rssi(bluetooth_address)
        if rssi[i] == None:
            rssi[i] = -256

        if debug:
            print datetime.datetime.now(), rssi[i], rssi_prev1[i], rssi_prev2[i]

        if rssi[i] == rssi_prev1[i] == rssi_prev2[i]:
            print "No change detected"
        else:
            urllib2.urlopen(urls[i] + rssi[i]).read()

        rssi_prev1[i] = rssi[i]
        rssi_prev2[i] = rssi_prev1[i]

        if rssi[i] == -256:
            time.sleep(sleep_if_not_connected)
        else:
            time.sleep(sleep_if_connected)
