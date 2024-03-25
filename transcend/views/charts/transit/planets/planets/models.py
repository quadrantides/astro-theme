# # coding=utf-8
# """
# Created on 2020, April 28th
# @author: orion
# """
# from transcend.processes import merge
# from transcend.views.charts.graphics.models import Model as GraphicsModel
# from transcend.views.charts.theme.models import Model as BaseModel
#
#
# class Model(BaseModel, GraphicsModel):
#
#     def __init__(self, chart, dimensions=None):
#         BaseModel.__init__(self, chart)
#         GraphicsModel.__init__(self, dimensions=dimensions)
#         self.init()
#
#     def init(self):
#         self.load_chart()
#
#     def load_chart(self):
#         chart = self.get_container()
#         theme = chart.get_theme()
#
#         planets_radius = WHEEL["planets"][self.get_theme()]['radius']
#
#         image_size = WHEEL['planets']['image']['size']
#
#         image_radius = 0.5 * image_size + planets_radius
#         annotation_radius = 1.5 * image_size + planets_radius
#         marker_radius = (image_radius + annotation_radius) / 2.0
#         lines = self.get_planets_lines(WHEEL)
#
#         box_size = WHEEL['planets']['box_size']
#
#         content = chart.get_content()
#
#         color = WHEEL['planets']['line']['color']
#
#         structure = dict(
#             hovertemplate='%{text}',
#             opacity=0.75,
#             visible=True,
#             name="planets",
#             radius=planets_radius,
#             box_size=box_size,
#             annotation=dict(
#                 opacity=0.75,
#                 radius=annotation_radius,
#                 xanchor="center",
#                 yanchor="middle",
#                 textposition="center middle",
#                 font=dict(
#                     family='sans-serif',
#                     color=color,
#                     size=9,
#                 ),
#                 layer="above",
#             ),
#             image=dict(
#                 opacity=0.75,
#                 radius=image_radius,
#                 sizex=image_size,
#                 sizey=image_size,
#                 xanchor="center",
#                 yanchor="middle",
#                 layer="above",
#             ),
#             marker=dict(
#                 opacity=0.0,
#                 visible=True,
#                 symbol="square",
#                 size=8,
#                 color="#009933",
#                 line=dict(
#                     color="#b3b3cc",
#                     width=2,
#                 ),
#                 # radius=marker_radius,
#                 radius=marker_radius,
#                 layer="above",
#                 hovertemplate="" +
#                               "<i>%{customdata[2]}</i><br>" +
#                               "<i> %{customdata[3]}</i><br>" +
#                               "<i> %{customdata[1]}</i><br>" +
#                               "<i>%{customdata[4]}</i>",
#             ),
#             line=dict(
#                 points=dict(
#                     internal=dict(
#                         radius=lines["radius"]['min'],
#                     ),
#                     external=dict(
#                         radius=lines["radius"]['max'],
#                     ),
#                 ),
#                 dash='solid',
#                 color=color,
#                 width=1.5,
#             ),
#         )
#
#         merge(
#             structure,
#             content,
#         )
#
#     def get_data(self):
#         return self.get_container()
