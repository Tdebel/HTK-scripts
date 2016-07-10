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
def hcopy(sourcedir,mfcdir,filedir,config,tempdir):
    scp = os.path.join(tempdir,'scp')
    make_scp(sourcedir,mfcdir,scp)
    if not os.path.exists(mfcdir):
        os.mkdir(mfcdir)
    config_prepare = os.path.join(tempdir, 'prepare.config')
    add_sourceformat_to_config(sourcedir,config,config_prepare)
    call('HCopy -C {} -S {}'.format(config_prepare,scp))
    return scp

def prepare(sourcedir,mfcdir,filedir,regex,config,dictionary,tempdir):
    
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)
    if not os.path.exists(filedir):
        os.mkdir(filedir)

    gram = os.path.join(tempdir,'gram')
    wdnet = os.path.join(filedir,'wdnet')
    wlist = os.path.join(tempdir,'wlist')
    temp_dict = os.path.join(tempdir,'dict')
    htk_dict = os.path.join(filedir,'dict')
    monophones = os.path.join(filedir,'monophones')
    words_mlf = os.path.join(filedir,'words.mlf')
    scp = os.path.join(filedir,'scp')

    gram_folder(gram,sourcedir,regex)
    call('HParse {} {}'.format(gram,wdnet))
    call("cut -d'\t' -f1 {} | LC_ALL=C sort | uniq > {}".format(dictionary,wlist))
    call('cat {} | LC_ALL=C sort | uniq > {}'.format(dictionary,temp_dict))
    replace_numbers(temp_dict)
    call("sed -e 's/\t/\t1\t/' -i {}".format(temp_dict))
    call('HDMan -m -w {} -n {} -i {} {}'.format(wlist,monophones,htk_dict,temp_dict))
    call("echo 'sil' >> {}".format(monophones))
    call("echo -e 'silence\t[silence]\tsil' >> {}".format(htk_dict))
    call("sort {0} -o {0}".format(htk_dict))
    mlf_folder(words_mlf,sourcedir,regex)
    temp_scp = hcopy(sourcedir,mfcdir,filedir,config,tempdir)
    call('cat {} | cut -d " " -f 2 > {}'.format(temp_scp,scp))

    return wdnet, htk_dict, monophones, words_mlf, scp
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('sourcedir', help='The directory of the input sound files.')
    parser.add_argument('regex', help='The regex for extracting words from the sound file names.')
    parser.add_argument('config', help='The config file path.')
    parser.add_argument('dictionary', help='The word->phoneme dictionary file path')
    parser.add_argument('--tempdir', help='The directory to use for temporary files used in this script', nargs='?', default='.temp')
    parser.add_argument('--mfcdir', help='The directory to create the prepared mfc files in.',nargs='?',default='mfc')
    parser.add_argument('--filedir', help='The directory to store other output files in.',nargs='?',default='htk')
    args = parser.parse_args()
    outfiles = prepare(args.sourcedir,args.mfcdir,args.filedir,args.regex,args.config,args.dictionary,args.tempdir)
    print(' '.join(outfiles))
