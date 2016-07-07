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

# write a hcopy config file to filename based on args
def macro(protodir,outdir):
    vfloors = open(os.path.join(protodir,'vFloors'))
    proto = open(os.path.join(protodir,'proto'))
    macros = open(os.path.join(outdir,'macros'), 'w')
    proto_global = proto.read().splitlines()[:3]
    macros.write("\n".join(proto_global))
    macros.write("\n" + vfloors.read())

def hmmdefs(protodir,monophones,outdir):
    monophones = open(os.path.join(protodir,'proto')
    proto = open('monophones')
    hmmdefs = open(os.path.join(outdir,'hmmdefs', 'w')
    
    mono_list = monophones.read().splitlines()
    proto_temp = proto.read().splitlines()[4:]
    
    for phone in mono_list:
        hmmdefs.write("~h \"" + phone + "\"\n")
	hmmdefs.write("\n".join(proto_temp) + "\n")
    
def train(config,scp,outdir,proto,dict,mlf,floor=0.01):
    if not os.exists(outdir):
        os.mkdir(outdir)
    call('cat {} | cut -d " " -f 2 > scp2'.format(scp))
    call('HCompV -C {} -f {} -m -S scp2 -M {} {}'.format(config,floor,outdir,proto))
    hled('phones.mlf',dict,mlf)
    macro(outdir,outdir+2) #???
    
	
train('input/config','scp','htk','input/proto','ordered_dict','mlf')