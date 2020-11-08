#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
# Created by kayrlas on August 17, 2019 (https://github.com/kayrlas)
# main_gui.py

from threading import Thread
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

from serial.serialutil import SerialException

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
        lf_status.pack(expand=False, fill="x", side="top")

        self.la_status = ttk.Label(
            master=lf_status,
            text="No Connection",
            background="lightgray")
        self.la_status.pack(expand=False, fill="x", side="left")

    def _wedget_com(self):
        # COM list pulldown, Reload button
        lf_com = ttk.LabelFrame(self.master, text="COM")
        lf_com.pack(expand=False, fill="x", side="top")

        self.cb_com = ttk.Combobox(
            master=lf_com,
            state="readonly",
            values=self.serialcom.find_comports())
        self.cb_com.current(0)
        self.cb_com.pack(expand=True, fill="x", side="left")

        self.btn_reload = ttk.Button(
            master=lf_com,
            text="Reload",
            command=self.reload_com_btn)
        self.btn_reload.pack(expand=False, fill="x", side="left")

    def _wedget_bps(self):
        # Baudrate list pulldown, Open button, Close button
        lf_bps = ttk.LabelFrame(self.master, text="Baudrate (bps)")
        lf_bps.pack(expand=False, fill="x", side="top")

        self.en_bps = ttk.Entry(
            master=lf_bps)
        self.en_bps.pack(expand=True, fill="x", side="left")

        self.btn_open = ttk.Button(
            master=lf_bps,
            text="Open",
            command=self.open_com_btn)
        self.btn_open.pack(expand=False, fill="x", side="left")

        self.btn_close = ttk.Button(
            master=lf_bps,
            text="Close",
            command=self.close_com_btn,
            state="disable")
        self.btn_close.pack(expand=False, fill="x", side="left")

    def _wedget_send(self):
        # String entry
        lf_send = ttk.LabelFrame(self.master, text="Text")
        lf_send.pack(expand=False, fill="x", side="top")

        self.en_send = ttk.Entry(
            master=lf_send,
            state="disable")
        self.en_send.pack(expand=True, fill="x", side="left")

        self.btn_send = ttk.Button(
            master=lf_send,
            text="Send",
            command=self.send_text_btn,
            state="disable")
        self.btn_send.pack(expand=False, fill="x", side="left")

    def _wedget_txrx(self):
        # TX RX
        pw_txrx = ttk.PanedWindow(self.master, orient="horizontal")
        pw_txrx.pack(expand=True, fill="both", side="top")

        # TX
        lf_tx = ttk.LabelFrame(pw_txrx, text="TX")
        lf_tx.pack(expand=True, fill="both", side="left")

        self.lb_tx = tk.Listbox(
            master=lf_tx,
            height=20,
            width=30,
            state="disable")
        sbx_tx = ttk.Scrollbar(
            master=lf_tx,
            orient=tk.HORIZONTAL,
            command=self.lb_tx.xview)
        sby_tx = ttk.Scrollbar(
            master=lf_tx,
            orient=tk.VERTICAL,
            command=self.lb_tx.yview)
        self.lb_tx.configure(
            xscrollcommand=sbx_tx.set,
            yscrollcommand=sby_tx.set)
        lf_tx.rowconfigure(0, weight=1)
        lf_tx.columnconfigure(0, weight=1)
        self.lb_tx.grid(row=0, column=0, sticky="nsew")
        sbx_tx.grid(row=1, column=0, sticky="ew")
        sby_tx.grid(row=0, column=1, sticky="ns")

        self.btn_txexp = ttk.Button(
            master=lf_tx,
            text="TX Export",
            command=self.exp_tx_btn,
            state="disable")
        self.btn_txexp.grid(row=2, column=0, sticky="n")

        # RX
        lf_rx = ttk.LabelFrame(pw_txrx, text="RX")
        lf_rx.pack(expand=True, fill="both", side="left")

        self.lb_rx = tk.Listbox(
            lf_rx,
            height=20,
            width=30,
            state="disable")
        sbx_rx = ttk.Scrollbar(
            master=lf_rx,
            orient=tk.HORIZONTAL,
            command=self.lb_rx.xview)
        sby_rx = ttk.Scrollbar(
            master=lf_rx,
            orient=tk.VERTICAL,
            command=self.lb_rx.yview)
        self.lb_rx.configure(
            xscrollcommand=sbx_rx.set,
            yscrollcommand=sby_rx.set)
        lf_rx.rowconfigure(0, weight=1)
        lf_rx.columnconfigure(0, weight=1)
        self.lb_rx.grid(row=0, column=0, sticky="nsew")
        sbx_rx.grid(row=1, column=0, sticky="ew")
        sby_rx.grid(row=0, column=1, sticky="ns")

        self.btn_rxexp = ttk.Button(
            master=lf_rx,
            text="RX Export",
            command=self.exp_rx_btn,
            state="disable")
        self.btn_rxexp.grid(row=2, column=0, sticky="n")

    def reload_com_btn(self):
        self.cb_com.config(values=self.serialcom.find_comports())

    def open_com_btn(self):
        self.serialcom.register_comport(deviceno=self.cb_com.current())

        try:
            _baudrate = int(self.en_bps.get())
            self.serialcom.serial.baudrate = _baudrate
            self.serialcom.serial.open()
        except ValueError:
            messagebox.showerror(
                title="Open comport was canceled",
                message="Parameters are out of range."
            )
        except SerialException:
            messagebox.showerror(
                title="Open comport was canceled",
                message="The device can not be configured."
            )
        else:
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

    def _start_serialread(self):
        self._th_sread = Thread(target=self._serial_read)
        self._th_sread.start()

    def _serial_read(self):
        while self.serialcom.serial.is_open:
            try:
                _recv_data = self.serialcom.serial.readline()
            except (TypeError, AttributeError, SerialException):
                messagebox.showerror(
                    title="Serial read was stopped",
                    message="Comport disconnected while reading."
                )
            else:
                if _recv_data != b'':
                    self.lb_rx.insert(
                        tk.END, _recv_data.strip().decode("utf-8"))
                    time.sleep(0.01)

    def close_com_btn(self):
        try:
            self.serialcom.close_comport()
            self._th_sread.join()
        except AttributeError:
            messagebox.showerror(
                title="Close comport was canceled",
                message="Comport has not been opened."
            )
        except ValueError:
            messagebox.showerror(
                title="Close comport was canceled",
                message="Parameters are out of range."
            )
        except SerialException as e:
            messagebox.showerror(
                title="Close comport was canceled",
                message="The device can not be configured. " + str(e)
            )
        else:
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

        if _fname == "" or _fname == ():
            messagebox.showwarning(
                title="No filename",
                message="Export was canceled."
            )
        else:
            with open(_fname, 'w') as f:
                for i in range(self.lb_tx.size()):
                    f.write(str(self.lb_tx.get(i)) + "\n")

    def exp_rx_btn(self):
        _fname = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save as",
            filetypes=[("text file", "*.txt"), ("all files", "*.*")])

        if _fname == "" or _fname == ():
            messagebox.showwarning(
                title="No filename",
                message="Export was canceled."
            )
        else:
            with open(_fname, 'w') as f:
                for i in range(self.lb_rx.size()):
                    f.write(str(self.lb_rx.get(i)) + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SerialComPython")

    Application(master=root)

    root.mainloop()
