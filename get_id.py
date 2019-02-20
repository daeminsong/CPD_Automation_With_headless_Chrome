from time import sleep
from datetime import date
import datetime, calendar
from dateutil.relativedelta import relativedelta
import holidays
import pyperclip
import getpass

#https://www.google.com/search?newwindow=1&safe=active&client=firefox-b-ab&ei=MXv1W6CWLMvEjwT706X4BA&q=pyinstaller+selenium&oq=pyinstaller+selenium&gs_l=psy-ab.3.1.0j0i22i30l2.1107088.1108426..1108784...0.0..0.194.1224.0j8......0....1..gws-wiz.......0i71j0i67j0i20i263.r6Xd8Sl7m0w
#https://stackoverflow.com/questions/49579558/trouble-getting-the-current-url-on-selenium
class peripharial_info():
    def workdays_calculator(self):
        ''' This funcion will get the '''
        now = date.today() #YYYY-MM-DD format
        dt = datetime.datetime(now.year, now.month, now.day)
        i = 1
        dt1 = datetime.date(dt.year, dt.month, dt.day) - datetime.timedelta(days = i)
        while True:
            if ((self.holiday_checker(dt1.year, dt1.month, dt1.day) != True) and (dt1.weekday() != 5 and dt1.weekday() != 6)):
                break
            dt1 = dt1 - datetime.timedelta(days = i)
        return dt1

    def holiday_checker(self, dt_year, dt_month, dt_day):
        ''' This function will check whether or not a particulary day is a holiday
        and return.'''
        ca_holidays = holidays.CountryHoliday('CA', prov='MB')
        return date(dt_year, dt_month, dt_day) in ca_holidays

    def last_day_of_month(self, any_day):  # the argument should be - (datetime.date(YYYY,MM,DD))
        '''get the last day of the month'''
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)

    def get_user_info(self):
        id_info = input('Please enter your id\n - ')
        pw_reveal = self.ask_ok('would you prefer the password to be shown when you type? (y/n) - ')
        if pw_reveal == False:
            pw_info = getpass.getpass('Please enter you password (it won\'t show anything, but it still works! \
        :\n - ')
        else:
            pw_info = input('Please enter your password\n - ')
        return id_info, pw_info

    def ask_ok(self, prompt, retries=1, reminder='please try again! only (y/n)'):
        '''Ask a user y/n and return True = Y, False = N'''
        while True:
            ok = input(prompt)
            if ok in ('y', 'ye', 'yes', 'yep'):
                return True
            if ok in ('n', 'no', 'nop', 'nope'):
                return False
            retries = retries - 1
            if retries < 0:
                raise ValueError('invalid user response')
            print(reminder)
