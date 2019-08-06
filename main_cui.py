#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
# Created by kayrlas on August 5, 2019 (https://github.com/kayrlas)
# main_cui.py

from serialcompy import SerialCom


if __name__ == "__main__":
    com = SerialCom(baudrate=9600, timeout=0.1, write=True)
    com.start_serialcom()
