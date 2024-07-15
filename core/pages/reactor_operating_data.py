from nicegui import ui, events
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone

from models import datetime_converter
from models.reactor_operating_data import ReactorOperatingData
from pages import theme
from time_series_data.reactor_operating_data import get_points_between_dates, get_start_stop_intervals
from tinyflux import Point

@ui.page('/reactor_operating_data')
def reactor_operating_data():

    def get_dates_from_value_change_event(event: events.ValueChangeEventArguments):
        if type(event.value) == str:
            start = datetime.strptime(event.value, '%Y-%m-%d')
            stop = start
        elif type(event.value) == dict:
            start = datetime.strptime(event.value["from"], '%Y-%m-%d')
            stop = datetime.strptime(event.value["to"], '%Y-%m-%d')
        else: 
            start = None
            stop = None

        return start, stop

    @ui.refreshable
    def plot_cards(start_local: datetime | None = None, stop_local: datetime | None = None):
        if start_local is None:
            start_local = datetime_converter.utc_to_local(datetime.now())
        if stop_local is None:
            stop_local = datetime_converter.utc_to_local(datetime.now())

        start_earliest_on_local_day = start_local.replace(hour=0, minute=0, second=0, microsecond=0)
        stop_latest_on_local_day = stop_local.replace(hour=23, minute=59, second=59, microsecond=999999)

        with ui.row().classes("items-center"):
            ui.icon('edit_calendar', size="md", color="primary").on('click', date_range_menu.open).classes('cursor-pointer ml-2 hover:bg-slate-200 rounded-full h-12 w-12')
            with ui.row().classes('text-lg font-mono'):
                if start_local.date() == stop_local.date():
                    ui.markdown(f"Showing data from **{start_local.date()}**")
                else:
                    ui.markdown(f"Showing data from **{start_local.date()}** to **{stop_local.date()}**")

        ui.separator().classes("mb-2")

        with ui.row():
            for reactor in ReactorOperatingData.objects.all():
                reactor: ReactorOperatingData

                points: list[Point] = get_points_between_dates(reactor, start_earliest_on_local_day, stop_latest_on_local_day)

                if len(points) == 0:
                    with ui.card():
                        with ui.row().classes('w-full'):
                            with ui.row().classes("items-baseline"):
                                ui.label(reactor.reactor_name).classes('text-lg font-bold font-mono')
                                ui.label(reactor.reactor_type).classes('text-xs font-mono') 
                        ui.label("No data")
                    continue

                x = [datetime_converter.utc_to_local(point.time) for point in points]
                y = [point.fields["pct"] for point in points]

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
                        ui.circular_progress(round(points[-1].fields["pct"]), min=0, max=100, size="md").classes("mr-2")
                    ui.plotly(fig).classes('w-96 h-40')

    with theme.frame():
        # Dates picker
        with ui.row():
            start_interval, stop_interval = get_start_stop_intervals()
            start_interval_date_str = datetime_converter.utc_to_local(start_interval).strftime('%Y/%m/%d')
            stop_interval_date_str = datetime_converter.utc_to_local(stop_interval).strftime('%Y/%m/%d')

            today = datetime.now(timezone.utc)
            if today < start_interval:
                today = start_interval
            elif today > stop_interval:
                today = stop_interval
            today_interval_str_dashes = datetime_converter.utc_to_local(today).strftime('%Y-%m-%d')

            with ui.menu() as date_range_menu:
                with ui.date(value=today_interval_str_dashes, on_change=lambda x: x.value is not None and plot_cards.refresh(*get_dates_from_value_change_event(x))).props(f'''range :options="date => date >= '{start_interval_date_str}' && date <= '{stop_interval_date_str}'"'''):
                    with ui.row().classes('justify-end'):
                        ui.button('Close', on_click=date_range_menu.close).props('flat')
            
            # ui.icon('edit_calendar', size="md", color="primary").on('click', date_range_menu.open).classes('cursor-pointer')

            # with ui.input('Date range', value=today_interval_str_dashes, on_change=lambda x: plot_cards.refresh(*get_dates_from_value_change_event(x))) as date_range:
            #     with ui.menu() as date_range_menu:
            #         with ui.date().bind_value(date_range).props(f'''range :options="date => date >= '{start_interval_date_str}' && date <= '{stop_interval_date_str}'"'''):
            #             with ui.row().classes('justify-end'):
            #                 ui.button('Close', on_click=date_range_menu.close).props('flat')
            #     with date_range.add_slot('append'):
            #         ui.icon('edit_calendar').on('click', date_range_menu.open).classes('cursor-pointer')

        # Plot cards
        plot_cards()