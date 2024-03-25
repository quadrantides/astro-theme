# # coding=utf-8
# """
# Created on 2020, May 19th
# @author: orion
# """
#
# from corsheaders.signals import check_request_enabled
#
# from .models.themes import Theme
#
#
# def cors_allow_mysites(sender, request, **kwargs):
#     return True
#
#
# check_request_enabled.connect(cors_allow_mysites)