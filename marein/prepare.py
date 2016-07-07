import os, re
import functools
import subprocess
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
	
# hcopy the files from indir to outdir given a config file
def hcopy(indir,outdir,config_file):
    scp_file = 'scp'
    make_scp(indir,outdir,scp_file)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    subprocess.call(['HCopy','-C',config_file,'-S',scp_file])
		
def prepare(in_dir,out_dir,regex,config_file,word_file,dict_file):
	gram_folder('gram',in_dir,regex)
	call('HParse gram wdnet')
	call('cat {} | LC_ALL=C sort | uniq > wlist'.format(word_file))
	call('cat {} | LC_ALL=C sort | uniq > ordered_dict'.format(dict_file))
	replace_numbers('ordered_dict')
	call("sed -e 's/\t/\t1\t/' -i ordered_dict")
	call('HDMan -m -w wlist -n monophones -i dict ordered_dict')
	call("echo 'sil' >> monophones")
	call("echo -e 'silence\t[silence]\tsil' >> dict")
	call("sort dict -o dict")
	mlf_folder('words.mlf',in_dir,regex)
	hcopy(in_dir,out_dir,config_file)
	
prepare('../../material/segmentations','mfc','cut_\d*_\d*_(\w*).wav','input/config','input/words.txt','input/current_wordlist.txt')
	