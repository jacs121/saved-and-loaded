import random
from messages import MESSAGES

from prompt_toolkit.application import Application
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.shortcuts.dialogs import BaseStyle, _T, get_app, functools

from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings

from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.widgets import Dialog, Label, Button, TextArea
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.cursor_shapes import CursorShape

def fixed_button_dialog(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    buttons: list[tuple[str, _T]] = [],
    style: BaseStyle | None = None,
) -> Application[_T]:

    def button_handler(v: _T) -> None:
        get_app().exit(result=v)

    dialog = Dialog(
        title=title,
        body=Label(text=text, dont_extend_height=True),
        buttons=[
            Button(text=t, handler=functools.partial(button_handler, v), width=len(t)+2)
            for t, v in buttons
        ],
        with_background=True,
    )

    # Key bindings.
    bindings = KeyBindings()
    bindings.add("tab")(focus_next)
    bindings.add("s-tab")(focus_previous)

    return Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
        cursor=CursorShape.UNDERLINE
    )


def uppercaseDialogInput(title:str, text:str, style: Style):
    # Create the TextArea (input field)
    input_field = TextArea(multiline=False)

    # Key bindings for uppercase enforcement
    kb = KeyBindings()

    @kb.add("<any>")
    def _(event: KeyPressEvent):
        """Force all typed letters to uppercase."""
        data = event.data
        buf = event.app.current_buffer
        if data.isalpha() or data == " ":
            buf.insert_text(data.upper())
        elif data == "\r":  # Enter key
            buf.validate_and_handle()

    # Define OK and Cancel button behavior
    result = {"text": None}

    def ok_handler():
        result["text"] = input_field.text
        app.exit(result["text"])

    def cancel_handler():
        app.exit(None)

    ok_button = Button(text="OK", handler=ok_handler)
    cancel_button = Button(text="Cancel", handler=cancel_handler)

    # Build the dialog layout
    dialog = Dialog(
        title=title,
        body=HSplit([
            Label(text=text),
            input_field,
        ]),
        buttons=[ok_button, cancel_button],
        with_background=True,
    )

    # Create the Application
    app = Application(
        layout=Layout(dialog),
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=True,
        cursor=CursorShape.UNDERLINE
    )

    # Run it
    return app.run()

class IntegerValidator(Validator):
    def __init__(self, min_value: int = None, max_value: int = None):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, document):
        text = document.text
        if text and ((not text.isdigit()) or (self.max_value and self.max_value < int(text)) or (self.min_value and self.min_value > int(text))):  # Only attempt conversion if there's text
            raise ValidationError(
                message=random.choice(MESSAGES['invalid_input']),
                cursor_position=len(text)  # Keep cursor at the end
            )
