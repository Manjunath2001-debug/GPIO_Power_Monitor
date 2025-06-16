import csv,os,time,subprocess
from main import read_rtc_time,LOG_DIR,log_file,GPIO_INPUT,unexport_gpio
from main import read_gpio
#------------------------------------------------------------------------------------------------
def GPIO_Power_Monitor():
    """
        Function to monitor the gpio state.
        
        :param input_line: specifies the input gpio line.
        :param previous: specifies the previous state.
        :return: None.
        """
    global log_file
    previous = read_gpio(GPIO_INPUT)

    print(f"Starting GPIO monitoring on line {GPIO_INPUT} (initial state: {previous})")
    try:
        print("Monitoring started. Press Ctrl+C to stop.")
        while True:
            current = read_gpio(GPIO_INPUT)
            rtc_now = read_rtc_time()

            if not rtc_now:
                print("RTC time not available. Skipping this cycle.")
                time.sleep(0.2)
                continue

            time.sleep(0.1)

            if current != previous:
                timestamp = rtc_now.strftime('%Y-%m-%d %H:%M:%S')
                #print(f"[DEBUG]-current time : {timestamp}")
                previous = current

                if current == "1": # State is High
                    set_led("led2",1) # Turn LED_1 on
                    
                    filename = f"power_monitor_{rtc_now.strftime('%Y_%m_%d_%H_%M_%S')}.csv"
                    log_file = os.path.join(LOG_DIR, filename)

                    with open(log_file, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f"Timestamp : {timestamp}"])
                        writer.writerow([f"State : HIGH"])

                    print(f"[HIGH] Logged new file: {filename} | LED ON")

                else:
                    set_led("led2",0)  # Turn LED_1 OFF

                    if not log_file or not os.path.exists(log_file):
                        # To get the latest file
                        csv_files = [f for f in os.listdir(LOG_DIR) if f.startswith("power_monitor_") and f.endswith(".csv")]
                        if csv_files:
                            latest_file = max(csv_files, key=lambda x: os.path.getctime(os.path.join(LOG_DIR, x)))
                            log_file = os.path.join(LOG_DIR, latest_file)
                            print(f"[LOW] Found latest file: {latest_file}")
                        else:
                            print("[LOW] No log files found in directory. | LED OFF")
                            continue  # Skip 

                    # Append LOW state to the latest file
                    with open(log_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f"Timestamp : {timestamp}"])
                        writer.writerow([f"State : LOW"])
                        print(f"[LOW] Appended to: {os.path.basename(log_file)} | LED OFF")

            network_status = Network_Connectivity(3, 1)
    
            if network_status:
                print("[DEBUG]:Inside network connection")
                set_led("led1", 1)      
            else:
            # Blink LED2 only if network is down
                set_led("led1", 1)
                time.sleep(0.2)
                set_led("led1", 0)
                time.sleep(0.2)
                
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        unexport_gpio(GPIO_INPUT)
#-----------------------------------------------------------------------------------------------------------------

def Network_Connectivity(retries=3, delay=1):
    """
    Checks network connectivity by pinging a known public DNS server (Google's 8.8.8.8).
    
    :param retries: Number of retry attempts.
    :param delay: Delay between retries in seconds.
    :return: True if network is reachable, else False.
    """
    for attempt in range(1, retries + 1):
        try:
            #print(f"[DEBUG] Checking network... Attempt {attempt}")
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", "8.8.8.8"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if result.returncode == 0:
                return True
        except Exception as e:
            print(f"[ERROR] Network check failed: {e}")
        
        time.sleep(delay)

    print("[WARNING] Network unreachable after retries.")
    return False
#------------------------------------------------------------------------------------------------------------------
def set_led(led_name, value):
    """
    Function to set the LED ON(HIGH) and OFF(LOW).
    
    :param led_name: specifies LED name (for eg, led1/led2).
    :param value: specifies HIGH or LOW to set the LED.
    :return: None.
    """
    try:
        subprocess.run(['sh', '-c', f'echo {value} > /sys/class/leds/{led_name}/brightness'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not set {led_name} to {value}: {e}")

#--------------------------------------------------------------------------------------------------------------------