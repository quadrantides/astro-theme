# coding=utf-8
"""
Created on 2020, June 29th
@author: orion
"""
import math
import numpy as np

from transcend.containers import Container


class Cluster(Container):

    def __init__(self, data):
        self.set_identifier(data)
        super(Cluster, self).__init__(container=data, identifier=self.get_identifier())
        self.raw_bounds = []
        self.perimeter = []

    def add_planet(self, data):
        self.container.append(data)
        self.set_identifier(self.get_container())

    def set_raw_bounds(self, value):
        self.raw_bounds = value

    def get_raw_bounds(self):
        return self.raw_bounds

    # def raw_bounds(self, orb, index=-1):
    #
    #     data = self.get_container()
    #     nb_planets = len(data)
    #
    #     index = 0 if index == -1 and nb_planets == 1 else index
    #     if index == -1 and nb_planets % 2 == 1:
    #         index = int(nb_planets / 2)
    #
    #     # caractérisation de la planète de référence
    #
    #     if index == 4:
    #         print('ok')
    #     if index < 0:
    #         index_candidate = int(nb_planets / 2)
    #         angle_max = data[-1]['angle']
    #         angle_min = data[0]['angle']
    #         if angle_max < angle_min:
    #             angle_max += 360.0
    #         ref_angle = angle_min + (angle_max - angle_min) / 2.0
    #         ref_angle = ref_angle % 360
    #         if nb_planets > 3:
    #             angles = np.array([datai['angle'] for datai in data])
    #             dangles = abs(angles - ref_angle)
    #             ref_angle = angles[np.argmin(dangles)]
    #     else:
    #         ref_angle = data[index]["angle"]
    #
    #     ref_angle = int(round(ref_angle))
    #
    #     if index > -1:
    #         ref_angle_min = ref_angle - orb / 2.0
    #         # ref_angle_max = ref_angle + orb / 2.0
    #         position_min = ref_angle_min - orb * index
    #         position_max = position_min + orb * nb_planets
    #
    #     else:
    #         position_min = ref_angle - orb * index_candidate
    #         position_max = position_min + orb * nb_planets
    #
    #     if nb_planets == 1:
    #         print('ok')
    #
    #     return math.ceil(position_min), math.ceil(position_max)

    def perimeter_validation(self, perimeter, orb):
        validation = False
        data = self.get_container()
        nb_planets = len(data)
        elongation = perimeter[-1] - perimeter[0] + 1
        if elongation == 360:
            perimeter = np.array(perimeter)
            dp = perimeter[1::] - perimeter[0:-1]
            if len(np.where(dp > 1)) > 0:
                perimeter[0:np.where(dp > 1)[0][0] + 1] = perimeter[0:np.where(dp > 1)[0][0] + 1] + 360
                perimeter.sort()
                perimeter = perimeter.tolist()
                elongation = perimeter[-1] - perimeter[0] + 1

        if elongation == orb * nb_planets:
            self.perimeter = perimeter
            validation = True
        return validation

    def get_graphical_position(self, perimeter, orb):
        positions = dict()
        if self.perimeter_validation(perimeter, orb):
            data = self.get_container()
            nb_planets = len(data)
            for i in range(nb_planets):
                anglei = (self.perimeter[0] + orb / 2.0 + i * orb) % 360
                positions.update(
                    {data[i]['label']: anglei}
                )
        return positions

    def get_raw_graphical_position(self, orb):
        position_min = -1
        position_max = -1
        if self.is_graphical_position_fixed():

            asc_found, asc_index = self.contains_planet("asc")
            mc_found, mc_index = self.contains_planet("mc")

            if asc_found and mc_found:
                # cas particulier : ce cluster contient les deux ppoints d'intérêt ASC et MC
                # il faut s'assurer que toutes les planètes situées entre les deux points d'intérêt
                # seront graphiquement affichables
                # TODO calculer la valeur de orb qui permette d'afficher toutes les planètes situées entre ASC et MC
                print('set_graphical_position')
            else:
                ref_index = asc_index if asc_found else mc_index
                position_min, position_max = self.get_raw_bounds()
        else:
            position_min, position_max = self.get_raw_bounds()

        return position_min, position_max

    def set_identifier(self, data):
        labels = [item['label'] for item in data]
        self.identifier = "-".join(labels)

    def get_identifier(self):
        return self.identifier

    def __contains__(self, cluster):
        labels = [item['label'] for item in self.get_container()]
        cluster_labels = [item['label'] for item in cluster.get_container()]
        nb_cluster_labels = len(cluster_labels)
        nb_found = 0
        for label in cluster_labels:
            if label in labels:
                nb_found += 1
        return nb_found == nb_cluster_labels

    def __eq__(self, other):
        labels = [item['label'] for item in self.get_container()]
        nb_labels = len(labels)
        other_labels = [item['label'] for item in other.get_container()]
        nb_other_labels = len(other_labels)
        return self.__contains__(other) and nb_labels == nb_other_labels

    def is_graphical_position_fixed(self):
        asc_found, index = self.contains_planet("asc")
        mc_found, index = self.contains_planet("mc")
        return asc_found or mc_found

    def contains_planet(self, label):
        cluster = self.get_container()
        nb_planets = len(cluster)
        eod = nb_planets == 0
        found = False
        i = 0
        while not eod and not found:
            if cluster[i]["label"] == label:
                found = True
            if not found:
                i += 1
                if i > nb_planets - 1:
                    eod = True
        if found:
            index = i
        else:
            index = -1
        return found, index


