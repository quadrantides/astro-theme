# coding=utf-8
"""
Created on 2020, June 5th
@author: orion
"""
from astro.utils import is_conjunction

from .containers import Container
from .aspects import Aspect, ConjunctionAspect
from .aspects import AspectProcess, ConjunctionAspectProcess

PRECISION = 0.001

DATE_FORMAT = "%Y-%m-%d %H:%M"


def get_event_instance(angle):
    if is_conjunction(angle):
        res = ConjunctionAspect()
    else:
        res = Aspect()
    return res


class AspectsManager(Container):

    def __init__(self, angles, just_one_aspect=False):
        super(AspectsManager, self).__init__([])
        self.just_one_aspect = just_one_aspect
        self.angles = angles
        self.orbs = []
        self.aspects_in_progress = []
        self.nb_aspects_expected = 0

    # def set_angles(self, dlongitudes):
    #     print("ok")
    #     self.angles = None

    def set_orbs(self, value):
        self.orbs = value

    def set_nb_aspects_expected(self):
        self.nb_aspects_expected = len(self.get_container())

    def set_just_one_aspect(self, value):
        self.just_one_aspect = value

    def created_all_aspects_in_progress(self):
        aspects_to_remove = []
        for aspect in self.aspects_in_progress:
            self.get_container().append(aspect)
            aspects_to_remove.append(aspect)

        for aspect in aspects_to_remove:
            self.aspects_in_progress.remove(aspect)

    def remove_created_aspects(self, angular_distance):
        """
            Retire les aspects qui passent de l'état : "loading in progress" à l'état "created"
            Les stocke dans le container

        :param angular_distance:

        """
        aspects_to_remove = []
        for aspect in self.aspects_in_progress:
            if not aspect.is_state_loading_in_progress(angular_distance):
                self.get_container().append(aspect)
                aspects_to_remove.append(aspect)

        for aspect in aspects_to_remove:
            self.aspects_in_progress.remove(aspect)

    def add_new_aspects_in_progress(self, angular_distance):
        """
            Ajoute les nouveaux aspects
        :param angular_distance:
        :return:
        """
        in_progress = []
        for aspect in self.aspects_in_progress:
            in_progress.append(
                (
                    aspect.get_container().get_angle(),
                    aspect.get_container().get_orb(),
                )
            )

        for angle in self.angles:
            for orb in self.orbs:
                if not (angle, orb) in in_progress:

                    if is_conjunction(angle):
                        aspect = ConjunctionAspectProcess(
                            ConjunctionAspect(),
                        )

                    else:
                        aspect = AspectProcess(
                            Aspect(),
                        )

                    aspect.get_container().set_angle(angle)
                    aspect.get_container().set_orb(orb)

                    if angle == 180.0 and aspect.is_state_loading_in_progress(angular_distance):
                        print('ok')

                    if aspect.is_state_loading_in_progress(angular_distance):

                        self.aspects_in_progress.append(
                            aspect,
                        )

    def get_loading_in_progress_aspects(self, angular_distance):
        """
            Retourne les aspects dont l'état est "loading in progress"

        :param angular_distance:
        :return:
        """
        self.remove_created_aspects(angular_distance)
        self.add_new_aspects_in_progress(angular_distance)
        return self.aspects_in_progress

    def get_aspects(self):
        return self.get_container()

    def stop(self):
        res = False
        nb_aspects_created = len(self.get_container())
        if self.just_one_aspect:
            res = nb_aspects_created == self.nb_aspects_expected
        if res:
            self.created_all_aspects_in_progress()
        return res

    def reinit(self):
        self.set_container([])
        self.aspects_in_progress = []
