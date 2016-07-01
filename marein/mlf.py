import os, re
import argparse

def extract(filename,regex):
    return re.search(regex,filename).group(1)

# create a grammar file based on files in a folder and a regular expression
def folder(out,path,regex):
    words = {(f,extract(f,regex)) for f in os.listdir(path)}
    with open(out,'w') as f:
        f.write('#!MLF!#\n')
        for file,word in words:
            f.write('"*/{}"\n{}\n.\n'.format(file,word))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Methods for creating a Master Label File.')
    parser.add_argument('outfile', type=str)
    # TODO: should use subparsers
    parser.add_argument('-f', '--folder',type=str)
    parser.add_argument('-r', '--regex',type=str)
    args = parser.parse_args()
    if args.folder:
        folder(args.outfile,args.folder,args.regex)

