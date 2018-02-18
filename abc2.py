#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules import newspaper, writer
from tqdm import tqdm
import argparse
import datetime

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', dest='start', action='store', required=True, type=str)
    parser.add_argument(
        '-e', dest='end', action='store', required=False, type=str, default='')
    
    args = parser.parse_args()
    args.end = args.start if args.end == '' else args.end
    return args

def dates(start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    step = datetime.timedelta(days=1)

    while start <= end:
        yield start.date()
        start += step


args = args()
for date in dates(args.start, args.end):
    wr = writer.writer()
    np = newspaper.newspaper(date)

    print('Downloading {} pages of the {}'.format(
        np.pages, str(date)))

    for page in tqdm(range(1, np.pages+1)):
        doc = np.buff_pdf(page)
       
        try:
            wr.append(doc)
        except Exception:
            fn = np.save_pdf(page)
            wr.append_local(fn)
        
    wr.write(date)
    wr.remove_local()
    print('{} done!\n'.format(str(date)))
