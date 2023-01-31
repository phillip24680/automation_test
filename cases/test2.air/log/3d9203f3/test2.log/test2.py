# -*- encoding=utf8 -*-
__author__ = "SESA666275"

from airtest.core.api import *

auto_setup(__file__)


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

touch(Template(r"tpl1673860094318.png", threshold=0.9, record_pos=(-0.439, -0.937), resolution=(1080, 2340)))
poco("com.elko.home:id/tv_close_left").click()

