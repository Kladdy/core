from nicegui import ui
import plotly.graph_objects as go
from datetime import timedelta

from models import datetime_converter
from models.reactor_operating_data import ReactorOperatingData
from pages import theme

@ui.page('/reactor_operating_data')
def reactor_operating_data():
    with theme.frame():
        with ui.row():
            for reactor in ReactorOperatingData.objects.all():
                reactor: ReactorOperatingData

                x = [datetime_converter.utc_to_local(data_point.timestamp) for data_point in reactor.data_points]
                y = [data_point.value_percent for data_point in reactor.data_points]

                # Time window to allow values to not exist over before inserting null values
                time_window = 180

                # Loop over all x values. If there is more than time_window minutes between two x values, insert that time in x and a None value in y. This breaks the plot line if data is missing. Updates are expected every 10 minutes. 
                i = 0
                while i < len(x) - 1:
                    if y[i] != None and x[i] + timedelta(minutes=time_window) < x[i + 1]:
                        x.insert(i + 1, x[i] + timedelta(minutes=time_window))
                        y.insert(i + 1, None)
                    i += 1

                fig = go.Figure(go.Scatter(x=x, y=y), layout=go.Layout(yaxis=dict(range=[0, 100])))
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                with ui.card():
                    with ui.row().classes('w-full'):
                        with ui.row().classes("items-baseline"):
                            ui.label(reactor.reactor_name).classes('text-lg font-bold font-mono')
                            ui.label(reactor.reactor_type).classes('text-xs font-mono') 
                        ui.space()
                        ui.circular_progress(round(reactor.data_points[-1].value_percent), min=0, max=100, size="md").classes("mr-2")
                    ui.plotly(fig).classes('w-96 h-40')