import os, re
import argparse, functools, subprocess


call = functools.partial(subprocess.call,shell=True)

def hresults(phones,monophones):
    call('HResults -I {} {} results.mlf'.format(phones,monophones))

def hvite(indir,wdnet,dic,monophones,scp):
    macros = os.path.join(indir, 'macros')
    hmm = os.path.join(indir, 'hmmdefs')
    call('HVite -H {} -H {} -S {} -i results.mlf -w {} -p 0.0 -s 5.0 {} {}'.format(macros,hmm,scp,wdnet,dic,monophones))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing the recognition performance.')
    parser.add_argument('indir', help='The directory of the hmmdefs and macros files')
    parser.add_argument('wdnet', help='The directory of the hmmdefs and macros files')
    parser.add_argument('dict', help='The directory of the hmmdefs and macros files')
    parser.add_argument('monophones', help='The directory of the hmmdefs and macros files')
    parser.add_argument('scp', help='The directory of the hmmdefs and macros files')
    parser.add_argument('phones', help='The directory of the hmmdefs and macros files')
    args = parser.parse_args()
    hvite(args.indir,args.wdnet,args.dict,args.monophones,args.scp)
    hresults(args.phones,args.monophones)
    

    
