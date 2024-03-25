# # coding=utf-8
# """
# Created on 2020, April 28th
# @author: orion
# """
# import copy
# from transcend.processes import merge
#
# from transcend.views.processes import Process as BaseProcess
# from transcend.models.houses.models import Model as HousesModel
#
# from transcend.views.charts.theme.houses.charts import get_annotation_structure
#
# from transcend.views.charts.theme.figure.processes import get_coordinates, get_centers
#
# from transcend.views.charts.theme.graphics.lines import get_all as get_graphic_lines
# from transcend.views.charts.theme.graphics.houses import get_all as get_graphic_houses
#
#
# def get_labels(labels, prefix):
#     return ["{} - {}".format(prefix, label) for label in labels]
#
#
# class Process(BaseProcess):
#
#     def __init__(self, data_model, process_model, view_model):
#         super(Process, self).__init__(
#             data_model,
#             copy.deepcopy(
#                 process_model,
#             ),
#             view_model,
#         )
#         self.process()
#
#
#     def load(self):
#
#         model = HousesModel(
#             self.get_container()["houses"]
#         )
#
#
#
#     def get_data(self):
#         return self.data
#
#     def create_graphics_components(self, data=None):
#         traces = get_graphic_lines(self.get_chart().get_content())
#         self.add_traces(traces)
#
#         annotations = get_graphic_houses(self.get_chart().get_content())
#         self.add_annotations(annotations)
