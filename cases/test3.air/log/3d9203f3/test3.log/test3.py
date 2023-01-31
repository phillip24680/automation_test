# -*- encoding=utf8 -*-
__author__ = "SESA666275"

from airtest.core.api import *

auto_setup(__file__)


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

poco(text="Shutter and Switch").swipe([1,0])
poco(text="All Devices").click()
