import os, re
import argparse

def extract(filename,regex):
    return re.search(regex,filename).group(1)

# create a grammar file based on files in a folder and a regular expression
def folder(out,path,regex):
    words = {extract(f,regex) for f in os.listdir(path)}
    with open(out,'w') as f:
        f.write('$word = {}\n'.format(' | '.join(words)))
        f.write('( [silence] $word [silence] )\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Methods for creating a grammar file.')
    parser.add_argument('outfile', type=str)
    # TODO: should use subparsers
    parser.add_argument('-f', '--folder',type=str)
    parser.add_argument('-r', '--regex',type=str)
    args = parser.parse_args()
    if args.folder:
        folder(args.outfile,args.folder,args.regex)

