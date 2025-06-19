#------------------------------------------------------------------------------------------------------
#>> Application for power monitoring of GPIO.
#------------------------------------------------------------------------------------------------------
import os
#------------------------------------------------------------------------------------------------------
GPIO_INPUT = 89    # GPIO line to monitor

#------------------------------------------------------------------------------------------------------
LOG_DIR = 'GPIO_logs'
os.makedirs(LOG_DIR, exist_ok=True)
log_file = None
GPIO_PATH = "/sys/class/gpio"

#--------------------------------------------------------------------------------------------------------
def export_gpio(pin):
    """Function used to export GPIO pin.
       :param pin: It specifies the input GPIO Number. 
       :return: None.
       """
    if not os.path.exists(f"{GPIO_PATH}/gpio{pin}"):
        with open(f"{GPIO_PATH}/export", 'w') as f:
            f.write(str(pin))
#---------------------------------------------------------------------------------------------------------
def unexport_gpio(pin):
    """Function used to unexport GPIO pin.
       :param pin: It specifies the input GPIO Number. 
       :return: None.
       """
    if os.path.exists(f"{GPIO_PATH}/gpio{pin}"):
        with open(f"{GPIO_PATH}/unexport", 'w') as f:
            f.write(str(pin))
#-----------------------------------------------------------------------------------------------------------
def read_gpio(pin):
    """Function used to read GPIO pin.
       :param pin: It specifies the input GPIO Number. 
       :return: None.
       """
    with open(f"{GPIO_PATH}/gpio{pin}/value", 'r') as f:
        return f.read().strip()
#------------------------------------------------------------------------------------------------------------- 
def set_gpio_direction_input(pin):
    """Function used to set the direction for GPIO pin.
       :param pin: It specifies the input GPIO Number. 
       :return: None.
       """
    with open(f"{GPIO_PATH}/gpio{pin}/direction", 'w') as f:
        f.write("in")
#--------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    from gpio_monitor import GPIO_Power_Monitor,set_led
  
    try:
        export_gpio(GPIO_INPUT)
        set_gpio_direction_input(GPIO_INPUT)

        set_led("led1",0)
        set_led("led2",0)

        GPIO_Power_Monitor()
    except Exception as e:
        print(f"Error: {e}")

#---------------------------------------------------------------------------------------------------------------
