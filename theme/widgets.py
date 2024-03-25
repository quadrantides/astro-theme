# coding=utf-8
"""
Created on 2020, May 16th
@author: orion
"""

from django.forms import DateTimeInput


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker.html'
