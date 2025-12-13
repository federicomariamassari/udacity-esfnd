# Udacity Embedded Systems Fundamentals Nanodegree

## [Certificate of Completion](https://www.udacity.com/certificate/e/c3518fe2-07f8-11ef-acf8-bf6b5235762d)

![Certificate of Completion](certificate-of-completion.png)

# Core Projects

## [Project: Embedded Input Reader](projects/p1/p1-embedded-input-reader.md)

__Acquired familiarity with:__ Wokwi, MicroPython, Raspberry Pi Pico.

### Overview

As the capstone project for the Embedded Systems Fundamentals Nanodegree, I built a digital interface leveraging the Raspberry Pi Pico microcontroller to manage the state of LEDs based on input from switches and by entering a passcode.

__[Link to Wokwi project](https://wokwi.com/projects/402048833643264001)__ | __[Link to code](./projects/p1/main.py)__

### Output

Users can control the state of the four slide switches located at the top of the interface. Each switch represents a binary digit, and when a switch is activated, the corresponding yellow LED is turned on to visually indicate its state. The system accepts the three-digit passcode 0-2-1, and the input is processed only when this correct code is entered via the pushbuttons.

![Embedded Input Reader Output](./projects/p1/img/mov0.gif)
