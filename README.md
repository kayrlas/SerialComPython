# SerialComPython
[![GitHub issues](https://img.shields.io/github/issues/kayrlas/SerialComPython)](https://github.com/kayrlas/SerialComPython/issues)
[![GitHub forks](https://img.shields.io/github/forks/kayrlas/SerialComPython)](https://github.com/kayrlas/SerialComPython/network)
[![GitHub stars](https://img.shields.io/github/stars/kayrlas/SerialComPython)](https://github.com/kayrlas/SerialComPython/stargazers)
[![GitHub license](https://img.shields.io/github/license/kayrlas/SerialComPython)](https://github.com/kayrlas/SerialComPython/blob/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/kayrlas/SerialComPython?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fkayrlas%2FSerialComPython)

Serial Communication Python Class. CUI and GUI both are available.

## Strong Points
- Using a thread, TX and RX both are available at the same time.
- Execute `serial.close()` and disconnect safely.

## serialcompy (Python Code)
Serial Communication Python Class.
### Imports
- time: Standard library
- threading: Standard library
- serial (pySerial): Third-Party library (`pip install pyserial`)
### API
```
SerialCom (class)              // Args: baudrate, timeout, writemode
├── devices (variable)         // comports list  
├── device (variable)          // selected comport  
├── serial (variable)          // serial.Serial instance  
├── writemode (variable)       // boolean serial write accept  
├── find_comports (method)     // Find comports and save to `self.devices`  
├── select_comport (method)    // Select a comport from list  
├── register_comport (method)  // Save a comport to `self.serial.port`  
├── open_comports (method)     // Open the comport  
├── close_comports (method)    // Close ther comport  
├── serial_write (method)      // Write strings to comport  
├── start_serialwrite (method) // Start `serial_write` in another thread  
├── serial_read (method)       // Read strings from comport  
├── start_serialcom (method)   // Start serial communication  
├── start_serialcom_option (method) // Start serial communication (using option args)  
├── get_found_devices (method)      // Return `self.devices`  
├── get_selected_device (method)    // Return `self.device`  
└── get_write_available (method)    // Return `self.writemode`
```

## main_gui (Python Code)
1. Startup window.  
![Window Start](/img/01-start.png "01-start")  

2. Select a comport from the combobox. If you connect a device after the startup, push "Reload" button and check the combobox again.  
![Window Select](/img/02-select.png "02-select")  

3. After input a baudrate, push "Open" button. If the "Baudrate" entry is empty, the rate is 9600 bps by default or the last bps you open the port.  
![Window Open](/img/03-open.png "03-open")

4. Input string to "Text" entry and push "Send" button. "TX" listbox is a sending history and "RX" listbox is a receiving history. Pushing "TX Export" button or "RX Export" button, you can save these histories as a text file.  
![Window Send](/img/04-send.png "04-send")  

5. To disconnect, push "Close" button.  
![Window Close](/img/05-close.png "05-close")  

## main_cui (Python Code)
1. Select a comport.  
2. Input "yes", "y" or "no", "n".  
3. Serial communication starts.  
4. To disconnect, input Ctrl+C.  
![CUI Start](/img/00-cui.png "00-cui")  

## SerialCom (Arduino Code)
- 9600 bps serial communication
- Once get a string, send it.
