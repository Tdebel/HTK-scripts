import os
import argparse
import subprocess
from scp import make_scp
from collections import Counter

SUPPORTED_TYPES = ['htk','timit','nist','scribe','sdes1','aiff','sunaub','ogi','wav']

# return the most common filetype in the given dir
def most_common_type(dir):
    files = os.listdir(dir)
    types = [os.path.splitext(f)[1] for f in files]
    counter = Counter(types)
    return counter.most_common(1)[0][0][1:]

# write a hcopy config file to filename based on args
def make_config(args,filename):
    with open(filename,'w') as f:
        t = most_common_type(args.indir)
        if t.lower() not in SUPPORTED_TYPES:
            raise ValueError('Filetype {} is not supported by HTK.'.format(t))
        f.write('SOURCEFORMAT = {}\n'.format(t.upper()))
        f.write('TARGETKIND = {}\n'.format(args.targetkind))
        f.write('TARGETRATE = {}\n'.format(args.targetrate))
        f.write('SAVECOMPRESSED = {}\n'.format(args.compressed))

# hcopy the files from indir to outdir given args
def hcopy(indir,outdir,args):
    scp_file = 'hcopy_temp.scp'
    config_file = 'hcopy_temp.config'
    make_scp(indir,outdir,scp_file)
    make_config(args,config_file)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    subprocess.call(['HCopy','-C',config_file,'-S',scp_file])
    os.remove(scp_file)
    os.remove(config_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Given input and output directories, convert the input to .mfc files based on the arguments.')
    parser.add_argument('indir', help='The directory containing the input sound files.')
    parser.add_argument('outdir', help='The target directory for the converted files.')
    parser.add_argument('-k', '--targetkind', nargs='?', default='MFCC_0_D', type=str)
    parser.add_argument('-r', '--targetrate', nargs='?', default=100000.0, type=float)
    parser.add_argument('-c', '--compressed', nargs='?', default='T', choices=['T','F'])
    args = parser.parse_args()
    hcopy(args.indir,args.outdir,args)
