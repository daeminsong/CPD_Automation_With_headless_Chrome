import unittest
from os import path, remove
from time import sleep
from driver_builder import DriverBuilder
from get_id import peripharial_info
from selenium.webdriver.common.keys import Keys
from extract_data import excel_data
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException


class CPA_CPD():

    web_site_address = 'https://cpamb.ca/login'

    def login_to_website(self):
        id_info, pw_info = peripharial_info().get_user_info()
        driver_builder = DriverBuilder()
        driver = driver_builder.get_driver(headless=False)
        driver.get(self.web_site_address)
        element_id = driver.find_element_by_id("cphContent_C001_txtUserName")
        self.wait_until_page_refreshed(element_id)
        element_id.clear()
        element_id.send_keys(id_info) #id_info
        element_pw = driver.find_element_by_id("cphContent_C001_txtPassword")
        element_pw.clear()
        element_pw.send_keys(pw_info) #pw_info
        driver.find_element_by_id("cphContent_C001_btnLogin").click()
        return driver

    def main(self):
        list = excel_data().data_complete()
        driver = self.login_to_website()
        driver.get(self.web_site_address)
        element_link_text = driver.find_element_by_link_text("CPD Reporting")
        self.wait_until_page_refreshed(element_link_text)
        driver.find_element_by_link_text("CPD Reporting").click()
        driver.find_element_by_link_text("Submit Hours").click()
        ###
        verifiability_option = {'Unverifiable':'cphContent_C002_radUnverifiable', 'Ethics':'cphContent_C002_radEthics', 'Verifiable':'cphContent_C002_radVerifiable'}
        ###
        for i in range(int((len(list) + 1) / 5)):
            driver.find_element_by_id(verifiability_option[list[0]]).click()
            self.check_clickable(driver, 'cphContent_C002_txtHours')
            # driver.find_element_by_id('cphContent_C002_txtHours').clear()
            driver.find_element_by_id('cphContent_C002_txtHours').send_keys(list[1])
            # driver.find_element_by_id('cphContent_C002_txtActivityName').clear()
            driver.find_element_by_id('cphContent_C002_txtActivityName').send_keys(list[2])
            # driver.find_element_by_id('ctl00_cphContent_C002_rdpActivityDate_dateInput').clear()
            driver.find_element_by_id('ctl00_cphContent_C002_rdpActivityDate_dateInput').send_keys(list[3])
            # driver.find_element_by_id('cphContent_C002_txtActivityDescription').clear()
            driver.find_element_by_id('cphContent_C002_txtActivityDescription').send_keys(list[4])
            driver.find_element_by_id('cphContent_C002_lbtnSave').click()
            del list[0:5]
        driver.close()
        print("done")
        raise SystemExit

    def check_clickable(self, driver, selector, attempts=15):
        #credit - https://stackoverflow.com/questions/45653801/selenium-wait-for-element-to-be-clickable-not-working?rq=1
        count = 0
        while driver.find_element_by_id(selector).get_attribute('value') and not count > attempts:
            try:
                sleep(1)
                print("Waiting...." + str(count))
                count += 1
                return None
            except WebDriverException as e:
                if ('is not clickable at point' in str(e)):
                    print('Retrying clicking on button.')
                    count += 1
                else:
                    raise e
            raise TimeoutException('custom_wait_clickable timed out')

    def check_history(self):
        driver = self.login_to_website()
        driver.get(self.web_site_address)
        element_link_text = driver.find_element_by_link_text("CPD Reporting")
        self.wait_until_page_refreshed(element_link_text)
        driver.find_element_by_link_text("CPD Reporting").click()
        driver.find_element_by_link_text("History").click()
        while True:
            sleep(1)

    def wait_until_page_refreshed(self, element, wait_time_in_seconds=5):
        # make sure the webpage has been refreshed before move onto the next step
        waits = 0
        while not element.is_displayed() and waits < wait_time_in_seconds:
            print("Waiting...." + str(waits))
            sleep(.5)
            waits += .5


# if __name__=='__main__':
#     main()
# CPA_CPD().main()
CPA_CPD().check_history()
