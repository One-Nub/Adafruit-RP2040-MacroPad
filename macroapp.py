from adafruit_macropad import MacroPad


# Controls the stepping interval of the LED brightness.
DEFAULT_LED_INTERVAL = 0.05


class MacroKey:
    def __init__(self, key_num: int, label: str, color=0xFFFFFF, action: function = None):
        """
        Creates a macro key instance.

        Key_num - Corresponds to the key on the macropad (1-12)
        label - Name for the key to show on the display (6 chars at most preferred)
        color - Hex code that the key should light up as
        action - Function that handles what the key does on press.
            This function will be passed the current macropad instance.
            That way things like macropad.keyboard, macropad.mouse, etc, can be used.
        """
        self.key_num = key_num - 1
        self.label = label
        self.color = color
        self.action = action


class Layer:
    def __init__(self, name: str, keys: list[MacroKey]):
        """
        Creates a layer that contains MacroKeys.

        name - The name of the layer, this is displayed at the top of the macropad. Cut off at 20 characters.
        keys - List of MacroKeys for this layer.
        """
        self.name = name
        self.keys = keys


class MacroApp:
    def __init__(
        self,
        default_brightness: float = 0.5,
        brightness_step_interval: float = DEFAULT_LED_INTERVAL,
    ):
        """Initializes all necessary variables for the macropad to run."""
        self.layers = list()
        self.current_layer = None

        self.switch_layer_state = False

        self.macropad = MacroPad()
        self.macropad.pixels.brightness = default_brightness
        self.text_lines = self.macropad.display_text()

        self.macropad.display.auto_refresh = False
        self.macropad.pixels.auto_write = False

        self.prev_encoder_state = 0

        self.brightness_step = brightness_step_interval

    def add_layer(self, layer: Layer):
        """Adds a layer to the macropad."""
        self.layers.append(layer)

    def setup(self):
        """
        Initializes the first layer. Must be run before the program starts looping.
        """
        layers = self.layers
        if not layers:
            raise RuntimeError(
                "No layers were specified. Make sure to add at least one before running the code!"
            )

        self.current_layer = layers[0]
        self.switch_layer(0)

    def switch_layer(self, layer_index: int):
        """
        Handles the logic of switching between layers.
        This consists of updating the current_layer variable, as well as changing the
        display output & updating the neopixel colors.

        layer_index - index of the layer that is being switched to.
        """
        macropad = self.macropad

        macropad.keys.reset()
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()

        # macropad.pixels.show()

        self.current_layer = self.layers[layer_index]
        layer: Layer = self.current_layer

        text = f"{layer.name[:20] : ^20}"
        if self.switch_layer_state:
            text += "*"
        self.text_lines[0].text = text

        key_labels = dict()
        for i in range(12):
            key = None
            for x in layer.keys:
                if x.key_num == i:
                    key = x
                    break

            label = "X"
            color = 0x000000
            if key:
                label = "X" if not key.label else key.label
                color = key.color

            macropad.pixels[i] = color
            key_labels[i] = f"{label: ^7}"

        self.text_lines[1].text = f"{key_labels[0]}{key_labels[1]}{key_labels[2]}"
        self.text_lines[2].text = f"{key_labels[3]}{key_labels[4]}{key_labels[5]}"
        self.text_lines[3].text = f"{key_labels[6]}{key_labels[7]}{key_labels[8]}"
        self.text_lines[4].text = f"{key_labels[9]}{key_labels[10]}{key_labels[11]}"

    def check_encoder(self):
        """
        Logic related to checking the encoder state.

        Checks if the encoder has been pressed, which switches the state between moving between
        layers or adjusting the brightness of the neopixels.

        Also checks for the rotation of the encoder, and handles the according functionality
        as determined by the encoder state (default is to change neopixel brightness, alternative is to change layers.)
        """
        macropad = self.macropad

        macropad.encoder_switch_debounced.update()
        if macropad.encoder_switch_debounced.pressed:
            self.switch_layer_state = not self.switch_layer_state

            text = self.text_lines[0].text
            # Show an asterisk on screen when in layer switching mode.
            if self.switch_layer_state and not text.endswith("*"):
                text += "*"
            elif not self.switch_layer_state and text.endswith("*"):
                text = text[:-1]

            self.text_lines[0].text = text
            return

        encoder = macropad.encoder
        # Only handle if the encoder isn't where we left it.
        if encoder is not self.prev_encoder_state:
            if self.switch_layer_state:
                layer_max = len(self.layers)
                if layer_max == 1:
                    return

                current_layer_index = 0
                for layer_idx in range(len(self.layers)):
                    layer = self.layers[layer_idx]

                    if layer == self.current_layer:
                        current_layer_index = layer_idx
                        break

                # Make sure we're not overshooting.
                if encoder > self.prev_encoder_state and (current_layer_index + 1) < layer_max:
                    self.switch_layer(current_layer_index + 1)
                elif encoder < self.prev_encoder_state and (current_layer_index - 1) >= 0:
                    self.switch_layer(current_layer_index - 1)
            else:
                # Default state is to adjust the brightness of the neopixels.
                brightness = macropad.pixels.brightness
                step_interval = self.brightness_step
                if encoder > self.prev_encoder_state and brightness + step_interval <= 1:
                    macropad.pixels.brightness = round(macropad.pixels.brightness + step_interval, 2)
                elif encoder < self.prev_encoder_state and brightness - step_interval >= 0:
                    macropad.pixels.brightness = round(macropad.pixels.brightness - step_interval, 2)

            self.prev_encoder_state = macropad.encoder

    def check_keypress(self):
        """Handle the logic for triggering keypress action functions."""
        macropad = self.macropad

        key_event = macropad.keys.events.get()
        if key_event:
            if key_event.pressed:
                layer: Layer = self.current_layer

                layer_key = None
                for x in layer.keys:
                    if x.key_num == key_event.key_number:
                        layer_key = x
                        break

                if layer_key and layer_key.action:
                    layer_key.action(self.macropad)
