#
# Simple class for the MCP3201 ADC using SPI
# connections:
# xxPy | MCP3201
# -----|-------
# CLK  |  CLK
# MOSI |  CS
# MISO |  DATA
#
from machine import SPI

class MCP3201:
    def __init__(self, spi, *, vref=3.3, baudrate=800000):
        self.spi = spi
        self.vref = vref
        self.buf = bytearray(2)
        # The CS signal for the ADC is created by the bit pattern for MOSI
        # self conv defines the timing relation of
        # CS and the ADC conversion
        # Alternative values for earlier CS:
        # b'\x00\x00' or b'\xc0\x00' or b'\xe0\x00'
        self.conv = b'\x80\x00'
        baudrate = min(max(100000, baudrate), 800000)
        self.spi.init(SPI.MASTER, baudrate=baudrate,
                      polarity=1, phase=1, bits=16)

    def value(self):
        self.spi.write_readinto(self.conv, self.buf)
        return ((self.buf[0] << 8) | self.buf[1]) & 0xfff

    def voltage(self):
        return self.vref * self.value() / 4096
