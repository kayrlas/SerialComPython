#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
# Created by kayrlas on August 5, 2019 (https://github.com/kayrlas)
# serialcompy.py

import time
from threading import Thread

from serial import Serial
from serial.tools import list_ports
from serial.serialutil import SerialException


class SerialCom(object):
    """Class of serial communication

    Args:
        `baudrate (int)`: Serial communication symbol rate
        `timeout (float)`: Serial communication connection timeout

    Example:
    ```python
    if __name__ == "__main__":
        com = SerialCom()
        com.start_serialcom(9600, 0.1 , true)
    ```
    """

    def __init__(self, baudrate: int, timeout: float, write: bool):
        self.devices = []   # find_comports
        self.device = None  # select_comport
        self.serial = Serial(baudrate=baudrate, timeout=timeout)
        self.write = write


    def find_comports(self) -> int:
        """Save `list_ports.comports()` to `self.devices`

        Returns:
            `int`: Numbers of comports
        """
        _ports = list_ports.comports()
        self.devices = [info for info in _ports]
        return len(self.devices)


    def select_comport(self) -> bool:
        """Select comports from `self.devices` and save to `self.device`

        Returns:
            `bool`: Saving `self.device` successfully
        """

        _num_devices = self.find_comports()

        if _num_devices == 0:    # No device
            print("Device not found")
            return False
        elif _num_devices == 1:  # Only one device
            print("Only found %s" % self.devices[0])
            self.device = self.devices[0].device
            return True
        else:                    # Some devices
            print("Connected comports are as follows:")
            for i in range(_num_devices):
                print("%d : %s" % (i, self.devices[i]))

            _inp_num = input("Input the number of your target port >> ")

            if not _inp_num.isdecimal():
                print("%s is not a number!" % _inp_num)
                return False
            elif int(_inp_num) in range(_num_devices):
                self.device = self.devices[int(_inp_num)].device
                return True
            else:
                print("%s is out of the number!" % _inp_num)
                return False


    def open_comport(self) -> bool:
        """Open the comport

        Returns:
            `bool`: Open comport successfully
        """

        _select_com = self.select_comport()

        # Check device specified or not
        if (self.device is None) or (not _select_com):
            print("Device has not been specified yet!")
            return False
        else:
            self.serial.port = self.device

        # Input Yes/No
        _inp_yn = input("Open %s ? [Yes/No] >> " % self.serial.port).lower()
        if _inp_yn in ["y", "yes"]:    # YES
            print("Opening...")
            try:
                self.serial.open()
            except SerialException:
                print("%s was disconnected while you input [Yes/No]" % self.serial.port)
                return False
            else:
                return True
        elif _inp_yn in ["n", "no"]:   # NO
            print("Canceled")
            return False
        else:                          # Other than [Yes/No]
            print("Oops, you didn't enter [Yes/No]. Please try again.")
            return False


    def close_comport(self) -> bool:
        """Close the comport

        Returns:
            `bool`: Close comport successfully
        """

        try:
            self.serial.close()
        except AttributeError:
            print("open_comport has not been called yet!")
            return False
        else:
            print("Closing...")
            return True


    def serial_write(self):
        """Write strings to comport

        Returns:
            None
        """
        _format = "%Y/%m/%d %H:%M:%S"

        while self.serial.is_open:
            _t1 = time.strftime(_format, time.localtime())
            try:
                _send_data = input(_t1 + " (TX) >> ")
                self.serial.write(_send_data.encode("utf-8"))
            except EOFError:
                print("Sending texts canceled.")
                self.close_comport()
            except SerialException:
                print("%s was disconnected while writing texts" % self.serial.port)
                self.close_comport()
            else:
                time.sleep(1)


    def start_serialwrite(self):
        """Start `serial_write` in another thread

        Returns:
            None
        """
        self.th_swrite = Thread(target=self.serial_write)
        self.th_swrite.start()


    def start_serialcom(self) -> bool:
        """Start serial communication

        Returns:
            `bool`: Serial communication normally
        """
        _format = "%Y/%m/%d %H:%M:%S"

        if not self.open_comport():
            print("Cannot open the comport. Please try again.")
            return False

        if self.write:
            self.start_serialwrite()

        try:
            while self.serial.is_open:
                try:
                    _recv_data = self.serial.readline()
                except SerialException:
                    print("%s was disconnected while reading comport" % self.serial.port)
                    self.close_comport()
                else:
                    if _recv_data != b'':
                        _t1 = time.strftime(_format, time.localtime())
                        print(_t1 + " (RX) : " + _recv_data.strip().decode("utf-8"))
                        time.sleep(1)
        except KeyboardInterrupt:
            self.close_comport()

        if self.write:
            self.th_swrite.join()

        print("Comport has been closed. See you.")
        return True


    def get_device_list(self) -> list:
        return self.devices


    def get_device(self):
        return self.device


    def get_write_available(self) -> bool:
        return self.write


if __name__ == "__main__":
    com = SerialCom(baudrate=9600, timeout=0.1, write=True)
    com.start_serialcom()
