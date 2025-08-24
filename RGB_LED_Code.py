# RGB LED Code for CPR Compression Training Kit + Force Sensor Readings on OLED
# Code Credit: Yovani Coyazo | Adjustments/Debugging: Roxana Nevarez
# Assistance: ChatGPT, DeepSeek
import time
import board
import digitalio
import displayio
import terminalio
import analogio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

# --- OLED Display Setup ---
displayio.release_displays()
display = adafruit_displayio_ssd1306.SSD1306(
    displayio.I2CDisplay(board.I2C(), device_address=0x3C),
    width=128,
    height=64
)

text_area = label.Label(terminalio.FONT, text="", x=10, y=30)
display.root_group = displayio.Group()
display.root_group.append(text_area)

# --- Button, Buzzer, RBG LED, and Force Sensor Setup ---
button = digitalio.DigitalInOut(board.D2)
button.switch_to_input(pull=digitalio.Pull.UP)

buzzer = digitalio.DigitalInOut(board.D3)
buzzer.switch_to_output()

R = digitalio.DigitalInOut(board.D5) # red
G = digitalio.DigitalInOut(board.D6) # green
B = digitalio.DigitalInOut(board.D7) # blue
rgb = [R, G, B]
for led in rgb:
    led.switch_to_output()

force_sensor = analogio.AnalogIn(board.A0)

# Constants
TOO_LOW, TOO_HIGH = 60, 90 # force thresholds in Newtons

# --- Defining Functions ---
def show_text(t):
    text_area.text = t

def force_to_newtons(v):
    return v * (100 / 65535) # scale to 100N for testing

def countdown(s):
    for i in range(s, 0, -1):
        show_text(str(i))
        time.sleep(1)

def set_rgb(r, g, b):
    R.value = r
    G.value = g
    B.value = b

def beep_loop(duration):
    start = time.monotonic()
    show_text("Go!")
    
    while time.monotonic() - start < duration:
        # Beep Intervals
        buzzer.value = True
        time.sleep(0.1)
        buzzer.value = False

        # Read and Display Force on OLED
        f = force_to_newtons(force_sensor.value)
        show_text(f"{f:.1f}N")

        # Set RGB LED Color Based on Applied Force
        if f < TOO_LOW:
            set_rgb(False, False, True) # blue
        elif f > TOO_HIGH:
            set_rgb(True, False, False) # red
        else:
            set_rgb(False, True, False) # green

        time.sleep(0.5)

    show_text("Done!")
    set_rgb(False, False, False)  # turn off RGB LED

# --- Main Loop ---
while True:
    if not button.value:
        countdown(3)
        beep_loop(18)



