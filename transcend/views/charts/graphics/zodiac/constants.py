# coding=utf-8
"""
Created on 2020, April 16th
@author: orion
"""
VERSION = "1.0"

COLORS = ["#ffffff"] * 12


def get_domain(pie_width):

    domain_px = 1.0 - pie_width
    domain_dy = domain_px

    domain = {
        'x':
            [
                0 + domain_px / 2,
                1 - domain_px / 2,
            ],

        'y':
            [
                0 + domain_dy / 2,
                1 - domain_dy / 2,
            ],
    }
    return domain
