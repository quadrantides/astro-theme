# coding=utf-8
"""
Created on 2020, June 5th
@author: orion
"""
import numpy as np

from astro.utils import is_conjunction
from containers import Container

PRECISION = 0.001

DATE_FORMAT = "%Y-%m-%d %H:%M"


def get_event_instance(angle):
    if is_conjunction(angle):
        res = ConjunctionAspect()
    else:
        res = Aspect()
    return res


class Aspect(object):

    def __init__(self):
        self.start = None
        self.contact = None
        self.end = None
        self.angle = 0.0
        self.orb = 0.0

    @property
    def is_conjunction(self):
        return is_conjunction(self.angle)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_contact(self):
        return self.contact

    def get_orb(self):
        return self.orb

    def get_angle(self):
        return self.angle

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def set_contact(self, contact):
        self.contact = contact

    def set_orb(self, orb):
        self.orb = orb

    def set_angle(self, angle):
        self.angle = angle

    def update(self, date, is_contact=False):

        if not self.start:
            self.start = date
            self.end = date
        else:
            self.end = date

        if is_contact:
            self.contact = date

    def __str__(self):
        angle = "Angle : {}".format(
            str(self.angle),
        )
        orb = "Orb : {}".format(
            str(self.orb),
        )
        start = "Start : {}".format(
            str(self.start) if self.start else "",
        )
        end = "End : {}".format(
            str(self.end) if self.end else "",
        )
        contact = "Contact : {}".format(
            str(self.contact) if self.contact else "Date not defined",
        )

        content = ", ".join(
            [
                angle,
                orb,
                start,
                end,
                contact,
            ]
        )
        return content


class ConjunctionAspect(Aspect):

    def __init__(self):
        super(ConjunctionAspect, self).__init__()
        self.ra = 0.0
        self.conjunction = {'type': "", 'true': False}

    def set_ra(self, value):
        self.ra = value

    def set_type(self, value):
        self.conjunction['type'] = value

    def set_true(self, value):
        self.conjunction['true'] = value

    def get_type(self):
        return self.conjunction['type']

    def get_true(self):
        return self.conjunction['true']

    def update(self, date, conjunction_type, right_ascension, is_true=False, is_contact=False):
        super(ConjunctionAspect, self).update(date, is_contact=is_contact)
        self.set_ra(right_ascension)
        self.set_type(conjunction_type)
        self.set_true(is_true)

    def __str__(self):
        parent_content = super(ConjunctionAspect, self).__str__()
        conj_type = "Conjunction / Type : {}".format(
            str(self.conjunction['type']),
        )
        conj_true = "True Conjunction ? : {}".format(
            "Yes" if self.conjunction['true'] else "No",
        )

        content = ", ".join(
            [
                conj_type,
                conj_true,
             ]
        )

        return ", ".join(
            [
                parent_content,
                content,
             ]
        )


class AspectProcess(Container):

    def __init__(self, aspect):

        super(AspectProcess, self).__init__(aspect)
        self.angular_distances = [None] * 4
        self.states = ['initialized', 'loading in progress', 'created']
        self.state_index = 0

    def get_angle(self):
        return self.get_container().get_angle()

    def get_orb(self):
        return self.get_container().get_orb()

    def get_start(self):
        return self.get_container().get_start()

    def get_end(self):
        return self.get_container().get_end()

    def is_conjunction(self):
        return self.get_container().is_conjunction

    def is_contact(self):
        """
        il est atteint si la pente change de signe ou si la dérivé s'annnule
        :return:
        """
        angle = self.get_container().get_angle()
        if self.angular_distances[2] is not None:
            dp1 = self.angular_distances[2] - angle
            dp2 = self.angular_distances[3] - angle
            signed_of_derive_changed = dp1 * dp2 < 0
        else:
            signed_of_derive_changed = False

        if None not in self.angular_distances:
            dp_second1 = self.angular_distances[1] - self.angular_distances[0]
            dp_second2 = self.angular_distances[3] - self.angular_distances[2]
            extremum_of_derive_second_reached = dp_second1 * dp_second2 < 0
        else:
            extremum_of_derive_second_reached = False

        return signed_of_derive_changed or extremum_of_derive_second_reached

    def is_state_loading_in_progress(self, angular_distance):

        self.angular_distances = np.roll(self.angular_distances, -1)
        self.angular_distances[-1] = angular_distance
        is_artefact = False
        if self.angular_distances[-2] is not None:
            if abs(self.angular_distances[-1] - self.angular_distances[-2]) >= 200:
                # discontinuité (une des deux planètes a bouclé un tour du cercle trigonométrique
                # il s'agit d'un artefact
                is_artefact = True

        min_dist_reached = \
            (abs((angular_distance % 360) - self.get_container().get_angle()) <= self.get_container().get_orb())

        res = min_dist_reached # and not is_artefact
        if res:
            if self.states[self.state_index] == 'initialized':
                # => state "loading in progress"
                self.state_index = 1
        else:
            if self.states[self.state_index] == 'loading in progress':
                # => state "created"
                self.state_index = 2

        return res

    def update(self, date):
        container = self.get_container()

        if False:
            # le calcul du du contact est désactivé : c'est un calcul à faire une fois que les aspects sont connus
            # avec la plus grand eprécision possible

            is_contact = self.is_contact()
        else:
            is_contact = False

        container.update(date, is_contact=is_contact)

    def get_state(self):
        return self.states[self.state_index]


class ConjunctionAspectProcess(AspectProcess):

    def __init__(self, aspect):
        super(ConjunctionAspectProcess, self).__init__(aspect)
        # self.right_ascensions = [None] * 2

    def update(self, date, angular_distance, right_ascension, latitude_distance, sun_distance, planet_distance):

        # self.right_ascensions = np.roll(self.right_ascensions, -1)
        # self.right_ascensions[-1] = right_ascension

        conjunction_type = "superior" if planet_distance > sun_distance else "inferior"
        is_true = True if latitude_distance <= PRECISION else False

        container = self.get_container()
        container.update(date, conjunction_type, right_ascension, is_true=is_true, is_contact=self.is_contact())

    def get_type(self):
        return self.get_container().get_type()

    def get_true(self):
        return self.get_container().get_true()
