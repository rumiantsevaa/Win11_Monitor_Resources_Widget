# Win11_Monitor_Resources_Widget
## A Python GUI application to monitor system performance, displaying real-time CPU, GPU, RAM, and disk usage information in a draggable PyQt5 widget.

![image](https://github.com/user-attachments/assets/7cf7b0e3-4257-4651-aa50-f3db41dba3f5)

## System Performance Monitor is a Python application that provides real-time monitoring of CPU, GPU, RAM, and disk usage. The information is displayed in a draggable PyQt5 widget that remains on top of other windows.

# Features

* Real-time Monitoring: Display current CPU, GPU, RAM, and disk usage.
* Temperature Monitoring: Get temperatures of CPU and GPU.
* Active Process Info: Display the name of the active process and its FPS (if available).
* Draggable Widget: The monitoring widget can be moved around the screen.
* Disk Usage: Detailed information about each disk partition.

# Prerequisites
* Python 3.x
* PyQt5
* psutil
* GPUtil
* pywin32
* WMI

![image](https://github.com/user-attachments/assets/9f1fc300-e571-4bd0-b37e-e01937c12ee4)


# Code Overview
* main.py

This file contains functions to:

- Check if the script is run with administrator privileges.
- Launch OpenHardwareMonitor.
- Retrieve CPU and GPU temperatures.
- Get the active window process name.
- Get disk usage.
- Collect system performance information.

* gui.py

This file creates a PyQt5 widget to display system performance information:

- Initializes a frameless, always-on-top window.
- Uses a grid layout to organize information into two columns.
- Periodically updates the displayed information.
- Allows the widget to be dragged around the screen.

