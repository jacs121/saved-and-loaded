from prompt_toolkit.styles import Style

# Define all styles in one place
STYLES = {
    'default': Style.from_dict({
        'dialog': 'bg:''#362A2A',
        'dialog.text': '#ffffff',
        'dialog frame.label': 'bg:'"#000000"' '"#FFFFFF",
        'dialog.body': 'bg:''#000000'' ''#ffffff',
        'dialog.shadow': 'bg:''#1a1a1a',
        'button': "#ffffff",
        'button.focused': 'bg:''#ffffff'' ''#000000',
        'text-area': 'bg:''#000000'
    }),
    'live': Style.from_dict({
        'dialog': 'bg:''#ff0000',
        'dialog.text': '#9b0000',
        'dialog frame.label': 'bg:'"#000000"' '"#9b0000",
        'dialog.body': 'bg:''#000000'' ''#ffffff',
        'dialog.shadow': 'bg:''#1a1a1a',
        'button': '#9b0000',
        'button.focused': 'bg:'"#ff0000"' ''#000000',
        'text-area': 'bg:''#000000'
    }),
    'blank': Style.from_dict({
        'dialog': 'bg:''#808080',
        'dialog.text': '#ffffff',
        'dialog frame.label': 'bg:'"#000000"' '"#FFFFFF",
        'dialog.body': 'bg:''#000000'' ''#ffffff',
        'dialog.shadow': 'bg:''#1a1a1a',
        'button': '#ffffff',
        'button.focused': 'bg:''#ffffff'' ''#000000',
        'text-area': 'bg:''#000000'
    }),
    'game_over': Style.from_dict({
        'dialog': 'bg:''#000000',
        'dialog.text': '#ffffff',
        'dialog frame.label': 'bg:'"#000000"' '"#FFFFFF",
        'dialog.body': 'bg:'"#1D1D1D"' ''#ffffff',
        'dialog.shadow': 'bg:''#1a1a1a',
        'button': '#ffffff',
        'button.focused': 'bg:''#ffffff'' ''#000000',
        'text-area': 'bg:''#000000'
    }),
    'play_again': Style.from_dict({
        'dialog': 'bg:''#000000',
        'dialog.text': '#ffffff',
        'dialog frame.label': 'bg:'"#000000"' '"#FFFFFF",
        'dialog.body': 'bg:''#1D1D1D'' ''#ffffff',
        'dialog.shadow': 'bg:''#1a1a1a',
        'button': '#ffffff',
        'button.focused': 'bg:''#ffffff'' ''#000000',
        'text-area': 'bg:''#000000'
    }),
    'stats': Style.from_dict({
        'dialog': 'bg:''#362A2A',
        'dialog.text': '#ffffff',
        'dialog frame.label': 'bg:'"#4C3838"' '"#FFFFFF",
        'dialog.body': 'bg:''#000000'' ''#ffffff',
        'dialog.shadow': 'bg:''#1a1a1a',
        'button': '#000000',
        'button.focused': 'bg:''#ffffff'' ''#000000',
        'text-area': 'bg:''#000000'
    }),
    'item': Style.from_dict({
        'dialog': 'bg:''#4A3900'' ''#b4b4b4',
        'dialog.text': "#b4b4b4",
        'dialog frame.label': 'bg:'"#000000"' '"#FFFFFF",
        'dialog.body': 'bg:''#000000'' ''#b4b4b4',
        'dialog.shadow': 'bg:''#1a1a1a',
        'button': "#3a3424",
        'button.focused': 'bg:'"#ffffff",
        'text-area': 'bg:''#000000'
    })
}