class Clusters(Container):

    def __init__(self, process, orb):
        super(Clusters, self).__init__(process)
        self.data = []
        self.orb = orb
        self.graphical_positions = []
        self.init_graphical_positions()
        self.load()
        self.remove_duplicates()
        self.update()

    def init_graphical_positions(self):
        self.graphical_positions = np.array([""] * 360, dtype="S100")

    def sort_planets_data(self):

        angles = []
        labels = []

        for planet in self.get_container().get_data():
            angles.append(
                planet['angle']
            )
            labels.append(
                planet['label']
            )

        orders = list(range(len(angles)))

        sorted_indices = np.argsort(angles)

        orders = np.array(orders)
        angles = np.array(angles)
        labels = np.array(labels)

        orders = orders[sorted_indices]
        dangle = angles[0] + 360 - angles[-1]
        i = 1
        while dangle < 2 * self.orb:
            dangle = angles[i] - angles[i - 1]
            i += 1

        orders = np.roll(orders, -(i - 1))

        angles = angles[orders]
        labels = labels[orders]

        angles = angles.tolist()
        labels = labels.tolist()

        return angles, labels

    def add(self, cluster):
        self.data.append(cluster)

    def remove(self, duplicates):
        data = []
        for item in self.data:
            found = False
            for duplicate in duplicates:
                if item == duplicate:
                    found = True
                    break
            if not found:
                data.append(
                    item
                )
        self.data = data

    def update(self):
        for cluster in self.data:
            self.set_cluster_bounds(cluster)

    def get_clusters(self):
        return self.data

    def remove_duplicates(self):
        clusters = dict()
        i = 0
        for cluster in self.get_clusters():
            clusters[i] = dict()
            for item in cluster.get_container():
                clusters[i].update(
                    {item["label"]: item["angle"]},
                )
            i += 1

        keys = list(clusters.keys())
        key0 = keys[0]
        uniques = {key0: clusters[key0]}
        keys.remove(key0)
        for key in keys:
            i = 0
            unique_keys = list(uniques.keys())
            nb_unique_keys = len(unique_keys)
            eod = nb_unique_keys == 0
            found = False
            while not eod and not found:
                if list(clusters[key].keys()) == list(uniques[unique_keys[i]].keys()):
                    found = True
                else:
                    i += 1
                    if i > nb_unique_keys - 1:
                        eod = True
            if not found:
                uniques[key] = clusters[key]

        lengths = dict()
        for key in uniques.keys():
            length = len(self.get_clusters()[key].get_container())
            if length in lengths.keys():
                lengths[length].append(
                    self.get_clusters()[key],
                )
            else:
                lengths[length] = [self.get_clusters()[key]]

        self.fusion(lengths)

    def fusion(self, lengths):
        duplicates = []
        keys = list(lengths.keys())
        keys = np.sort(np.array(keys)).tolist()
        nb_keys = len(keys)
        for i in range(nb_keys-1):
            sources = lengths[keys[i]]
            for key in keys[i+1::]:
                targets = lengths[key]
                nb_targets = len(targets)
                for source in sources:
                    eod = nb_targets == 0
                    found = False
                    j = 0
                    while not eod and not found:
                        if targets[j].__contains__(source):
                            found = True
                        else:
                            j += 1
                            if j > nb_targets - 1:
                                eod = True
                    if found:
                        duplicates.append(
                            source,
                        )

        self.remove(duplicates)

    def calculate_cluster_bounds(self, cluster, index=-1):

        data = cluster.get_container()
        nb_planets = len(data)

        index = 0 if index == -1 and nb_planets == 1 else index

        if index >= 0:
            ref_angle = data[index]["angle"]
        else:
            if nb_planets % 2 == 1:
                # Nombre de planète impaire
                index = int(nb_planets / 2)
            else:
                # Nombre de planète paire
                angles = [planet['angle']for planet in data]
                angle_max = angles[-1]
                angle_min = angles[0]

                if angle_max < angle_min:
                    angle_max += 360.0
                ref_angle = angle_min + (angle_max - angle_min) / 2.0
                ref_angle = ref_angle % 360
                if nb_planets > 2:
                    angles = np.array(angles)
                    index = np.argmin(abs(angles - ref_angle))

            if index >= 0:
                ref_angle = data[index]["angle"]
            else:
                index_candidate = int(nb_planets / 2)
        # caractérisation de la planète de référence


        if nb_planets == 2:
            print('ok')
        # if index < 0:
        #     index_candidate = int(nb_planets / 2)
        #     angle_max = data[-1]['angle']
        #     angle_min = data[0]['angle']
        #     if angle_max < angle_min:
        #         angle_max += 360.0
        #     ref_angle = angle_min + (angle_max - angle_min) / 2.0
        #     ref_angle = ref_angle % 360
        #     if nb_planets > 3:
        #         angles = np.array([datai['angle'] for datai in data])
        #         dangles = abs(angles - ref_angle)
        #         ref_angle = angles[np.argmin(dangles)]
        # else:
        #     ref_angle = data[index]["angle"]

        ref_angle = int(round(ref_angle))

        if index > -1:
            ref_angle_min = ref_angle - self.orb / 2.0
            # ref_angle_max = ref_angle + orb / 2.0
            position_min = ref_angle_min - self.orb * index
            position_max = position_min + self.orb * nb_planets

        else:
            position_min = ref_angle - self.orb * index_candidate
            position_max = position_min + self.orb * nb_planets

        return math.ceil(position_min), math.ceil(position_max)

    def set_cluster_bounds(self, cluster):

        position_min = -1
        position_max = -1
        if cluster.is_graphical_position_fixed():

            asc_found, asc_index = cluster.contains_planet("asc")
            mc_found, mc_index = cluster.contains_planet("mc")

            if asc_found and mc_found:
                # cas particulier : ce cluster contient les deux ppoints d'intérêt ASC et MC
                # il faut s'assurer que toutes les planètes situées entre les deux points d'intérêt
                # seront graphiquement affichables
                # TODO calculer la valeur de orb qui permette d'afficher toutes les planètes situées entre ASC et MC
                print('set_graphical_position')
            else:
                ref_index = asc_index if asc_found else mc_index
                position_min, position_max = self.calculate_cluster_bounds(cluster, index=ref_index)
        else:
            position_min, position_max = self.calculate_cluster_bounds(cluster)

        cluster.set_raw_bounds(
            [position_min, position_max],
        )

    def load(self):

        angles, labels = self.sort_planets_data()

        nb_records = len(angles)
        eod = nb_records == 0
        i = 0

        while not eod:

            # CREATION D'UN NOUVEAU CLUSTER

            anglei = angles[i]
            labeli = labels[i]

            planets_in_cluster = [labeli]

            data = dict(
                label=labeli,
                angle=anglei,
            )

            cluster = Cluster([data])
            self.set_cluster_bounds(cluster)
            cluster_elongation_max = cluster.get_raw_bounds()[1]

            # Permet de contrôler l'élongation du cluster

            orbs = 0

            # on applique une permutation pour s'assurer que l'angle courant soit à l'indice 0

            wangles = np.roll(angles, -i).tolist()
            wlabels = np.roll(labels, -i).tolist()

            # AJOUT DANS LE CLUSTER COURANT DES PLANETES DONT LA DISTANCE ANGULAIRE A LA PLANÈTE QUI PRÉCÈDE
            # est inférieure à self.orb

            iref = 0

            cluster_elongation_max = wangles[iref] + self.orb / 2.0
            previous_planet_angle = wangles[iref]

            j = 1
            eod1 = nb_records == 0
            while not eod1:

                anglej = wangles[iref+j]
                labelj = wlabels[iref+j]

                if anglej < previous_planet_angle:
                    anglej += 360

                condition1 = anglej <= cluster_elongation_max
                condition2 = (anglej - cluster_elongation_max) <= self.orb / 2.0

                is_planet_in_cluster = condition1 or condition2

                if is_planet_in_cluster:

                    # AJOUT DE LA PLANETE

                    # cluster_elongation_max += self.orb

                    datai = dict(
                        label=labelj,
                        angle=anglej,
                    )
                    cluster.add_planet(datai)
                    self.set_cluster_bounds(cluster)

                    cluster_elongation_max = cluster.get_raw_bounds()[1]

                    planets_in_cluster.append(labelj)
                    orbs += self.orb

                    j += 1
                    i += 1
                    if i > nb_records - 1:
                        eod = True
                    if j > nb_records - 1:
                        eod1 = True
                else:
                    break

            self.add_cluster(cluster)

            i += 1
            if i > nb_records - 1:
                eod = True

    def add_cluster(self, cluster):
        self.add(
            cluster,
        )

    def get_cluster(self, label):

        clusters = self.get_clusters()
        nb_clusters = len(clusters)
        found = False
        i = 0
        eod = i > nb_clusters - 1
        while not eod and not found:
            found, index = clusters[i].contains_planet(label)
            if not found:
                i += 1
                if i > nb_clusters - 1:
                    eod = True
        if found:
            cluster = clusters[i]
        else:
            cluster = None
        return cluster

    def get_asc_mc_clusters(self):
        asc = self.get_cluster("asc")
        mc = self.get_cluster("mc")

        return [asc] if asc == mc else [asc, mc]

    # def get_available_front_positions_number(self, indexes):
    #     nb_indexes = len(indexes)
    #     positions_number = 0
    #     if nb_indexes:
    #         if self.graphical_positions[indexes][0] == b"":
    #             nb_indexes = len(indexes)
    #             eod = nb_indexes == 0
    #             found = False
    #             i = 0
    #             while not found and not eod:
    #                 found = self.graphical_positions[indexes[i]] != b""
    #                 if not found:
    #                     i += 1
    #                     if i > nb_indexes - 1:
    #                         eod = True
    #             if found:
    #                 positions_number = i + 1
    #                 if self.graphical_positions[indexes[i]][0:3] != b"<f>":
    #                     j = indexes[i]
    #                     nb_graphical_positions = len(self.graphical_positions)
    #                     eod = j > nb_graphical_positions - 1
    #                     while not self.graphical_positions[j][0:3] == b"<f>" and not eod:
    #                         if self.graphical_positions[j][0] == b"":
    #                             positions_number += 1
    #                         j += 1
    #                         if i > nb_graphical_positions - 1:
    #                             eod = True
    #             else:
    #                 positions_number = nb_indexes
    #
    #     return positions_number

    # def get_available_back_positions_number(self, indexes):
    #
    #     """
    #     Test d'un décalage en arrière des clusters mobiles afin d'insérer le cluster courant
    #     dans la zone candidate
    #     """
    #     positions_number = 0
    #
    #     nb_graphical_positions = len(self.graphical_positions)
    #     jmax = nb_graphical_positions - 1
    #     graphical_positions = np.roll(self.graphical_positions, jmax - indexes[0])
    #     j = jmax
    #     eod = j < 0
    #     while not graphical_positions[j][0:3] == b"<f>" and not eod:
    #         if graphical_positions[j] == b"":
    #             positions_number += 1
    #         j -= 1
    #         if j < 0:
    #             eod = True
    #
    #     return positions_number

    def update_current_graphical_positions_using_front_strategy(self, indexes, shift_current_cluster=False):
        """
        Test d'un décalage en avant des clusters mobiles afin d'insérer le cluster courant 
        dans la zone candidate
        """

        nb_graphical_positions = len(self.graphical_positions)
        nb_indexes = len(indexes)

        real_shift = 0

        # contrôle

        # la stratégie d'un décalage vers l'avant n'a de sens que lorsqu'un cluster empiète, par l'avant
        # dans la zone du cluster courrant

        validation1 = self.graphical_positions[indexes[-1]][0:3] == b"<f>" or self.graphical_positions[indexes[-1]][0:3] == b"<m>"

        # ou lorsqu'un cluster fixe empiète, par l'arrière dans la zone du cluster courrant :
        # c'est le cluster courant qui doit donc être décalé dans ce cas-là

        validation2 = shift_current_cluster and self.graphical_positions[indexes[-1]] == b""

        if not validation1 and not validation2:
            raise Exception(
                "La stratégie 'front' n'est pas la bonne stratégie à utiliser !!!!"
            )

        shift = 0

        if self.graphical_positions[indexes[0]] == b"":
            """
            La stratégie consiste à aller voir si le prochain cluster qui se trouve devant est mobile ou pas
            """

            # Déplacement jusqu'au cluster

            found = False
            i = 0
            eod = i > nb_indexes - 1
            while self.graphical_positions[indexes[i]] == b"" and not eod:
                i += 1
                eod = i > nb_indexes - 1

            if not eod:
                # on opère une permutation pour éliminer les effets de bord du tableau.
                # => après la permutation, tous les clusters précèdent la position courante

                shift = indexes[i]

                offset = i + 1

                self.graphical_positions = np.roll(self.graphical_positions, - shift)

                j = 0

                while self.is_cluster_insertion_in_progress(indexes, shift=shift) and not eod:

                    # nouveau cluster : fixe ou mobile ?

                    mobile_cluster_index_min = offset + j

                    if self.graphical_positions[j][0:3] == b"<f>":
                        # cluster fixe => pas de décalage possible
                        # => fin de la stratégie
                        break

                    else:
                        # cluster mobile
                        # calcul de la taille du cluster
                        eod = j > nb_graphical_positions - 1
                        while self.graphical_positions[j][0:3] == b"<m>" and not eod:
                            j += 1
                            eod = j > nb_graphical_positions - 1

                        if eod:
                            # la fin du cluster n'a pas été trouvée => cas IMPOSSIBLE
                            raise Exception(
                                "la fin du cluster n'a pas été trouvée, bien que 360° ait été parcouru !!!!"
                            )
                        else:
                            # la fin du cluster a été trouvée
                            mobile_cluster_index_max = mobile_cluster_index_min + j
                            # la position qui est devant ce cluster est-elle libre ?
                            eod1 = j > nb_graphical_positions - 1
                            while self.graphical_positions[j] == b"" and not eod1:
                                if self.is_cluster_insertion_in_progress(indexes, shift=shift):
                                    # la position devant ce cluster est libre
                                    # => la stratégie consiste à décaler le cluster mobile d'une position
                                    for k in range(j, j - (mobile_cluster_index_max - mobile_cluster_index_min + 1), -1):
                                        self.graphical_positions[k] = self.graphical_positions[k-1]
                                        # if k == j + cluster_length - 1:
                                        #     self.graphical_positions[k + 1] = b""
                                    j += 1
                                    eod1 = j > nb_graphical_positions - 1

        else:
            """
            La stratégie consiste à aller voir si le prochain cluster qui se trouve devant est mobile ou pas
            """
            shift = indexes[0]

            self.graphical_positions = np.roll(self.graphical_positions, - shift)

            # Déplacement jusqu'à trouver le bon emplacement
            indexes = np.array(indexes)
            j = 0
            eod = j > nb_graphical_positions - 1

            while self.is_cluster_insertion_in_progress(indexes, shift=shift) and not eod:
                # Tant qu'on a besoin de place, on décale le cluster
                # la stratégie consiste à décaler le cluster d'une position
                indexes += 1
                if len(np.where(indexes >= 360)) > 0:
                    indexes[indexes >= 360] = indexes[indexes >= 360] - 360
                j += 1
                eod = j > nb_graphical_positions - 1

        # on retire la permutation qui n'avait d'utilité que pour l"insertion du décalage
        self.graphical_positions = np.roll(self.graphical_positions, shift)

        return indexes

    def update_current_graphical_positions_using_back_strategy(self, indexes, shift_current_cluster=False):

        # contrôle

        # la stratégie d'un décalage vers l'arrière n'a de sens que lorsqu'un cluster empiète, par l'arrière
        # dans la zone du cluster courrant

        validation1 = \
            self.graphical_positions[indexes[0]][0:3] == b"<f>" or self.graphical_positions[indexes[0]][0:3] == b"<m>"

        # ou lorsqu'un cluster fixe empiète, par l'avant dans la zone du cluster courant :
        # c'est le cluster courant qui doit donc être décalé dans ce cas-là

        validation2 = shift_current_cluster and self.graphical_positions[indexes[0]] == b""

        if not validation1 and not validation2:
            raise Exception(
                "La stratégie 'back' n'est pas la bonne stratégie à utiliser !!!!"
            )

        # on opère une permutation pour éliminer les effets de bord du tableau.
        # => après la permutation, tous les clusters suivent la position courante

        nb_graphical_positions = len(self.graphical_positions)
        jmax = nb_graphical_positions - 1

        real_shift = 0

        nb_indexes = len(indexes)

        if self.graphical_positions[indexes[0]] == b"":

            shift = jmax - indexes[0]

        else:

            i = 0
            eod = i > nb_indexes - 1

            while self.graphical_positions[indexes[i]] != b"" and not eod:
                i += 1
                eod = i > nb_indexes - 1

            if not eod:
                shift = jmax - indexes[i] + 1
            else:
                raise Exception(
                    "Pas d'espace dans la zone réservée au cluster courant. Cas IMOSSIBLE  !!!!"
                )

        self.graphical_positions = np.roll(self.graphical_positions, shift)

        j = jmax
        eod = j < 0

        if self.graphical_positions[indexes[0]] == b"":

            indexes = np.array(indexes)

            # Le cas échéant : décalage du cluster vers l'arrière (cas de la validation2)

            while self.graphical_positions[j] == b"" and not eod:
                # la position derrière ce cluster est libre
                if self.is_cluster_insertion_in_progress(indexes, shift=-shift):
                    # Tant qu'on a besoin de place, on décale le cluster
                    # la stratégie consiste à décaler le cluster d'une position
                    indexes -= 1
                    if len(np.where(indexes < 0)) > 0:
                        indexes[indexes < 0] = indexes[indexes < 0] + 360
                    j -= 1
                    eod = j < 0
                else:
                    break

        while self.is_cluster_insertion_in_progress(indexes, shift=-shift) and not eod:

            # nouveau cluster : fixe ou mobile ?
            mobile_cluster_index_max = j

            if self.graphical_positions[j][0:3] == b"<f>":
                # cluster fixe => pas de décalage possible
                # => fin de la stratégie
                break

            else:
                # cluster mobile
                # calcul de la taille du cluster
                eod = j < 0
                while self.graphical_positions[j][0:3] == b"<m>" and not eod:
                    j -= 1
                    eod = j < 0

                if eod:
                    # le début du cluster n'a pas été trouvée => cas IMPOSSIBLE
                    raise Exception(
                        "la fin du cluster n'a pas été trouvée, bien que 360° ait été parcouru !!!!"
                    )
                else:
                    # la fin du cluster a été trouvée
                    mobile_cluster_index_min = j + 1
                    cluster_length = mobile_cluster_index_max - mobile_cluster_index_min + 1
                    # la position qui est derrière ce cluster est-elle libre ?
                    eod1 = j < 0
                    while self.graphical_positions[j] == b"" and not eod1:
                        # la position devant ce cluster est libre
                        if self.is_cluster_insertion_in_progress(indexes, shift=-shift):
                            # Tant qu'on a besoin de place, on décale le cluster mobile
                            # la stratégie consiste à décaler le cluster mobile d'une position
                            for k in range(j, j + cluster_length, 1):
                                self.graphical_positions[k] = self.graphical_positions[k+1]
                                if k == j + cluster_length - 1:
                                    self.graphical_positions[k + 1] = b""
                            j -= 1
                            eod1 = j < 0
                        else:
                            break

        # on retire la permutation qui n'avait d'utilité que pour l"insertion du décalage
        self.graphical_positions = np.roll(self.graphical_positions, - shift)

        return indexes

    def is_cluster_insertion_in_progress(self, indexes, shift=0):
        graphical_positions = np.roll(self.graphical_positions, shift)
        return sum([len(stri) for stri in graphical_positions[indexes]])

    def update_current_graphical_positions(self, position, identifier, fixed=False):

        success = False

        insertion_aborted = False

        indexes = [i % 360 for i in range(position[0], position[1])]

        if identifier == 'jupiter-saturn':
            print("stop")
        if identifier.find('mercury') >= 0:
            print("stop")
        while self.is_cluster_insertion_in_progress(indexes):

            # choix de la stratégie

            if self.graphical_positions[indexes[0]] == b"":

                indexes = self.update_current_graphical_positions_using_front_strategy(indexes)

                if self.is_cluster_insertion_in_progress(indexes):
                    """
                    les positions libres qui sont situées devant le cluster courant
                    ne permettent pas de le positionner à l'endroit prévu
                    """
                    if fixed:
                        insertion_aborted = True
                    else:
                        indexes = self.update_current_graphical_positions_using_back_strategy(
                            indexes,
                            shift_current_cluster=True,
                        )
                        if self.is_cluster_insertion_in_progress(indexes):
                            insertion_aborted = True
                else:
                    """
                    les positions libres qui sont situées devant le cluster courant
                    permettent de le positionner à l'endroit prévu
                    """

            elif self.graphical_positions[indexes[0]][0:3] == b"<m>":

                indexes = self.update_current_graphical_positions_using_back_strategy(indexes)

                if self.is_cluster_insertion_in_progress(indexes):
                    """
                    les positions libres qui sont situées derrière le cluster courant
                    ne permettent pas de le positionner à l'endroit prévu
                    """
                    indexes = self.update_current_graphical_positions_using_front_strategy(
                        indexes,
                        shift_current_cluster=True,
                    )
                    if self.is_cluster_insertion_in_progress(indexes):
                        insertion_aborted = True
                else:
                    """
                    les positions libres qui sont situées derrière le cluster courant
                    permettent de le positionner à l'endroit prévu
                    """
            else:
                """
                les positions libres qui sont situées derrière le cluster courant
                ne permettent pas de le positionner à l'endroit prévu
                """
                indexes = self.update_current_graphical_positions_using_front_strategy(
                    indexes,
                    shift_current_cluster=True,
                )
                if self.is_cluster_insertion_in_progress(indexes):
                    insertion_aborted = True

            if insertion_aborted:
                # toutes les stratégies ont été testées, et l'insertion a échoué
                break

        if not self.is_cluster_insertion_in_progress(indexes):
            success = True
            self.graphical_positions[np.array(indexes)] = "{} {}".format(
                "<f>" if fixed else "<m>",
                identifier,
            )

        return success

    def calculate_graphical_positions(self):
        success = False
        i = 0
        step = 1  # in degree
        while not success and self.orb > 0:
            self.init_graphical_positions()
            success = self.calculate_graphical_fixed_positions()
            if not success:
                self.orb -= step
                self.update()
        if success:
            success = self.calculate_graphical_flexible_positions()
        return success

    def calculate_graphical_fixed_positions(self):
        clusters = self.get_asc_mc_clusters()
        success = False
        for cluster in clusters:
            position = cluster.get_raw_graphical_position(self.orb)
            success = self.update_current_graphical_positions(position, cluster.get_identifier(), fixed=True)
            if not success:
                break
        return success

    def calculate_graphical_flexible_positions(self):
        success = False
        for cluster in self.get_clusters():
            asc_found, asc_index = cluster.contains_planet("asc")
            mc_found, mc_index = cluster.contains_planet("mc")
            if not asc_found and not mc_found:
                position = cluster.get_raw_graphical_position(self.orb)
                success = self.update_current_graphical_positions(position, cluster.get_identifier())
                if not success:
                    break
        return success

    def get_graphical_positions_perimeter(self, identifier):
        indexes = [i for i, gpi in enumerate(self.graphical_positions) if str(gpi).find(identifier) > 0]
        found = False if len(indexes) == 0 else True
        return found, indexes

    def get_graphical_positions(self):
        success = self.calculate_graphical_positions()
        positions = dict()
        if success:
            for cluster in self.get_clusters():
                identifier = cluster.get_identifier()
                found, perimeter = self.get_graphical_positions_perimeter(identifier)
                if found:
                    position = cluster.get_graphical_position(perimeter, self.orb)
                    if position:
                        positions.update(
                           position,
                        )
                    else:
                        print("ko")
                else:
                    print("ko")

        else:
            raise Exception(
                "Les différentes stratégies de positionnement des planètes dans le thème ont échoué."
                "Le thème ne peut pas être affiché",
            )
        return positions, self.orb

    # def get_graphical_positions2(self):
    #     positions = dict()
    #     for cluster in self.get_clusters():
    #         data = cluster.get_container()
    #         nb_planets = len(data)
    #         if nb_planets == 1:
    #             positions.update(
    #                 {data[0]['label']: data[0]['angle']},
    #             )
    #         else:
    #             indices = list(range(nb_planets))
    #             contains_asc, asc_index = cluster.contains_planet("Asc")
    #             contains_mc, mc_index = cluster.contains_planet("Mc")
    #             if contains_asc and contains_mc:
    #                 ref_index = asc_index
    #                 for i in indices[0:ref_index]:
    #                     anglei = data[ref_index]['angle'] - self.orb * (ref_index - i)
    #                     if anglei < 0:
    #                         anglei += 360
    #                     positions.update(
    #                         {data[i]['label']: anglei},
    #                     )
    #                 positions.update(
    #                     {data[ref_index]['label']: data[ref_index]['angle']},
    #                 )
    #                 for i in indices[ref_index + 1::]:
    #                     anglei = data[ref_index]['angle'] + self.orb * (i - ref_index)
    #                     anglei = anglei % 360
    #                     positions.update(
    #                         {data[i]['label']: anglei},
    #                     )
    #                 # cas possible ???
    #                 print('cas possible ???')
    #             else:
    #                 if contains_asc:
    #                     ref_index = asc_index
    #                 elif contains_mc:
    #                     ref_index = mc_index
    #                 else:
    #                     pair = nb_planets % 2 == 0
    #                     if pair:
    #                         ref_index = -1
    #                     else:
    #                         ref_index = int(nb_planets / 2)
    #
    #                 if ref_index > -1:
    #                     for i in indices[0:ref_index]:
    #                         anglei = data[ref_index]['angle'] - self.orb * (ref_index - i)
    #                         if anglei < 0:
    #                             anglei += 360
    #                         positions.update(
    #                             {data[i]['label']: anglei},
    #                         )
    #                     positions.update(
    #                         {data[ref_index]['label']: data[ref_index]['angle']},
    #                     )
    #                     for i in indices[ref_index+1::]:
    #                         anglei = data[ref_index]['angle'] + self.orb * (i - ref_index)
    #                         anglei = anglei % 360
    #                         positions.update(
    #                             {data[i]['label']: anglei},
    #                         )
    #                 else:
    #                     ref_index = int(nb_planets / 2)
    #                     angle_max = data[-1]['angle']
    #                     angle_min = data[0]['angle']
    #                     if angle_max < angle_min:
    #                         angle_max += 360.0
    #                     center_angle = angle_min + (angle_max - angle_min) / 2.0
    #                     center_angle = center_angle % 360
    #                     for i in indices[0:ref_index]:
    #                         anglei = center_angle - self.orb / 2.0 - self.orb * (ref_index - 1 - i)
    #                         if anglei < 0:
    #                             anglei += 360
    #                         positions.update(
    #                             {data[i]['label']: anglei},
    #                         )
    #
    #                     for i in indices[ref_index::]:
    #                         anglei = center_angle + self.orb / 2.0 + self.orb * (i - ref_index)
    #                         anglei = anglei % 360
    #                         positions.update(
    #                             {data[i]['label']: anglei},
    #                         )
    #
    #     return positions
