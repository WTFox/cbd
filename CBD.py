# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)
import configparser
import os
import shutil
import datetime


__author__ = 'anthonyfox'


class CBDDocExplorer(object):
    ''' Class to manipulate CBD Config.

        :param filename: Filename to the config file.

        Usage:
            f = CBDConfig('20150427 - Accounting_RSP.txt')

        Methods:
            add_folder(item, parent)

    '''

    def __init__(self, filename):
        self.filename = filename
        self._backup_file()
        self.config = configparser.ConfigParser(strict=False)

    def add_folder(self, item, parent):
        ''' Main method for adding folders.
            Usage:
                f.add_folder('Westfield', 'gb')
                f.add_folder('Westfield', 'pc')
                f.add_folder(['Westfield', 'Apple'], 'pc')

        '''

        if parent == 'pc':
            parent = 'P&C Direct Bill Statements'
        elif parent == 'gb':
            parent = 'Group Benefits Statements'

        if isinstance(item, list):
            for x in item:
                self._add_item(x, parent)

        self._add_item(item, parent)

        return


    def _add_item(self, new_item, parent):
        ''' Adds the folder to the CBD library and sorts it.

            Currently does not sort the sub items in Group Benefits

        '''
        with open(self.filename, 'r') as configfile:
            self.config.readfp(configfile)

        section = self.config[parent]

        new_items = []
        for index, item in enumerate(section):
            # Skipping count
            if index is not 0:
                new_items.append(section[item])
        new_items.append(new_item)
        new_items = sorted(new_items, key=str.lower)
        self.config.set(section.name, 'count', str(int(section['count']) + 1))
        for i, item in enumerate(new_items):
            self.config.set(section.name, 'item' + str(i + 1), item)

        if parent == 'Group Benefits Statements':
            self._add_sub_section(new_item)
            # self._clean_up()

        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

        return


    def _add_sub_section(self, new_item):
        ''' Adds the subfolders for GB

        '''
        self.config.add_section(new_item)
        self.config.set(new_item, 'count', '9')
        for i, x in enumerate(range(2012, 2021)):
            i += 1
            key = 'item' + str(i)
            value = str(x)
            self.config.set(new_item, key, value)

        return


    def _backup_file(self):
        ''' Backs the file up in case something goes wrong.

        '''
        if not os.path.exists('backup/'):
            os.makedirs('backup')
        shutil.copyfile(self.filename, 'backup/' + str(self.filename) + str(datetime.datetime.now()) + '.bak')
        return


    def _clean_up(self):
        sections = self.config.sections()
        start = sections.index('Group Benefits Statements')+1
        sections = sorted(sections[start:], key=str.lower)
        for section in sections:
            if section == 'Vision Services' or section == 'Cash Receipts':
                pass

            self.config.remove_section(section)
            self._add_sub_section(section)

        return

if __name__ == "__main__":
    f = CBDConfig('20150427 - Accounting_RSP.txt')
    f.clean_up()
