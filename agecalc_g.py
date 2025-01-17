#!/usr/bin/python

from fractions import Fraction

epoch = 1721426 - 366 # Julian Day of 1st January of the year 0
cycle400 = (400 * 365) + 97 # days in 400 Gregorian years
century = (100 * 365) + 24 # days in 11 Gregorian years
quad = (4 * 365) + 1 # days in 4 Gregorian years
mean_year = Fraction(cycle400, 400) # days in a mean Gregorian year

month_lengths = {365: (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31), # normal years
                 366: (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)} # leap years

def year_length(year):
    '''Compute number of days in a year'''
    year = int(year)

    if (year % 400 == 0):
        # leap year
        ans = 366
    elif (year % 100 == 0):
        # normal year
        ans = 365
    elif (year % 4 == 0):
        # leap year
        ans = 366
    else:
        # normal year
        ans = 365

    return ans

def nyd(year):
    '''Compute the Julian Day on which New Year's Day of a given year falls'''
    year = int(year)

    cycles = year // cycle400
    y = 400 * cycles
    ans = epoch + (cycles * cycle400) # new year's day

    if (y + 100 <= year):
        y += 100
        ans += 36525 # 100 years with 25 leap years

        while (y + 100 <= year):
            y += 100
            ans += century

    if ( (y + 4 <= year) and (year_length(y) == 365) ):
        # four-year period without a leap year
        y += 4
        ans += (4 * 365)

    while (y + 4 <= year):
        y += 4
        ans += quad

    while (y < year):
        ans += year_length(y)
        y += 1

    return ans

def tojd(day, month, year):
    '''Convert a date in the Gregorian calendar to a Julian Day'''
    day = int(day) - 1 # subtract 1 because computers count from 0
    month = int(month) - 1 # subtract 1 because computers count from 0
    year = int(year) # don't subtract 1 because we're assuming there is a year 0

    l = month_lengths[year_length(year)]

    # account for the year
    jd = nyd(year)

    # account for the month
    m = 0
    while (m != month):
        jd += l[m]
        m += 1

    # add the day
    jd += day

    return jd

def timediff(start, end):
    '''Compute the time between two dates, in mean Gregorian years'''
    start = str(start) # start date, in yyyy-mm-dd format
    end = str(end) # end date, in yyyy-mm-dd format

    start_day = int(start[len(start) - 2:]) # day of the month
    start_month = int(start[len(start) - 5:len(start) - 3]) # number of the month
    start_year = int(start[:len(d) - 6]) # number of the year. 0 is a valid year number

    end_day = int(end[len(end) - 2:]) # day of the month
    end_month = int(end[len(end) - 5:len(end) - 3]) # number of the month
    end_year = int(end[:len(d) - 6]) # number of the year. 0 is a valid year number

    delta = tojd(end_day, end_month, end_year) - tojd(start_day, start_month, start_year)
    ans = Fraction(delta, mean_year)

    return ans
