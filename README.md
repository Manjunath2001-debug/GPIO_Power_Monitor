
# GPIO Power Monitoring Application

This application is used to monitor the state of a GPIO line on a Linux system (typically embedded platforms like debian .). It logs **HIGH/LOW** changes with **timestamps from RTC** and manages status LEDs and network checks.

---

## 🧱 Folder Structure

```
.
├── main.py             # Contains GPIO setup, RTC time functions, and execution entry
├── gpio_monitor.py     # Main GPIO monitoring logic and LED/network handling
├── GPIO_logs/          # Directory to store generated log files
```

---

## Functional Overview

### GPIO Monitoring
- **GPIO_INPUT = 89** is monitored for changes.
- On state change (HIGH or LOW), a log is written/appended to a CSV file in `./GPIO_logs/`.

### Real-Time Clock (RTC)
- Uses `/dev/rtc0` to get accurate system time.
- Avoids system time drift.

### LED Indications
- **LED1**: Power GPIO status.
  - ON when GPIO is HIGH.
  - OFF when GPIO is LOW.
- **LED2**: Network connectivity.
  - ON when connected.
  - Blinks when network is down.

### Network Connectivity
- Pings Google's DNS (8.8.8.8) to verify Internet access.
- Retries up to 3 times before deciding it's disconnected.

---

## 📁 Log File Format

Log files are named:
```
power_monitor_YYYY_MM_DD_HH_MM_SS.csv
```

### Contents:
```
Timestamp : 2025-06-14 10:32:45
State : HIGH
Timestamp : 2025-06-14 10:34:10
State : LOW
```

---

## Main Components

### main.py

Responsible for:
- Exporting and configuring GPIO.
- Getting RTC time.
- Starting `GPIO_Power_Monitor`.

```python
export_gpio(GPIO_INPUT)
set_gpio_direction_input(GPIO_INPUT)
GPIO_Power_Monitor()
```

---

### gpio_monitor.py

Contains the main loop:

```python
def GPIO_Power_Monitor():
    while True:
        current_state = read_gpio(GPIO_INPUT)
        rtc_time = read_rtc_time()

        if current_state != previous_state:
            # Log timestamp and state
            # Control LED1
```

### Network Check:

```python
def Network_Connectivity():
    ping 8.8.8.8 -W 1 -c 1
```

---

## Usage

### 1. Run the Application

```bash
sudo python3 main.py
```

Ensure script is run with **root privileges** to access GPIO and RTC.

---

## Requirements

- Linux with `/sys/class/gpio` and `/dev/rtc0` support
- LED entries: `/sys/class/leds/led1` and `/sys/class/leds/led2`
- Python 3
- Permissions for GPIO and RTC access

---

## Debug Tips

- **RTC not working?** Check `/dev/rtc0` exists.
- **GPIO not responding?** Confirm the pin number is correct and accessible.
- **LED not lighting?** Check permissions and `led_name`.

