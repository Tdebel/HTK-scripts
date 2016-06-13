import os
import argparse

parser = argparse.ArgumentParser(description='Create a \'script file\' containing sound file paths and their corresponding .mfc file paths.')
parser.add_argument('indir', help='The directory to search for files. All files will be listed.')
parser.add_argument('outdir', help='The directory that .mfc paths will lead to.')
parser.add_argument('outfile', help='The path to the output file.')
args = parser.parse_args()

def inpath(filename):
    return os.path.join(args.indir, filename)

def outpath(filename):
    name, _ = os.path.splitext(filename)
    return os.path.join(args.outdir, name + '.mfc')

scp = {inpath(f):outpath(f) for f in os.listdir(args.indir)}

with open(args.outfile,'w') as f:
    for i,o in scp.items():
        f.write('{} {}\n'.format(i,o))

