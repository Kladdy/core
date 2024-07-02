from nicegui import ui
import plotly.graph_objects as go
from datetime import timedelta

from models import datetime_converter
from models.reactor_operating_data import ReactorOperatingData

@ui.page('/other_page')
def other_page():
    ui.label('Welcome to the other side')

    ui.link('Visit other page', other_page)
    ui.link('Visit dark page', dark_page)

    with ui.grid(columns=2):
        for reactor in ReactorOperatingData.objects.all():
            reactor: ReactorOperatingData

            x = [datetime_converter.utc_to_local(data_point.timestamp) for data_point in reactor.data_points]
            y = [data_point.value_percent for data_point in reactor.data_points]

            # Loop over all x values. If there is more than 20 minutes between two x values, insert that time in x and a None value in y
            for i in range(len(x) - 1):
                if x[i] + timedelta(minutes=20) < x[i + 1]:
                    x.insert(i + 1, x[i] + timedelta(minutes=20))
                    y.insert(i + 1, None)

            fig = go.Figure(go.Scatter(x=x, y=y), layout=go.Layout(yaxis=dict(range=[0, 100])))
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            with ui.card():
                with ui.row().classes('items-center justify-between'):
                    ui.label(reactor.reactor_name).classes('text-lg font-bold font-mono')
                    ui.circular_progress(round(reactor.data_points[-1].value_percent), min=0, max=100, size="md")
                ui.plotly(fig).classes('w-96 h-40')

@ui.page('/dark_page', dark=True)
def dark_page():
    ui.label('Welcome to the dark side')

    ui.link('Visit other page', other_page)
    ui.link('Visit dark page', dark_page)