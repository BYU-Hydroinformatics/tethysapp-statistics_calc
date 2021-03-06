# Most of your test classes should inherit from TethysTestCase
import unittest
from tethys_sdk.testing import TethysTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# Use if your app has persistent stores that will be tested against.
# Your app class from app.py must be passed as an argument to the TethysTestCase functions to both
# create and destroy the temporary persistent stores for your app used during testing
# from ..app import StatisticsCalc

# Use if you'd like a simplified way to test rendered HTML templates.
# You likely need to install BeautifulSoup, as it is not included by default in Tethys Platform
#    1. Open a terminal
#    2. Enter command ". /usr/lib/tethys/bin/activate" to activate the Tethys python environment
#    3. Enter command "pip install beautifulsoup4"
# For help, see https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# from bs4 import BeautifulSoup

"""
To run any tests:
    1. Open a terminal
    2. Enter command ". /usr/lib/tethys/bin/activate" to activate the Tethys python environment
    3. In settings.py make sure that the tethys_default database user is set to tethys_super
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'tethys_default',
                'USER': 'tethys_super',
                'PASSWORD': 'pass',
                'HOST': '127.0.0.1',
                'PORT': '5435'
            }
        }
    4. Enter tethys test command.
       The general form is: "tethys test -f tethys_apps.tethysapp.<app_name>.<folder_name>.<file_name>.<class_name>.<function_name>"
       See below for specific examples

        To run all tests across this app:
            Test command: "tethys test -f tethys_apps.tethysapp.statistics_calc"

        To run all tests in this file:
            Test command: "tethys test -f tethys_apps.tethysapp.statistics_calc.tests.tests"

        To run tests in the StatisticsCalcTestCase class:
            Test command: "tethys test -f tethys_apps.tethysapp.statistics_calc.tests.tests.StatisticsCalcTestCase"

        To run only the test_if_tethys_platform_is_great function in the StatisticsCalcTestCase class:
            Test command: "tethys test -f tethys_apps.tethysapp.statistics_calc.tests.tests.StatisticsCalcTestCase.test_if_tethys_platform_is_great"

To learn more about writing tests, see:
    https://docs.djangoproject.com/en/1.9/topics/testing/overview/#writing-tests
    https://docs.python.org/2.7/library/unittest.html#module-unittest
"""


class StatisticsCalcTestCase(TethysTestCase):
    """
    In this class you may define as many functions as you'd like to test different aspects of your app.
    Each function must start with the word "test" for it to be recognized and executed during testing.
    You could also create multiple TethysTestCase classes within this or other python files to organize your tests.
    """

    def set_up(self):
        """
        This function is not required, but can be used if any environmental setup needs to take place before
        execution of each test function. Thus, if you have multiple test that require the same setup to run,
        place that code here. For example, if you are testing against any persistent stores, you should call the
        test database creation function here, like so:

            self.create_test_persistent_stores_for_app(StatisticsCalc)

        If you are testing against a controller that check for certain user info, you can create a fake test user and
        get a test client, like so:

            #The test client simulates a browser that can navigate your app's url endpoints
            self.c = self.get_test_client()
            self.user = self.create_test_user(username="joe", password="secret", email="joe@some_site.com")
            # To create a super_user, use "self.create_test_superuser(*params)" with the same params

            # To force a login for the test user
            self.c.force_login(self.user)

            # If for some reason you do not want to force a login, you can use the following:
            login_success = self.c.login(username="joe", password="secret")

        NOTE: You do not have place these functions here, but if they are not placed here and are needed
        then they must be placed at the beginning of your individual test functions. Also, if a certain
        setup does not apply to all of your functions, you should either place it directly in each
        function it applies to, or maybe consider creating a new test file or test class to group similar
        tests.
        """
        pass

    def tear_down(self):
        """
        This function is not required, but should be used if you need to tear down any environmental setup
        that took place before execution of the test functions. If you are testing against any persistent
        stores, you should call the test database destruction function from here, like so:

            self.destroy_test_persistent_stores_for_app(StatisticsCalc)

        NOTE: You do not have to set these functions up here, but if they are not placed here and are needed
        then they must be placed at the very end of your individual test functions. Also, if certain
        tearDown code does not apply to all of your functions, you should either place it directly in each
        function it applies to, or maybe consider creating a new test file or test class to group similar
        tests.
        """
        pass

    def test_home_controller(self):
        """
        This is an example test function of how you might test a controller that returns an HTML template rendered
        with context variables.
        """

        # If all test functions were testing controllers or required a test client for another reason, the following
        # 3 lines of code could be placed once in the set_up function. Note that in that case, each variable should be
        # prepended with "self." (i.e. self.c = ...) to make those variables "global" to this test class and able to be
        # used in each separate test function.
        c = self.get_test_client()
        user = self.create_test_user(username="joe", password="secret", email="joe@some_site.com")
        c.force_login(user)

        # Have the test client "browse" to your home page
        response = c.get('/apps/statistics-calc/')  # The final '/' is essential for all pages/controllers

        # Test that the request processed correctly (with a 200 status code)
        self.assertEqual(response.status_code, 200)

        '''
        NOTE: Next, you would likely test that your context variables returned as expected. That would look
        something like the following:
        
        context = response.context
        self.assertEqual(context['my_integer'], 10)
        '''


class HydroStatsPreprocessTesting(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(r'/usr/local/bin')

    def test_ideal_case(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8000/apps/statistics-calc/preprocessing/")
        self.assertIn("Tethys", driver.title)

        # Username
        elem = driver.find_element_by_id("id_username")
        elem.send_keys('admin')
        # Password
        elem = driver.find_element_by_id("id_password")
        elem.send_keys('pass')

        # Button
        elem = driver.find_element_by_xpath('// *[ @ id = "login-submit"]')
        elem.click()

        time.sleep(2)

        # CSV File
        driver.execute_script("document.getElementById('pps_csv').style.display = 'block'")
        elem = driver.find_element_by_id('pps_csv')
        elem.send_keys(os.path.join(os.getcwd(), "Asaraghat_observed.csv"))

        # Change Units
        elem = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div[4]/div/label[1]')
        elem.click()

        # Plot
        elem = driver.find_element_by_xpath('//*[@id="raw_data_plot_button"]')
        elem.click()

    def tearDown(self):
        self.driver.close()
