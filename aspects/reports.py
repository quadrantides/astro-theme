# coding=utf-8
"""
Created on 2020, June 9th
@author: orion
"""
from datetime import datetime as dt


def execute(process, logger=None, save=False):

    if not logger:
        logger = process.get_logger()

    logger.info(
        "DÉBUT DU SCRIPT DE RECHERCHE DES ASPECTS",
    )

    logger.info(
        "BASE DE LA RECHERCHE".format(
            process.time_range[0],
            process.time_range[1],
        ),
    )
    logger.info(
        "< DATE DÉBUT : {} - DATE FIN : {} >".format(
            process.time_range[0],
            process.time_range[1],
        ),
    )
    logger.info(
        "< PLANÈTES : {} - {} >".format(
            process.planet1,
            process.planet2,
        ),
    )
    logger.info(
        "< ANGLES : {} - ORBS : {} >".format(
            process.angles,
            process.orbs,
        ),
    )
    logger.info(
        "LANCEMENT DE LA RECHERCHE DES ASPECTS",
    )

    begin = dt.now()

    process.add_logger(logger)

    if save:
        process.calculate_if_not_exists()
    else:
        process.calculate(visualize=True)

    logger.info(
        "FIN DE LA RECHERCHE DES ASPECTS",
    )
    logger.info(
        "FIN DU SCRIPT DE RECHERCHE DES ASPECTS",
    )

    end = dt.now()
    duration = end - begin

    total_seconds = duration.total_seconds()
    if total_seconds > 1:
        total_seconds = int(total_seconds)

    msg = "DURÉE DE L'EXÉCUTION DU SCRIPT : {} secondes".format(
        total_seconds,
    )

    logger.info(
        msg,
    )
