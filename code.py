from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

from macroapp import MacroApp, Layer, MacroKey


RED = 0xFF0000
GREEN = 0x00FF00
BLUE = 0x0000FF
ORANGE = 0xE3690B
PURPLE = 0x8000FF
PINK = 0xFF00EA


def send_consumer_code(mp: MacroPad, key: ConsumerControlCode):
    mp.consumer_control.send(key)


def send_key(mp: MacroPad, key: Keycode):
    if isinstance(key, list):
        mp.keyboard.send(*key)
    else:
        mp.keyboard.send(key)


def send_string(mp: MacroPad, output: str):
    mp.keyboard.write(output)


keypad_layer = [
    MacroKey(1, "KP 7", action=lambda mp: send_key(mp, Keycode.KEYPAD_SEVEN)),
    MacroKey(2, "KP 8", action=lambda mp: send_key(mp, Keycode.KEYPAD_EIGHT)),
    MacroKey(3, "KP 9", action=lambda mp: send_key(mp, Keycode.KEYPAD_NINE)),
    #
    MacroKey(4, "KP 4", action=lambda mp: send_key(mp, Keycode.KEYPAD_FOUR)),
    MacroKey(5, "KP 5", action=lambda mp: send_key(mp, Keycode.KEYPAD_FIVE)),
    MacroKey(6, "KP 6", action=lambda mp: send_key(mp, Keycode.KEYPAD_SIX)),
    #
    MacroKey(7, "KP 1", action=lambda mp: send_key(mp, Keycode.KEYPAD_ONE)),
    MacroKey(8, "KP 2", action=lambda mp: send_key(mp, Keycode.KEYPAD_TWO)),
    MacroKey(9, "KP 3", action=lambda mp: send_key(mp, Keycode.KEYPAD_THREE)),
    #
    MacroKey(10, "DELETE", action=lambda mp: send_key(mp, Keycode.BACKSPACE), color=RED),
    MacroKey(11, "KP 0", action=lambda mp: send_key(mp, Keycode.KEYPAD_ZERO)),
    MacroKey(12, "ENTER", action=lambda mp: send_key(mp, Keycode.KEYPAD_ENTER), color=GREEN),
]

play_pause_color = RED


def play_pause(mp: MacroPad):
    global play_pause_color

    play_pause_color = BLUE if play_pause_color == RED else RED
    mp.pixels[4] = play_pause_color

    send_consumer_code(mp, ConsumerControlCode.PLAY_PAUSE)


media_layer = [
    MacroKey(1, "NUMLK", action=lambda mp: send_key(mp, Keycode.KEYPAD_NUMLOCK)),
    MacroKey(2, "", color=0),
    MacroKey(3, "", color=0),
    #
    MacroKey(
        4,
        "PREV",
        action=lambda mp: send_consumer_code(mp, ConsumerControlCode.SCAN_PREVIOUS_TRACK),
        color=ORANGE,
    ),
    MacroKey(5, "PLY/PSE", action=play_pause, color=play_pause_color),
    MacroKey(
        6,
        "NEXT",
        action=lambda mp: send_consumer_code(mp, ConsumerControlCode.SCAN_NEXT_TRACK),
        color=ORANGE,
    ),
    #
    MacroKey(7, "", color=0),
    MacroKey(8, "", color=0),
    MacroKey(9, "", color=0),
    #
    MacroKey(10, "", color=0),
    MacroKey(11, "", color=0),
    MacroKey(12, "", color=0),
]


utils_layer = [
    MacroKey(1, "ESC", action=lambda mp: send_key(mp, Keycode.ESCAPE), color=0),
    MacroKey(2, "", color=0),
    MacroKey(3, "", color=0),
    #
    MacroKey(
        4,
        "COLOR",
        action=lambda mp: send_key(mp, [Keycode.WINDOWS, Keycode.SHIFT, Keycode.C]),
        color=PURPLE,
    ),
    MacroKey(
        5,
        "TSKMGR",
        action=lambda mp: send_key(mp, [Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE]),
        color=PURPLE,
    ),
    MacroKey(
        6,
        "WINTAB",
        action=lambda mp: send_key(mp, [Keycode.WINDOWS, Keycode.TAB]),
        color=PURPLE,
    ),
    #
    MacroKey(
        7,
        "VD L",
        action=lambda mp: send_key(mp, [Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW]),
        color=ORANGE,
    ),
    MacroKey(8, "SS", action=lambda mp: send_key(mp, [Keycode.WINDOWS, Keycode.SHIFT, Keycode.S])),
    MacroKey(
        9,
        "VD R",
        action=lambda mp: send_key(mp, [Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW]),
        color=ORANGE,
    ),
    #
    MacroKey(10, "COPY", action=lambda mp: send_key(mp, [Keycode.CONTROL, Keycode.C]), color=PINK),
    MacroKey(11, "CUT", action=lambda mp: send_key(mp, [Keycode.CONTROL, Keycode.X]), color=PINK),
    MacroKey(12, "PASTE", action=lambda mp: send_key(mp, [Keycode.CONTROL, Keycode.V]), color=PINK),
]


app = MacroApp()
app.add_layer(Layer("Layer 0 - Keypad", keypad_layer))
app.add_layer(Layer("Layer 1 - Media", media_layer))
app.add_layer(Layer("Layer 2 - Utilities", utils_layer))
app.setup()

while True:
    app.check_encoder()
    app.check_keypress()

    app.text_lines.show()
    app.macropad.pixels.show()
    app.macropad.display.refresh()
