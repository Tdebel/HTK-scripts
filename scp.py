import os
import argparse

def make_scp(indir, outdir, outfile):

    def inpath(filename):
        return os.path.join(indir, filename)

    def outpath(filename):
        name, _ = os.path.splitext(filename)
        return os.path.join(outdir, name + '.mfc')

    with open(outfile,'w') as outfile:
        for f in os.listdir(indir):
            outfile.write('{} {}\n'.format(inpath(f),outpath(f)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a \'script file\' containing sound file paths and their corresponding .mfc file paths.')
    parser.add_argument('indir', help='The directory to search for files. All files will be listed.')
    parser.add_argument('outdir', help='The directory that .mfc paths will lead to.')
    parser.add_argument('outfile', help='The path to the output file.')
    args = parser.parse_args()
    make_scp(args.indir, args.outdir, args.outfile)
