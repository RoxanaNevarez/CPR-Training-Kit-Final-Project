# CPR Compression Training Kit Using 3 LEDs - No Force Value Display on OLED
# Collaboration with: Thejo Tattala, Matthew Hwang, Yovani Coyazo
import time
import board
import digitalio
import displayio
import terminalio
import analogio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

# --- LEDs on Metro M0 ---
L1 = digitalio.DigitalInOut(board.D4) # red
L3 = digitalio.DigitalInOut(board.D6) # green
L5 = digitalio.DigitalInOut(board.D8) # yellow
leds = [L1, L3, L5] # too strong, just right, too weak
for led in leds:
    led.direction = digitalio.Direction.OUTPUT

# --- OLED Display Setup ---
displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 64
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

text_area = label.Label(terminalio.FONT, text="", x=10, y=30)
text_group = displayio.Group()
text_group.append(text_area)
display.root_group = text_group

def show_text(text):
    text_area.text = text

def countdown(seconds):
    for i in range(seconds, 0, -1):
        show_text(str(i))
        time.sleep(1)

# --- Button Setup ---
button = digitalio.DigitalInOut(board.D2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# --- Buzzer Setup ---
buzzer = digitalio.DigitalInOut(board.D3)
buzzer.direction = digitalio.Direction.OUTPUT

# --- Force Sensor Setup ---
force_sensor = analogio.AnalogIn(board.A0)

def force_in_pounds(raw_value):
    return (raw_value / 65535) * 105  # Scale to 105 for testing - outputs would be close to pounds


# --- Beeping Control Variables ---
beeping = False
beep_start = 0
beep_interval = 0.6  # 100 BPM: 0.1s ON, 0.5s OFF
last_beep_time = 0
buzzer_on = False

# --- Main Loop ---
while True:
    # --- Start Beeping Cycle ---
    if not button.value and not beeping:
        countdown(3)
        show_text("Go!")
        beeping = True
        beep_start = time.monotonic()
        last_beep_time = time.monotonic()

    # --- Beeping Logic (Non-Blocking) ---
    if beeping:
        current_time = time.monotonic()

        # End Beeping After 18 Seconds
        if current_time - beep_start > 18:
            beeping = False
            buzzer.value = False
            show_text("Done!")

        # Toggle Buzzer Between On (0.1s) and Off (0.5s) = 0.6s Total per Beat
        elif buzzer_on and current_time - last_beep_time >= 0.1:
            buzzer.value = False
            buzzer_on = False
            last_beep_time = current_time
        elif not buzzer_on and current_time - last_beep_time >= 0.5:
            buzzer.value = True
            buzzer_on = True
            last_beep_time = current_time


    # --- Read Force Sensor and Update LEDs ---
    force_raw = force_sensor.value
    force_lb = force_in_pounds(force_raw)
    if 100 <= force_lb <= 120: 
        # Just Right
        L5.value = False
        L1.value = False
        L3.value = True # green LED on
    elif 0 < force_lb < 100: 
        # Too Weak
        L5.value = True # yellow LED on
        L1.value = False
        L3.value = False
    elif force_lb > 120:
        # Too Strong
        L5.value = False
        L1.value = True # red LED on
        L3.value = False
    else:
        # No Force
        L5.value = False
        L1.value = False
        L3.value = False

    time.sleep(0.01)  # short CPU delay

