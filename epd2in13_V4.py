# Repurposed from https://github.com/waveshareteam/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd2in13_V4.py
# Repurposed from https://github.com/waveshareteam/e-Paper/blob/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epdconfig.py
import os
import time
import logging
import spidev
import gpiozero
from ctypes import CDLL
from PIL import Image

# Display resolution
EPD_WIDTH = 122
EPD_HEIGHT = 250

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RaspberryPi:
    # Pin definition
    RST_PIN = 17
    DC_PIN = 25
    CS_PIN = 8
    BUSY_PIN = 24
    PWR_PIN = 18
    MOSI_PIN = 10
    SCLK_PIN = 11

    def __init__(self):
        self.SPI = spidev.SpiDev()
        self.GPIO_RST_PIN = gpiozero.LED(self.RST_PIN)
        self.GPIO_DC_PIN = gpiozero.LED(self.DC_PIN)
        self.GPIO_PWR_PIN = gpiozero.LED(self.PWR_PIN)
        self.GPIO_BUSY_PIN = gpiozero.Button(self.BUSY_PIN, pull_up=False)

    def digital_write(self, pin, value):
        logger.debug(f"Setting pin {pin} to {value}")
        if pin == self.RST_PIN:
            if value:
                self.GPIO_RST_PIN.on()
            else:
                self.GPIO_RST_PIN.off()
        elif pin == self.DC_PIN:
            if value:
                self.GPIO_DC_PIN.on()
            else:
                self.GPIO_DC_PIN.off()
        elif pin == self.PWR_PIN:
            if value:
                self.GPIO_PWR_PIN.on()
            else:
                self.GPIO_PWR_PIN.off()

    def digital_read(self, pin):
        logger.debug(f"Reading pin {pin}")
        if pin == self.BUSY_PIN:
            return self.GPIO_BUSY_PIN.value
        elif pin == self.RST_PIN:
            return self.RST_PIN.value
        elif pin == self.DC_PIN:
            return self.DC_PIN.value
        elif pin == self.PWR_PIN:
            return self.PWR_PIN.value

    def delay_ms(self, delaytime):
        logger.debug(f"Delaying for {delaytime} ms")
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        logger.debug(f"Writing byte: {data}")
        self.SPI.writebytes(data)

    def spi_writebyte2(self, data):
        logger.debug(f"Writing bytes: {data}")
        self.SPI.writebytes2(data)

    def DEV_SPI_write(self, data):
        self.DEV_SPI.DEV_SPI_SendData(data)

    def DEV_SPI_nwrite(self, data):
        self.DEV_SPI.DEV_SPI_SendnData(data)

    def DEV_SPI_read(self):
        return self.DEV_SPI.DEV_SPI_ReadData()

    def module_init(self, cleanup=False):
        self.GPIO_PWR_PIN.on()

        if cleanup:
            find_dirs = [
                os.path.dirname(os.path.realpath(__file__)),
                '/usr/local/lib',
                '/usr/lib',
            ]
            self.DEV_SPI = None
            for find_dir in find_dirs:
                val = int(os.popen('getconf LONG_BIT').read())
                logger.debug(f"System is {val} bit")
                if val == 64:
                    so_filename = os.path.join(find_dir, 'DEV_Config_64.so')
                else:
                    so_filename = os.path.join(find_dir, 'DEV_Config_32.so')
                if os.path.exists(so_filename):
                    self.DEV_SPI = CDLL(so_filename)
                    break
            if self.DEV_SPI is None:
                raise RuntimeError('Cannot find DEV_Config.so')

            self.DEV_SPI.DEV_Module_Init()

        else:
            # SPI device, bus = 0, device = 0
            self.SPI.open(0, 0)
            self.SPI.max_speed_hz = 4000000
            self.SPI.mode = 0b00
        return 0

    def module_exit(self, cleanup=False):
        logger.debug("SPI end")
        self.SPI.close()

        self.GPIO_RST_PIN.off()
        self.GPIO_DC_PIN.off()
        self.GPIO_PWR_PIN.off()
        logger.debug("Close 5V, Module enters 0 power consumption ...")

        if cleanup:
            self.GPIO_RST_PIN.close()
            self.GPIO_DC_PIN.close()
            self.GPIO_PWR_PIN.close()
            self.GPIO_BUSY_PIN.close()

epdconfig = RaspberryPi()

class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def reset(self):
        logger.debug("Resetting EPD")
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20)

    def send_command(self, command):
        logger.debug(f"Sending command: {command}")
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        logger.debug(f"Sending data: {data}")
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data2(self, data):
        logger.debug(f"Sending data2: {data}")
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte2(data)
        epdconfig.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        logger.debug("e-Paper busy")
        while epdconfig.digital_read(self.busy_pin) == 1:  # 0: idle, 1: busy
            epdconfig.delay_ms(10)
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
        if epdconfig.module_init() != 0:
            return -1
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

    def init_fast(self):
        logger.debug("Initializing EPD fast")
        if epdconfig.module_init() != 0:
            return -1
        self.reset()

        self.send_command(0x12)  # SWRESET
        self.ReadBusy()

        self.send_command(0x18)  # Read built-in temperature sensor
        self.send_command(0x80)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x22)  # Load temperature value
        self.send_data(0xB1)
        self.send_command(0x20)
        self.ReadBusy()

        self.send_command(0x1A)  # Write to temperature register
        self.send_data(0x64)
        self.send_data(0x00)

        self.send_command(0x22)  # Load temperature value
        self.send_data(0x91)
        self.send_command(0x20)
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
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(1)
        epdconfig.digital_write(self.reset_pin, 1)

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

        epdconfig.delay_ms(2000)
        epdconfig.module_exit()

### END OF FILE ###
