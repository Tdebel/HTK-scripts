import argparse
import subprocess
import os 

def hresults(args):
    mlf = os.path.join(args.indir_files, 'testset.mlf')
    mono = os.path.join(args.indir_files, 'monophones')
    subprocess.call(['HResults -I', mlf, mono, 'results.mlf'])

def hvite(args):
    macros = os.path.join(args.indir_hmm, 'macros')
    hmm = os.path.join(args.indir_hmm, 'hmmdefs')
    wdnet = os.path.join(args.indir_files, 'wdnet')
    dic = os.path.join(args.indir_files, 'dict')
    mono = os.path.join(args.indir_files, 'monophones')
    scp = os.path.join(args.indir_files, 'hcompv_temp.scp')
    subprocess.call(['HVite -A -D -T 1 -H', macros, '-H', hmmdefs, '-S', scp, '-i results.mlf', '-w', wdnet, '-p 0.0 -s 5.0', dic, mono])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing the recognition performance.')
    parser.add_argument('indir_hmm', help='The directory of the hmmdefs and macros files')
    parser.add_argument('indir_files', help='The path to the scp, dict and wordnet, monophones, mlf')
    parser.add_argument('config', help='config for the hmms (built during HERest)', nargs='+')
    args = parser.parse_args()
    hvite(args)
    hresults(args)    
    

    
