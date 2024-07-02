from nicegui import ui, context
from contextlib import contextmanager
from dataclasses import dataclass

@dataclass
class Endpoint:
    title: str
    icon: str
    href: str

    def is_current(self):
        return context.client.page.path == self.href

endpoints = [
    Endpoint("Hem", "home", "/"),
    Endpoint("Driftdata för kärnreaktorer", "factory", "/reactor_operating_data"),
]

def menu_icon(endpoint: Endpoint):
    with ui.link("", endpoint.href).classes(f"rounded p-1 {'bg-slate-700' if endpoint.is_current() else 'hover:bg-secondary'}"):
        ui.tooltip(endpoint.title).props('anchor="center right" self="center start" :offset="[8, 0]"')
        ui.icon(endpoint.icon).classes("text-2xl text-primary")

@contextmanager
def frame():
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary="#7CB2CC", secondary="#53B689", accent="#111B1E", positive="#53B689")
    with ui.row().classes("no-wrap"):
        with ui.column().classes("-ml-4 -mt-4 w-12 pt-3 fixed h-screen bg-accent text-white items-center"):
            for endpoint in endpoints:
                if endpoint.is_current():
                    ui.page_title(f"{endpoint.title} | Core")
                menu_icon(endpoint)
        with ui.column().classes("ml-12"):
            yield