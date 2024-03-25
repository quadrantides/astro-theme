# coding=utf-8
"""
Created on 2020, April 24th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.theme.graphics.points.lines import get_all as get_graphic_lines
from transcend.views.charts.theme.graphics.points.annotations import get_all as get_graphic_annotations

# from transcend.views.charts.theme.graphics.processes import get_display_order
from transcend.views.charts.theme.planets.points.processes import Process as BaseProcess
from transcend.views.charts.theme.planets.points.processes import get_annotations_keywords

BOX_SIZE = 5  # in degree
SHIFT = 0  # 20


def extract_label_subscript(label):
    slabel = label.split('<sub>')
    items = [item.replace('</sub>', "") for item in slabel]
    return items[1]


def concat_labels(label1, label2):
    slabel1 = label1.split('<sub>')
    items1 = [item.replace('</sub>', "") for item in slabel1]

    slabel2 = label2.split('<sub>')
    items2 = [item.replace('</sub>', "") for item in slabel2]

    if items1[0] == items2[0]:
        name = items1[0]
        index = ",".join(
            [
                items1[1],
                items2[1],
            ]
        )
        label = "{}<sub>{}</sub>".format(
            name,
            index
        )
    else:
        label = " - ".join(
            [
                label1,
                label2,
            ]
        )
    return label


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None, label_extension='', load_only=True):
        super(Process, self).__init__(
            data_model,
            process_model,
            view_model=view_model,
            label_extension=label_extension,
            load_only=load_only,
        )

    def create_graphics_components(self, data=None):
        traces = get_graphic_lines(self.get_chart().get_content()['points'])

        if data:

            # TRACES
            traces.extend(
                get_graphic_lines(data)
            )

            # ANNOTATIONS
            all_points = self.get_chart().get_content()['points']
            all_points.extend(
                data
            )
            i = 0
            indexes = []
            angles = []
            for point in all_points:
                angles.append(
                    point['angle'],
                )

                indexes.append(i)
                i += 1

            orders = get_display_order(BOX_SIZE, angles)

            new_points = [
                all_points[orders[0]],
            ]

            new_points[0]['annotation'] = merge(
                get_annotations_keywords(
                    new_points[0]['label'],
                    new_points[0]['angle'],
                ),
                new_points[0]['annotation'],
            )

            orders.pop(0)

            nb_orders = len(orders)
            found = False
            eod = False
            i = 0
            while not found and not eod:
                order = orders[i]
                point = all_points[order]
                angle = point['angle']
                current_new_point = new_points[-1]
                dangle = round(angle) - round(current_new_point['angle'])
                dangle = dangle % 360
                if dangle < BOX_SIZE:
                    if abs(dangle) < 1:
                        # current point must be concatenated with the previous new point
                        current_new_point['annotation']["text"] = concat_labels(
                            current_new_point['annotation']["text"],
                            point['annotation']["text"],
                        )
                    else:
                        if point["label"][0:2] != 'AS':
                            # ax, ay must be calculated to move away the two current points

                            current_new_point['annotation'] = merge(
                                get_annotations_keywords(
                                    current_new_point['label'],
                                    current_new_point['angle'],
                                    shift=-SHIFT,
                                ),
                                current_new_point['annotation'],
                            )
                            point['annotation'] = merge(
                                get_annotations_keywords(
                                    point['label'],
                                    point['angle'],
                                    shift=SHIFT,
                                ),
                                point['annotation'],
                            )
                        else:
                            point['annotation'] = merge(
                                get_annotations_keywords(
                                    point['label'],
                                    point['angle'],
                                ),
                                point['annotation'],
                            )

                        point['annotation']["text"] = extract_label_subscript(
                            point['annotation']["text"],
                        )
                        point['annotation']['font']['size'] = 10
                        point['annotation']['ax'] = 0.5 * point['annotation']['ax']
                        point['annotation']['ay'] = 0.5 * point['annotation']['ay']

                        new_points.append(
                            point
                        )

                else:

                    point['annotation'] = merge(
                        get_annotations_keywords(
                            point['label'],
                            point['angle'],
                        ),
                        point['annotation'],
                    )

                    new_points.append(
                        point
                    )

                i += 1
                if i >= nb_orders:
                    eod = True

            annotations = get_graphic_annotations(new_points)
        else:
            annotations = get_graphic_annotations(self.get_chart().get_content()['points'])

        self.add_traces(traces)
        self.add_annotations(annotations)
