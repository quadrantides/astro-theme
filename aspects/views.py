# from os.path import join
# from typing import Any
#
# from django.conf import settings
#
# from bokeh.document import Document
# from bokeh.layouts import column
# from bokeh.models import ColumnDataSource, Slider, Div
# from bokeh.plotting import figure
# from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
# from bokeh.themes import Theme
#
# from aspects.read import get_inactive_by_cycle as get_inactive_aspects_by_cycle
#
# theme = Theme(filename=join(settings.ASPECTS_THEMES_DIR, "theme.yaml"))
#
#
# def with_request(f):
#     def wrapper(doc):
#         return f(doc, doc.session_context.request)
#     return wrapper
#
#
# async def activation_handler(doc: Document) -> None:
#
#     planet1 = "sun"
#     planet2 = "venus"
#
#     inactive_aspects_by_cycle = await get_inactive_aspects_by_cycle(planet1, planet2)
#     # inactive_aspects_by_cycle = await database_sync_to_async(get_inactive_aspects_by_cycle(planet1, planet2))()
#
#     text = "Nombre d'enregistrements inactifs : {}".format(
#         inactive_aspects_by_cycle,
#     )
#
#     div = Div(text=text)
#
#     df = sea_surface_temperature.copy()
#     source = ColumnDataSource(data=df)
#
#     plot = figure(x_axis_type="datetime", y_range=(0, 25), y_axis_label="Temperature (Celsius)",
#                   title="Sea Surface Temperature at 43.18, -70.43")
#     plot.line("time", "temperature", source=source)
#
#     def callback(attr: str, old: Any, new: Any) -> None:
#         if new == 0:
#             data = df
#         else:
#             data = df.rolling("{0}D".format(new)).mean()
#         source.data = dict(ColumnDataSource(data=data).data)
#
#     slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
#     slider.on_change("value", callback)
#
#     doc.theme = theme
#     doc.add_root(column(div, slider, plot))
#     # doc.add_root(column(slider, plot))
#
#
# async def activation(doc: Document, request: Any) -> None:
#     await activation_handler(doc)
#     doc.template = """
# {% block title %}Embedding a Bokeh Apps In Django{% endblock %}
# {% block preamble %}
# <style>
# .bold { font-weight: bold; }
# </style>
# {% endblock %}
# {% block contents %}
#     <div>
#     This Bokeh app below is served by a <span class="bold">Django</span> server for {{ username }}:
#     </div>
#     {{ super() }}
# {% endblock %}
#     """
#     doc.template_variables["username"] = request.user
#
#
# @with_request
# async def activation_view(doc: Document, request: Any) -> None:
#     await activation(doc, request)
