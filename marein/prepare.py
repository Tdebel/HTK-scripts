import os, re
import argparse, functools, subprocess
from shutil import copyfile
from collections import Counter

call = functools.partial(subprocess.call,shell=True)

def extract(filename,regex):
	return re.search(regex,filename).group(1)

# create a grammar file based on files in a folder and a regular expression
def gram_folder(out,path,regex):
	words = {extract(f,regex) for f in os.listdir(path)}
	with open(out,'w') as f:
		f.write('$word = {};\n'.format(' | '.join(words)))
		f.write('( [silence] $word [silence] )\n')

# create an MLF file based on files in a folder and a regular expression
def mlf_folder(out,path,regex):
    words = {(f,extract(f,regex)) for f in os.listdir(path)}
    with open(out,'w') as f:
        f.write('#!MLF!#\n')
        for file,word in words:
            f.write('"*/{}"\n{}\n.\n'.format(file,word))

def replace_numbers(file):
	with open(file) as f:
		text = f.read()
		for i,c in zip(range(10),'abcdefghij'):
			text = text.replace(str(i),'n{}'.format(c))
	with open(file,'w') as f:
		f.write(text)

def make_scp(indir, outdir, outfile):
    def inpath(filename):
        return os.path.join(indir, filename)
    def outpath(filename):
        name, _ = os.path.splitext(filename)
        return os.path.join(outdir, name + '.mfc')
    with open(outfile,'w') as outfile:
        for f in os.listdir(indir):
            outfile.write('{} {}\n'.format(inpath(f),outpath(f)))

# return the most common filetype in the given dir
def most_common_type(dir):
    files = os.listdir(dir)
    types = [os.path.splitext(f)[1] for f in files]
    counter = Counter(types)
    return counter.most_common(1)[0][0][1:].upper()

 def add_sourceformat_to_config(indir,config_in,config_out):
    copyfile(config_in,config_out)
    filetype = most_common_type(indir)
    with open(config_out,'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write('SOURCEFORMAT = {}\n'.format(filetype) + content)
    
# hcopy the files from indir to outdir given a config file
def hcopy(indir,outdir,config):
    scp = 'scp'
    make_scp(indir,outdir,scp)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    config_prepare = config+'_prepare'
    add_sourceformat_to_config(indir,config,config_prepare)
    subprocess.call(['HCopy','-C',config_prepare,'-S',scp])
		
def prepare(indir,outdir,regex,config,dict):
	gram_folder('gram',indir,regex)
	call('HParse gram wdnet')
	call("cut -d' ' -f1 {} > words".format(dict))
	call('cat words | LC_ALL=C sort | uniq > wlist')
	call('cat {} | LC_ALL=C sort | uniq > ordered_dict'.format(dict))
	replace_numbers('ordered_dict')
	call("sed -e 's/\t/\t1\t/' -i ordered_dict")
	call('HDMan -m -w wlist -n monophones -i dict ordered_dict')
	call("echo 'sil' >> monophones")
	call("echo -e 'silence\t[silence]\tsil' >> dict")
	call("sort dict -o dict")
	mlf_folder('words.mlf',indir,regex)
	hcopy(indir,outdir,config)
    
# python prepare.py ../../material/segmentations mfc "cut_\d*_\d*_(\w*).wav" input/config input/current_wordlist.txt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('indir', help='The directory of the input sound files.')
    parser.add_argument('outdir', help='The directory to create the prepared files in.')
    parser.add_argument('regex', help='The regex for extracting words from the sound file names.')
    parser.add_argument('config', help='The config file path.')
    parser.add_argument('dict', help='The word->phoneme dictionary file path')
    args = parser.parse_args()
    prepare(args.indir,args.outdir,args.regex,args.config,args.dict)
