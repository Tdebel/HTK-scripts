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
    return cur_dir

def train(outdir,config,scp,proto,dict,words_mlf,monophones,tempdir,floor=0.01):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists(tempdir):
        os.mkdir(tempdirdir)

    phones_mlf = os.path.join(tempdir,'phones.mlf')

    call('HCompV -C {} -f {} -m -S {} -M {} {}'.format(config,floor,scp,outdir,proto))
    hled(phones_mlf,dict,words_mlf)
    macro(outdir,outdir)
    hmmdefs(outdir,monophones,outdir)
    final_dir = herest(config,phones_mlf,scp,outdir,monophones,outdir)

    return final_dir
	
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('scp', help='The script file (mfc file list).')
    parser.add_argument('dict', help='The word->phoneme dictionary file path')
    parser.add_argument('mlf', help='The input (words) mlf file.')
    parser.add_argument('monophones', help='The input monophones file.')
    parser.add_argument('proto', help='The input proto file')
    parser.add_argument('config', help='The config file path.')
    parser.add_argument('--filedir', help='The working directory for this script (will contain hmm folders).',nargs='?',default='htk')
    parser.add_argument('--tempdir', help='Temporary file storage for this script..',nargs='?',default='.temp')
    args = parser.parse_args()
    output = train(args.filedir, args.config, args.scp, args.proto, args.dict, args.mlf, args.monophones, args.tempdir)
    print(' '.join(output))

