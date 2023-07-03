# This was just something fun to put together while I was procrastinating making the board
# logic for the macro system I have now made.

# In gist this program just lets you toggle the controlling of the brightness with the encoder,
# as well as pick a random color each time you press a key (and then turn it off when pressed again).

from adafruit_macropad import MacroPad
import random

macropad = MacroPad()
macropad.pixels.brightness = 0.5

LED_INTERVAL = 0.05
brightness_mode = True
encoder_prev = 0
toggled_leds = [False] * 12

color_options = [0, 127, 255]

text_lines = macropad.display_text(title="Testing Macropad")
text_lines[0].text = f"Adj. brightness: {brightness_mode}"
text_lines[1].text = f"Brightess lvl: {macropad.pixels.brightness}"

while True:
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        brightness_mode = not brightness_mode
        text_lines[0].text = "Adj. brightness: {}".format(brightness_mode)
        if brightness_mode:
            encoder_prev = macropad.encoder

    if macropad.encoder is not encoder_prev and brightness_mode:
        changed = False
        if macropad.encoder > encoder_prev:
            if macropad.pixels.brightness + LED_INTERVAL <= 1:
                macropad.pixels.brightness = round(
                    macropad.pixels.brightness + LED_INTERVAL, 2
                )
                changed = True
        else:
            if macropad.pixels.brightness - LED_INTERVAL >= 0:
                macropad.pixels.brightness = round(
                    macropad.pixels.brightness - LED_INTERVAL, 2
                )
                changed = True

        if changed:
            text_lines[1].text = f"Brightess lvl: {macropad.pixels.brightness}"

        encoder_prev = macropad.encoder

    joe = macropad.keys.events.get()
    if joe:
        if joe.pressed and not toggled_leds[joe.key_number]:
            macropad.pixels[joe.key_number] = (
                random.choice(color_options),
                random.choice(color_options),
                random.choice(color_options),
            )
            toggled_leds[joe.key_number] = True
        elif joe.pressed:
            macropad.pixels[joe.key_number] = 0x000000
            toggled_leds[joe.key_number] = False

    text_lines.show()
