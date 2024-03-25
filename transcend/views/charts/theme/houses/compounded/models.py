# # coding=utf-8
# """
# Created on 2020, April 22th
# @author: orion
# """
# from transcend.processes import merge
# from transcend.views.charts.theme.constants import WHEEL
# from transcend.views.charts.theme.bounds.models import Model as BaseModel
#
#
# class Model(BaseModel):
#
#     def __init__(self, chart):
#         super(Model, self).__init__(chart)
#         self.init()
#
#     def init(self):
#         self.load_chart()
#
#     def load_chart(self):
#
#         chart = self.get_container()
#         chart_name = chart.get_name()
#         sub_chart_name = chart.get_sub_name()
#
#         if sub_chart_name:
#             colors = WHEEL[chart_name][sub_chart_name]['houses']['pie']['colors']
#
#         else:
#             colors = WHEEL[chart_name]['houses']['pie']['colors']
#
#         houses_bounds = self.get_houses_bounds(sub_chart_name="sidereal")
#
#         external_annotation_radius = WHEEL['houses']['annotations']['radius']['internal']
#
#         rmax, rmin, domain = self.get_houses_pie()
#
#         content = chart.get_content()
#
#         structure = dict(
#             opacity=0.75,
#             visible=True,
#             name="",
#             line=dict(
#                 opacity=0.4,
#                 points=dict(
#                     internal=dict(
#                         radius=houses_bounds["radius"]['min'],
#                     ),
#                     external=dict(
#                         radius=houses_bounds["radius"]['max'],
#                     ),
#                 ),
#                 dash='solid',
#                 color="#444",
#                 width=1,
#             ),
#             pie=dict(
#                 domain=domain,
#                 hole=rmin,
#                 colors=colors,
#                 # textinfo='none',
#                 textinfo='label',
#                 hovertext='',
#                 # hovertext=' ',
#                 # hoverinfo='none',
#                 marker=dict(
#                     line=dict(
#                         width=1.0,
#                         color="#888",
#                     ),
#                 ),
#                 hoverinfo='label',
#                 hovertemplate="" +
#                 "%{label}<br>" +
#                 "<i>%{customdata[0]}</i>",
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
