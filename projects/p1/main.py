    # 4-to-1 MUX Chaining Implementation, Building a MUX from Gates, Course 3: Combination Gates and Multiplexers
    # Implement a Circuit, Breadboarding, Course 4: Connecting and Programming Embedded Systems
    # Implement Complex Circuit on Breadboard, Course 5: Synchronous and Asynchronous Processing
    # Add LED Toggle

import machine
import time
from utime import sleep

BUTTON_COUNT = 3
LED_COUNT = 9
INPUT_COUNT = 4

BUTTON_START_ID = 16
LED_GPIO_START = 7
last_button_time_stamp = 0
key_presses = []

MAX_IDLE_TIME_MS = 3000  # To clear incomplete button sequence after 3 seconds of inactivity


def pin_id(pin):
    # Example pin value format: Pin(GPIO16, mode=IN, pull=PULL_DOWN)
    return int(str(pin)[8:10].rstrip(","))


## Pin interrupt handler
#
# A function to handle pin interrupts
# Expects a machine.Pin type parameter
def interrupt_callback(pin):
    global last_button_time_stamp

    cur_button_ts = time.ticks_ms()
    button_press_delta = cur_button_ts - last_button_time_stamp

    # Handle debouncing
    if button_press_delta > 200:
        last_button_time_stamp = cur_button_ts
        key_presses.append(pin)

        # Which button has been pressed?
        print(f'key press: {pin_id(pin) - BUTTON_START_ID}')


def clear_key_presses_if_inactive():
    global key_presses
    global last_button_time_stamp

    if len(key_presses) != 0 and time.ticks_ms() - last_button_time_stamp > MAX_IDLE_TIME_MS:
        key_presses = []
        print(f'key press sequence cleared after {MAX_IDLE_TIME_MS // 1000} seconds of inactivity')


def main():
    global key_presses
    global last_button_time_stamp
    PASSCODE_LENGTH = 0
    
    # A tiny sleep to allow the first print to be displayed
    sleep(0.01)
    print('Program starting')

    # Set pins controlling multiplexers' select lines
    s1 = machine.Pin(28, machine.Pin.OUT)
    s0 = machine.Pin(27, machine.Pin.OUT)

    # Set pin reading multiplexers' input
    mux_in = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_DOWN)

    buttons = []
    for btn_idx in range(0, BUTTON_COUNT):
        buttons.append(machine.Pin(BUTTON_START_ID + btn_idx, machine.Pin.IN, machine.Pin.PULL_DOWN))
        buttons[-1].irq(trigger=machine.Pin.IRQ_FALLING, handler=interrupt_callback)

    PASS_CODE = [buttons[0], buttons[2], buttons[1]]
    PASSCODE_LENGTH = len(PASS_CODE)

    out_pins = []
    for out_id in range(0, LED_COUNT):
        out_pins.append(machine.Pin(LED_GPIO_START + out_id, machine.Pin.OUT))

    prev_binary_code = -1  # Init
    while True:
        binary_code = 0
        for selector_val in range(INPUT_COUNT):  # Scan each mux

            # +----+----+-----+
            # | S1 | S0 |  D  |
            # +----+----+-----+
            # |  0 |  0 |  0  |
            # |  0 |  1 |  1  |
            # |  1 |  0 |  2  |
            # |  1 |  1 |  3  |
            # +----+----+-----+

            # +----------------+--------------+
            # | Floor div (S1) |  Modulo (S0) |
            # +----------------+--------------+
            # |   0 // 2 = 0   |  0 % 2 = 0   |
            # |   1 // 2 = 0   |  1 % 2 = 1   |
            # |   2 // 2 = 1   |  2 % 2 = 0   |
            # |   3 // 2 = 1   |  3 % 2 = 1   |
            # +----------------+--------------+

            s1.value(selector_val // 2)  # TEST IF CORRECT!
            s0.value(selector_val % 2)

            sleep(0.02)

            # (2^1 * input_1) + (2^0 * input_0)
            binary_code += (pow(2, selector_val) * mux_in.value())

        if prev_binary_code != binary_code:
            prev_binary_code = binary_code
            print(f'selected output: {prev_binary_code}')
        sleep(0.1)

        if len(key_presses) >= PASSCODE_LENGTH:
            if key_presses[:PASSCODE_LENGTH] == PASS_CODE:
                print('correct passcode')
                
                if binary_code < LED_COUNT:
                    print(f'toggling: {binary_code}')
                    out_pins[binary_code].toggle()
                else:
                    print(f'invalid output: {binary_code}, ' + \
                    f'valid range: 0-{len(out_pins) - 1}, doing nothing')
            
            else:
                print('wrong passcode')
            print('')
            key_presses = key_presses[PASSCODE_LENGTH:]

        clear_key_presses_if_inactive()


if __name__ == "__main__":
    main()
