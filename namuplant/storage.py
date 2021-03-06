import os
import csv
import configparser

DOC_F = ['code', 'title', 'rev', 'time', 'index', 'error']
EDIT_F = ['index', 'opt1', 'opt2', 'opt3', 'opt4', 'edit']


def new_setting():
    if not os.path.isfile('config.ini'):  # 최초 생성
        write_config('config.ini',
                     {'login': {'ID': '', 'PW': '', 'UMI': '',
                                'UA': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'},
                      'work': {'DELAY': '3.0'},
                      'window': {'ON_TOP': 0, 'AUTO_INS': 1, 'SKIP_DIFF': 0}})
    # new list log files
    for name, field in (('doc_list.csv', DOC_F), ('doc_log.csv', DOC_F),
                        ('edit_list.csv', EDIT_F), ('edit_log.csv', EDIT_F)):
        if not os.path.isfile(name):  # 최초 생성
            with open(name, 'w', encoding='utf-8', newline='') as csv_file:
                csv.DictWriter(csv_file, field).writeheader()


def write_config(file_name, section_dict):  # 이중 딕셔너리
    config = configparser.ConfigParser()
    config.optionxform = str
    for section, value in section_dict.items():
        config[section] = value
    with open(file_name, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def read_config(file_name):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(file_name, encoding='utf-8')
    return dict(zip(config.sections(), [dict([v for v in config[section].items()]) for section in config.sections()]))


def write_csv(file_name, option, field):
    field = {'doc': DOC_F, 'edit': EDIT_F}[field]
    with open(file_name, option, encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, field)
        if option == 'w':
            writer.writeheader()
        while True:
            to_write = (yield)  # dict
            writer.writerow(to_write)


def read_csv(file_name):
    with open(file_name, 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            yield dict(row)


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.c = read_config(self.filename)

    def save(self, login=None, delay=None, on_top=None, auto_ins=None, skip_diff=None):
        if login is not None:
            self.c['login'] = login
        if delay is not None:
            self.c['work']['DELAY'] = round(delay, 1)
        if on_top is not None:
            self.c['window']['ON_TOP'] = on_top
        if auto_ins is not None:
            self.c['window']['AUTO_INS'] = auto_ins
        if skip_diff is not None:
            self.c['window']['SKIP_DIFF'] = skip_diff
        write_config(self.filename, self.c)
