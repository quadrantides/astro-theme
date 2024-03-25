# coding=utf-8
"""
Created on 2021, Feb 13th
@author: orion
"""
from bokeh.palettes import Category20, RdPu

COLORS = Category20[20]
RdPu5 = RdPu[5]
VERSION = "1.0"

DIRECT_BODIES_COLORS = dict(
    sun="#FDE724",
    moon=COLORS[15],
    mercury=COLORS[11],
    venus=RdPu5[3],
    mars=COLORS[7],
    jupiter=COLORS[9],
    saturn=COLORS[5],
    uranus=COLORS[19],
    neptune=COLORS[1],
    pluto=COLORS[17],
    chiron=COLORS[3],
)
