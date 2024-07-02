from nicegui import ui

from pages import theme

@ui.page('/')
def index():
    with theme.frame():
        ui.label("Hello, world!")