# Repurposed from https://github.com/waveshareteam/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd2in13_V4.py
# Repurposed from https://github.com/waveshareteam/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epdconfig.py

import time
import logging
from PIL import Image

# Display resolution
EPD_WIDTH = 122
EPD_HEIGHT = 250

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EPD:
    def __init__(self, reset_pin=17, dc_pin=25, busy_pin=24, cs_pin=8):
        self.reset_pin = reset_pin
        self.dc_pin = dc_pin
        self.busy_pin = busy_pin
        self.cs_pin = cs_pin
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def reset(self):
        logger.debug("Resetting EPD")
        self.digital_write(self.reset_pin, 1)
        time.sleep(0.020)
        self.digital_write(self.reset_pin, 0)
        time.sleep(0.002)
        self.digital_write(self.reset_pin, 1)
        time.sleep(0.020)

    def digital_write(self, pin, value):
        logger.debug(f"Setting pin {pin} to {value}")
        # Placeholder for actual pin control logic
        pass

    def digital_read(self, pin):
        logger.debug(f"Reading pin {pin}")
        # Placeholder for actual pin read logic
        return 0

    def delay_ms(self, delaytime):
        logger.debug(f"Delaying for {delaytime} ms")
        time.sleep(delaytime / 1000.0)

    def send_command(self, command):
        logger.debug(f"Sending command: {command}")
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        # Placeholder for SPI write logic
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        logger.debug(f"Sending data: {data}")
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        # Placeholder for SPI write logic
        self.digital_write(self.cs_pin, 1)

    def send_data2(self, data):
        logger.debug(f"Sending data2: {data}")
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        # Placeholder for SPI write logic
        self.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        logger.debug("e-Paper busy")
        while self.digital_read(self.busy_pin) == 1:  # 0: idle, 1: busy
            self.delay_ms(10)
        logger.debug("e-Paper busy release")

    def TurnOnDisplay(self):
        logger.debug("Turning on display")
        self.send_command(0x22)  # Display Update Control
        self.send_data(0xf7)
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def TurnOnDisplay_Fast(self):
        logger.debug("Turning on display fast")
        self.send_command(0x22)  # Display Update Control
        self.send_data(0xC7)  # fast:0x0c, quality:0x0f, 0xcf
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def TurnOnDisplayPart(self):
        logger.debug("Turning on display part")
        self.send_command(0x22)  # Display Update Control
        self.send_data(0xff)  # fast:0x0c, quality:0x0f, 0xcf
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def SetWindow(self, x_start, y_start, x_end, y_end):
        logger.debug(f"Setting window from ({x_start}, {y_start}) to ({x_end}, {y_end})")
        self.send_command(0x44)  # SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((x_start >> 3) & 0xFF)
        self.send_data((x_end >> 3) & 0xFF)

        self.send_command(0x45)  # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def SetCursor(self, x, y):
        logger.debug(f"Setting cursor to ({x}, {y})")
        self.send_command(0x4E)  # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(x & 0xFF)

        self.send_command(0x4F)  # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)

    def init(self):
        logger.debug("Initializing EPD")
        self.reset()
        self.ReadBusy()
        self.send_command(0x12)  # SWRESET
        self.ReadBusy()

        self.send_command(0x01)  # Driver output control
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x3c)
        self.send_data(0x05)

        self.send_command(0x21)  # Display update control
        self.send_data(0x00)
        self.send_data(0x80)

        self.send_command(0x18)
        self.send_data(0x80)

        self.ReadBusy()
        return 0

    def getbuffer(self, image):
        logger.debug("Getting buffer from image")
        img = image
        imwidth, imheight = img.size
        if imwidth == self.width and imheight == self.height:
            img = img.convert('1')
        elif imwidth == self.height and imheight == self.width:
            img = img.rotate(90, expand=True).convert('1')
        else:
            logger.warning(f"Wrong image dimensions: must be {self.width}x{self.height}")
            return [0x00] * (int(self.width / 8) * self.height)

        buf = bytearray(img.tobytes('raw'))
        return buf

    def display(self, image):
        logger.debug("Displaying image")
        self.send_command(0x24)
        self.send_data2(image)
        self.TurnOnDisplay()

    def display_fast(self, image):
        logger.debug("Displaying image fast")
        self.send_command(0x24)
        self.send_data2(image)
        self.TurnOnDisplay_Fast()

    def displayPartial(self, image):
        logger.debug("Displaying image partial")
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(1)
        self.digital_write(self.reset_pin, 1)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x01)  # Driver output control
        self.send_data(0xF9)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x24)  # WRITE_RAM
        self.send_data2(image)
        self.TurnOnDisplayPart()

    def displayPartBaseImage(self, image):
        logger.debug("Displaying part base image")
        self.send_command(0x24)
        self.send_data2(image)

        self.send_command(0x26)
        self.send_data2(image)
        self.TurnOnDisplay()

    def Clear(self, color=0xFF):
        logger.debug("Clearing display")
        if self.width % 8 == 0:
            linewidth = int(self.width / 8)
        else:
            linewidth = int(self.width / 8) + 1

        self.send_command(0x24)
        self.send_data2([color] * int(self.height * linewidth))
        self.TurnOnDisplay()

    def sleep(self):
        logger.debug("Entering sleep mode")
        self.send_command(0x10)  # enter deep sleep
        self.send_data(0x01)

        self.delay_ms(2000)
        # Placeholder for module exit logic