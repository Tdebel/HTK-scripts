import os, re
import argparse, functools, subprocess

call = functools.partial(subprocess.call,shell=True)

def make_led(fn,s):
    with open(fn,'w') as f:
        f.write('EX\n')
        if not s:
            f.write('IS sil sil\n')
            f.write('DE sp\n')

def hled(outfile,dictfile,wordsfile,s=False):
    ledfile = 'hled_temp.led'
    make_led(ledfile,s)
    subprocess.call(['HLEd', '-l', '*', '-d', dictfile, '-i', outfile, ledfile, wordsfile])
    os.remove(ledfile)

def macro(protodir,outdir):
    vfloors = open(os.path.join(protodir,'vFloors'))
    proto = open(os.path.join(protodir,'proto'))
    macros = open(os.path.join(outdir,'macros'), 'w')
    proto_global = proto.read().splitlines()[:3]
    macros.write("\n".join(proto_global))
    macros.write("\n" + vfloors.read())

def hmmdefs(protodir,monophones,outdir):
    monophones = open(monophones)
    proto = open(os.path.join(protodir,'proto'))
    hmmdefs = open(os.path.join(outdir,'hmmdefs'), 'w')
    
    mono_list = monophones.read().splitlines()
    proto_temp = proto.read().splitlines()[4:]
    
    for phone in mono_list:
        hmmdefs.write('~h "' + phone + '"\n')
        hmmdefs.write('\n'.join(proto_temp) + '\n')

def herest(config,mlf,script,macrodir,hmms,outdir,pruning=[250,150,1000],n=6):
    t = ['{:.1f}'.format(p) for p in pruning]
    cur_dir = macrodir
    macros = ['macros','hmmdefs']
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for i in range(n):
        H = [item for pair in zip(['-H']*len(macros),[os.path.join(cur_dir,macro) for macro in macros]) for item in pair]
        cur_dir = os.path.join(outdir,outdir+str(i))
        if not os.path.exists(cur_dir):
            os.mkdir(cur_dir)
        subprocess.call(['HERest', '-C', config, '-I', mlf, '-t'] + t + ['-S', script] + H + ['-M', cur_dir, hmms])

def train(config,scp,outdir,proto,dict,mlf,monophones,floor=0.01):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    call('cat {} | cut -d " " -f 2 > scp2'.format(scp))
    call('HCompV -C {} -f {} -m -S scp2 -M {} {}'.format(config,floor,outdir,proto))
    hled('phones.mlf',dict,mlf)
    if not os.path.exists(outdir+'2'):
        os.mkdir(outdir+'2')
    macro(outdir,outdir+'2') #???
    hmmdefs(outdir,monophones,outdir+'2')
    herest(config,'phones.mlf','scp2',outdir+'2',monophones,outdir)
	
# python train.py htk scp ordered_dict input/proto words.mlf monophones input/config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('outdir', help='The working directory for this script (will contain hmmdef# folders).')
    parser.add_argument('scp', help='The script file (mfc file list).')
    parser.add_argument('dict', help='The word->phoneme dictionary file path')
    parser.add_argument('proto', help='The input proto file')
    parser.add_argument('mlf', help='The input mlf file.')
    parser.add_argument('monophones', help='The input monophones file.')
    parser.add_argument('config', help='The config file path.')
    args = parser.parse_args()
    train(args.config, args.scp, args.outdir, args.proto, args.dict, args.mlf, args.monophones)
