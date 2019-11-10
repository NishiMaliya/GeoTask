import glob
import datetime
import logging
from datetime import datetime
from dataclasses import dataclass
from calendar import monthrange

_logger = logging.getLogger().setLevel(logging.INFO)


@dataclass
class Days:
    coldest_day: dict
    hottest_day: dict


@dataclass
class Months:
    coldest_month: dict
    hottest_month: dict


def read_file(file_path):
    data = []
    with open(file_path, encoding='UTF-8') as csv_file:
        for each_line in csv_file.readlines()[7:]:
            line = each_line.split(';')
            data.append(line)
    return data


def get_hottest_and_coldest_days(data: list):
    sum_day_temperature = 0
    avg_max_temperature = 0
    current_day = 0
    avg_min_temperature = 0
    max_temperature_day = ""
    min_temperature_day = ""
    for index, line in enumerate(data, start=0):
        date = parse_date(line)
        if date.tm_mday != current_day:
            current_avg_temperature = sum_day_temperature / 8
            sum_day_temperature = 0
            current_day = date.tm_mday
            if current_avg_temperature > avg_max_temperature:
                avg_max_temperature = current_avg_temperature
                max_temperature_day = get_previous_element(data, index)
            if current_avg_temperature < avg_min_temperature:
                avg_min_temperature = current_avg_temperature
                min_temperature_day = get_previous_element(data, index)
        current_temperature = change_temperature_type(line)
        sum_day_temperature += current_temperature
    return Days({min_temperature_day: avg_min_temperature}, {max_temperature_day: avg_max_temperature})


def get_hottest_and_coldest_months(data: list):
    sum_month_temperature = 0
    avg_max_temperature = 0
    current_month = 1
    avg_min_temperature = 0
    max_month_temperature = ""
    min_month_temperature = ""
    for index, line in enumerate(data, start=0):
        date = parse_date(line)
        mon = date.tm_mon
        if mon != current_month:
            current_avg_temperature = sum_month_temperature / (get_number_of_month_days(parse_date(data[index-1]))*8)
            sum_month_temperature = 0
            current_month = mon
            if current_avg_temperature > avg_max_temperature:
                avg_max_temperature = current_avg_temperature
                max_month_temperature = get_previous_element(data, index)
            if current_avg_temperature < avg_min_temperature:
                avg_min_temperature = current_avg_temperature
                min_month_temperature = get_previous_element(data, index)
        current_temperature = change_temperature_type(line)
        sum_month_temperature += current_temperature
    return Months({min_month_temperature: avg_min_temperature}, {max_month_temperature: avg_max_temperature})


def get_number_of_month_days(date):
    return monthrange(date.tm_year, date.tm_mon)[1]


def get_previous_element(data, index):
    return data[index - 1][0]


def change_temperature_type(line):
    return float(line[1].strip('"'))


def parse_date(line):
    return datetime.strptime(line[0].strip('"'), "%d.%m.%Y %H:%M").timetuple()


if __name__ == "__main__":
    data = read_file(glob.glob('./*.csv')[0])
    days_result = get_hottest_and_coldest_days(data)
    months_result = get_hottest_and_coldest_months(data)
    logging.info(f"The coldest day is {days_result.coldest_day}")
    logging.info(f"The coldest month is {months_result.coldest_month}")
    logging.info(f"The hottest day is {days_result.hottest_day}")
    logging.info(f"The hottest month is {months_result.hottest_month}")
