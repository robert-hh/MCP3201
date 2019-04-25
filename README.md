# ADS8718: Python class for the MCP3201 AD-converter

This is a very short and simple class. It uses the SPI bus for the interface. That
ensures that the tight timing requirements of the MCP3201 are met.

## Constructor

### adc = MCP3201(spi, \*, baudrate = 800000, vref = 2.5)

- spi is an SPI object which has to be created by the caller. Just the Pins have to be assigned by the caller.
The init method of the class sets baud rate, phase, polarity and word size.
- baudrate defines the baud rate of the SPI. the default is 800000.
The valid range is 200kHz through 800 kHz. These boundaries are silently enforced by the class.
- vref is the reference voltage, used to calculate the voltage value. Vref is only 
used for the calculation of the equivalent voltage.

## Methods

### value = adc.value()

Retrieves the adc raw value using the setting of the constructor. The returned
value is in the range of 0 - 4095

### volt = adc.voltage()

Reads the adc value and return the equivalent voltage. This is based on the vref
value set in the constructor. The formula is:   
    voltage = vref * value / 4096

## Interface

The MCP3201 is connected to the SPI bus signals. There is no CS needed. The
connection consist of:

|Micro|MCP3201|
|:---|:---|
|MOSI|CS (5)|
|MISO|DOUT (6)|
|CLK|CLK (7)|

The MCP3201 needs a Vcc of 2.7 to 5V. For connecting to a 3.3V device, when operated
at 5V, insert a resistor of about 4.7 kOhm between MISO and DATA.

## Example

```
# Drive the MCP3201 ADC using SPI
# Connections:
# xxPy | MCP3201
# -----|-------
# P10  |  CLK
# P11  |  CONV
# P14  |  DATA add a series resistor of about 4.7k between DATA and P14
#
from machine import SPI
from MCP3201 import MCP3201

spi = SPI(0, SPI.MASTER)
vref = 3.3 # Assumed that Vdd is 3.3v and Vref is connected to Vdd
ads = MCP3201(spi, vref=vref)

while True:
    # start a conversion and get the result back
    value = ads.value()
    volt = vref * value / 4096

    print(value, volt)
    res= input("Next: ")
    if res == "q":
        break
```
