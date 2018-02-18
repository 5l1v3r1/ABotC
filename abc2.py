from pandas import date_range
from tqdm import tqdm
import newspaper
import argparse
import writer

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', dest='start', action='store', required=True, type=str)
    parser.add_argument(
        '-e', dest='end', action='store', required=True, type=str)
    
    return parser.parse_args()

args = args()
for date in date_range(args.start, args.end):
    wr = writer.writer()
    np = newspaper.newspaper(date)

    print 'Downloading {} pages of the {}'.format(
        np.pages, str(date).split(' ')[0])

    for page in tqdm(range(1, np.pages+1)):
        doc = np.buff_pdf(page)
       
        try:
            wr.append(doc)
        except Exception:
            fn = np.save_pdf(page)
            wr.append_local(fn)
        
    wr.write(date)
    wr.remove_local()
    print '{} done!\n'.format(str(date).split(' ')[0])
