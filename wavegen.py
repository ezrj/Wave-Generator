import signal
import math
import time
import board
import busio
import adafruit_mcp4725 as adafruit
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
BTN = 6
GPIO.setup([BTN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit.MCP4725(i2c)

def square(amplitude, frequency):
    period = 1.0 / frequency
    half_period = period / 2.0

    while True:
        if (GPIO.input(BTN)):
            return
        dac.raw_value = int(amplitude)
        time.sleep(half_period)
        dac.raw_value = 0
        time.sleep(half_period)


def sin(amplitude, frequency):
    sampling_rate = 1000
    amplitude = int(amplitude / 2)
    time_between_samples = 1.0 / sampling_rate
    time_between_samples = 1.0 / sampling_rate * 0.3

    while True:
        if (GPIO.input(BTN)):
            return
        for i in range(sampling_rate):
            angle = 2 * math.pi * frequency * i / sampling_rate
            value = amplitude * math.sin(angle)
            scaled_value = int((value + amplitude) / (2 * amplitude) * 4095)
            dac.raw_value = scaled_value
            time.sleep(time_between_samples)


def triangle(amplitude, frequency):
    period = 1.0 / frequency
    half_period = period / 2.0
    amplitude = int(amplitude / 2)
    sampling_rate = 1000
    num_samples_half_period = int(sampling_rate * half_period)
    time_between_samples = 1.0 / sampling_rate * 0.3

    while True:
        if (GPIO.input(BTN)):
            return
        for i in range(num_samples_half_period):
            value = (2 * amplitude * i) / num_samples_half_period
            dac.raw_value = int(value)
            time.sleep(time_between_samples)

        for i in range(num_samples_half_period):
            value = 2 * amplitude - (2 * amplitude * i) / num_samples_half_period
            dac.raw_value = int(value)
            time.sleep(time_between_samples)

def menu(arg):
    dac.raw_value = 0
    wave = int(input("\nOptions: \n 1) Square \n 2) Sine \n 3) Triangle \n 4) Quit \n Choice: "))
    if (wave < 1) or (wave > 4):
        print("Enter one of the options")
        return

    if (wave == 4):
        sys.exit() 

    amplitude = int(input("Choose an amplitude (0-4095): "))
    if amplitude < 0 or amplitude > 4095:
        print("Amplitude must be between 0 and 4095.")
        return

    frequency = int(input("Choose a frequency (Hz) below 20: "))
    if frequency > 20:
        print("Frequency must be 20 Hz or lower.")
        return

    if (wave == 1):
        square(amplitude, frequency)

    if (wave == 2):
        sin(amplitude, frequency)

    if (wave == 3):
        triangle(amplitude, frequency)


while True:
    if (GPIO.input(BTN)):
        break
    time.sleep(0.001)


while True:
    menu(1)
