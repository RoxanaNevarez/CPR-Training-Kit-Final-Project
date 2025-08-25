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

# --- OLED Setup ---
displayio.release_displays()
display = adafruit_displayio_ssd1306.SSD1306(
    displayio.I2CDisplay(board.I2C(), device_address=0x3C),
    width=128,
    height=64
)

# --- Button and Buzzer Setup ---
button = digitalio.DigitalInOut(board.D2)
button.switch_to_input(pull=digitalio.Pull.UP)

buzzer = digitalio.DigitalInOut(board.D3)
buzzer.switch_to_output()

# --- RGB LED Setup ---
R = digitalio.DigitalInOut(board.D8) # red
G = digitalio.DigitalInOut(board.D6) # green
B = digitalio.DigitalInOut(board.D4) # blue
rgb = [R, G, B]
for led in rgb:
    led.switch_to_output()

# --- Force Sensor Setup ---
force_sensor = analogio.AnalogIn(board.A0)

# --- Display Setup ---
# text size must be kept small to avoid memory allocation errors
text_area = label.Label(terminalio.FONT, text="", x=10, y=30)
display.root_group = displayio.Group()
display.root_group.append(text_area)

# --- Constants ---
TOO_LOW, TOO_HIGH = 40, 90 # force thresholds in Newtons for testing purposes only

# --- Defining Functions ---
def show_text(t):
    text_area.text = t

def force_to_newtons(v):
    return v * (100 / 65535)

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
        # --- Beep Pace ---
        buzzer.value = True
        time.sleep(0.1)
        buzzer.value = False

        # --- Force Value ---
        f = force_to_newtons(force_sensor.value)
       # show_text(f"{f:.1f}N") - option to include force values in newtons

        # set RGB LED color based on force range
        if f < TOO_LOW:
            set_rgb(False, False, True) # blue
            show_text("Low!")
        elif f > TOO_HIGH:
            set_rgb(True, False, False) # red
            show_text("High!")      
        else:
            set_rgb(False, True, False) # green
            show_text("Good!")
        time.sleep(0.5)

    show_text("Done!")
    set_rgb(False, False, False) # turn off RGB LED

# --- Main Loop ---
while True:
    if not button.value:
        countdown(3)
        beep_loop(18)
