#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
# Created by kayrlas on August 17, 2019 (https://github.com/kayrlas)
# main_gui.py

from threading import Thread
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from serialcompy import SerialCom


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.serialcom = SerialCom(baudrate=9600, timeout=0.1, writemode=True)
        self.create_wedgets()

    def create_wedgets(self):
        self._wedget_statusbar()
        self._wedget_com()
        self._wedget_bps()
        self._wedget_send()
        self._wedget_txrx()

    def _wedget_statusbar(self):
        # StatusBar
        lf_status = ttk.LabelFrame(self.master, text="Status Bar")
        lf_status.pack(expand=False, side="top")

        self.la_status = ttk.Label(
            master=lf_status,
            width=62,
            text="No Connection",
            background="lightgray")
        self.la_status.pack(expand=False, side="left")

    def _wedget_com(self):
        # COM list pulldown, Reload button
        lf_com = ttk.LabelFrame(self.master, text="COM")
        lf_com.pack(expand=False, side="top")

        self.cb_com = ttk.Combobox(
            master=lf_com,
            state="readonly",
            values=self.serialcom.find_comports(),
            width=46)
        self.cb_com.current(0)
        self.cb_com.pack(expand=False, side="left")

        self.btn_reload = ttk.Button(
            master=lf_com,
            text="Reload",
            command=self.reload_com_btn)
        self.btn_reload.pack(expand=False, side="left")

    def _wedget_bps(self):
        # Baudrate list pulldown, Open button, Close button
        lf_bps = ttk.LabelFrame(self.master, text="Baudrate (bps)")
        lf_bps.pack(expand=False, side="top")

        self.en_bps = ttk.Entry(
            master=lf_bps,
            width=36)
        self.en_bps.pack(expand=False, side="left")

        self.btn_open = ttk.Button(
            master=lf_bps,
            text="Open",
            command=self.open_com_btn)
        self.btn_open.pack(expand=False, side="left")

        self.btn_close = ttk.Button(
            master=lf_bps,
            text="Close",
            command=self.close_com_btn,
            state="disable")
        self.btn_close.pack(expand=False, side="left")

    def _wedget_send(self):
        # String entry
        lf_send = ttk.LabelFrame(self.master, text="Text")
        lf_send.pack(expand=False, side="top")

        self.en_send = ttk.Entry(
            master=lf_send,
            width=49,
            state="disable")
        self.en_send.pack(expand=False, side="left")

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Send",
            command=self.send_text_btn,
            state="disable")
        self.btn_send.pack(expand=False, side="left")

    def _wedget_txrx(self):
        # TX RX
        pw_txrx = ttk.PanedWindow(self.master, orient="horizontal")
        pw_txrx.pack(expand=False, side="top")

        ## TX
        lf_tx = ttk.LabelFrame(pw_txrx, text="TX")
        lf_tx.pack(expand=False, side="left")

        self.lb_tx = tk.Listbox(
            master=lf_tx,
            height=20,
            width=30,
            state="disable")
        self.lb_tx.pack(expand=False)

        self.btn_txexp = ttk.Button(
            master=lf_tx,
            text="TX Export",
            command=self.exp_tx_btn,
            state="disable")
        self.btn_txexp.pack(expand=False, side="right")

        ## RX
        lf_rx = ttk.LabelFrame(pw_txrx, text="RX")
        lf_rx.pack(expand=False, side="right")

        self.lb_rx = tk.Listbox(
            lf_rx,
            height=20,
            width=30,
            state="disable")
        self.lb_rx.pack(expand=False)

        self.btn_rxexp = ttk.Button(
            lf_rx,
            text="RX Export",
            command=self.exp_rx_btn,
            state="disable")
        self.btn_rxexp.pack(expand=False, side="right")

    def reload_com_btn(self):
        self.cb_com.config(values=self.serialcom.find_comports())

    def open_com_btn(self):
        _device = self.serialcom.devices[self.cb_com.current()].device
        _baudrate = self.en_bps.get()
        if not self.serialcom.register_comport(device=_device):
            print("Cannot specify the comport. Please try again.")
        elif _baudrate.isdecimal() or _baudrate is "":
            if _baudrate.isdecimal():
                self.serialcom.serial.baudrate = int(_baudrate)

            self.serialcom.serial.open()
            self.la_status.config(text="Opening", background="lightgreen")
            self.en_send.config(state="normal")
            self.btn_send.config(state="normal")
            self.btn_close.config(state="normal")
            self.lb_rx.config(state="normal")
            self.btn_rxexp.config(state="normal")
            self.cb_com.config(state="disable")
            self.btn_reload.config(state="disable")
            self.en_bps.config(state="disable")
            self.btn_open.config(state="disable")
            if self.serialcom.writemode:
                self.lb_tx.config(state="normal")
                self.btn_txexp.config(state="normal")

            self._start_serialread()

        else:
            print("Text in the baudrate entry is not a number.")

    def _start_serialread(self):
        self._th_sread = Thread(target=self._serial_read)
        self._th_sread.start()

    def _serial_read(self):
        while self.serialcom.serial.is_open:
                try:
                    _recv_data = self.serialcom.serial.readline()
                except (TypeError, AttributeError):
                    print("Comport disconnected while reading")
                else:
                    if _recv_data != b'':
                        self.lb_rx.insert(tk.END, _recv_data.strip().decode("utf-8"))
                        time.sleep(1)

    def close_com_btn(self):
        self.serialcom.close_comport()
        self._th_sread.join()
        self.cb_com.config(state="readonly")
        self.btn_reload.config(state="normal")
        self.en_bps.config(state="normal")
        self.btn_open.config(state="normal")
        self.la_status.config(text="Disconnected", background="lightgray")
        self.en_send.config(state="disable")
        self.btn_send.config(state="disable")
        self.btn_close.config(state="disable")
        self.lb_rx.config(state="disable")
        self.btn_rxexp.config(state="disable")
        if self.serialcom.writemode:
            self.lb_tx.config(state="disable")
            self.btn_txexp.config(state="disable")

    def send_text_btn(self):
        _send_data = self.en_send.get()
        self.serialcom.serial.write(_send_data.encode("utf-8"))
        self.lb_tx.insert(tk.END, _send_data)
        self.en_send.delete(0, tk.END)

    def exp_tx_btn(self):
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        with open(_fname, 'w') as f:
            for i in range(self.lb_tx.size()):
                f.write(str(self.lb_tx.get(i)) + "\n")

    def exp_rx_btn(self):
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        with open(_fname, 'w') as f:
            for i in range(self.lb_rx.size()):
                f.write(str(self.lb_rx.get(i)) + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SerialComPython")

    Application(master=root)

    root.mainloop()
