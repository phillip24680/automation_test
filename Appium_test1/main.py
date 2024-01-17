from appium import webdriver
import time

desired_caps={
    "platformName":"Android",
    "platformVersion":"12",
    "deviceName":"V2217A",
    "appPackage":"com.elko.home",
    "appActivity":"com.smart.TuyaSplashActivity",
    "noReset":True
}


driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desired_caps)
driver.implicitly_wait(10)

#driver.find_element('-android uiautomator','UiSelector().text("同意")').click()
driver.find_element('xpath','//android.widget.TextView[@content-desc="dialog_confirm"]').click()

driver.implicitly_wait(10)
driver.find_element('id','com.elko.home:id/btn_wiser_login').click()
driver.implicitly_wait(10)
#driver.find_element('id','com.elko.home:id/rl_country_code').click()

# ele_account = driver.find_element('-android uiautomator','UiSelector().text("输入手机号 / 邮箱")')
# ele_account.send_keys('phillip_ft@mailinator.com')

driver.find_element('id','com.elko.home:id/edt_password').click()

time.sleep(2)
#driver.find_element('id','com.elko.home:id/edt_account').click()

# ele_password.send_keys('Wu@123456')
# driver.implicitly_wait(3)
#
# driver.find_element('-android uiautomator','UiSelector().text("登录")').click()