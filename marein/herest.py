import os, re
import argparse
import subprocess

def herest(mlf,script,macrodir,hmms,outdir,pruning,n):
    config = 'hcompv_temp.config'
    t = ['{:.1f}'.format(p) for p in pruning]
    cur_dir = macrodir
    macros = ['macros','hmmdefs']
    os.mkdir(outdir)
    for i in range(n):
        H = [item for pair in zip(['-H']*len(macros),[os.path.join(cur_dir,macro) for macro in macros]) for item in pair]
        cur_dir = os.path.join(outdir,outdir+str(i))
        os.mkdir(cur_dir)
        subprocess.call(['HERest', '-C', config, '-I', mlf, '-t'] + t + ['-S', script] + H + ['-M', cur_dir, hmms])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the required mlf edits.')
    parser.add_argument('mlf', type=str)
    parser.add_argument('script', type=str)
    parser.add_argument('macrodir', type=str) # dir with macros, hmmdefs (hmm0)
    parser.add_argument('outdir', type=str) # dir that will contain hmm0, hmm1 etc
    parser.add_argument('hmms', type=str) # monophones0
    parser.add_argument('-n', required=False, default=6)
    parser.add_argument('--pruning', nargs=3, default=[250,150,1000], type=float)
    args = parser.parse_args()
    herest(args.mlf,args.script,args.macrodir,args.hmms,args.outdir,args.pruning,args.n)
