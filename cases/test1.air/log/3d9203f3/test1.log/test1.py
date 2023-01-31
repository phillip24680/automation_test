# -*- encoding=utf8 -*-
__author__ = "SESA666275"

from airtest.core.api import *

auto_setup(__file__)


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

touch(Template(r"tpl1673860042610.png", threshold=0.9, record_pos=(0.028, -0.2), resolution=(1080, 2340)))

poco(text="Shutter and Switch").click()

