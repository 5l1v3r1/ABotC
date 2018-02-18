#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileMerger, utils
from subprocess import Popen

class writer():
    def __init__(self):
        self.merger = PdfFileMerger()
        self.local_files = []

    def append(self, doc):
        try:
            self.merger.append(doc)
        except utils.PdfReadError:
            raise Exception('Error')

    def append_local(self, fn):
        self.local_files.append(fn)

        with open(fn, 'rb') as f:
            self.merger.append(f)

    def write(self, date):
        self.merger.write(str(date)+'.pdf')

    def remove_local(self):
        [Popen(['rm', file]) for file in self.local_files]

if __name__ == '__main__':
    exit()