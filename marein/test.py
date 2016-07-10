import os, re
import argparse, functools, subprocess


call = functools.partial(subprocess.call,shell=True)
popen = functools.partial(subprocess.Popen,shell=True,stdout=subprocess.PIPE)

def hresults(words_mlf,monophones,results_mlf,tempdir):
    words_lab_mlf = os.path.join(tempdir,'words_lab.mlf')
    results_nosilence_mlf = os.path.join(tempdir,'results_nosilence_mlf')
    call("sed -E 's/\..*\"/.lab\"/' "+words_mlf+" > "+words_lab_mlf)
    call("sed '/ silence /d' {} > {}".format(results_mlf,results_nosilence_mlf))
    pipe = popen('HResults -e silence . -I {} {} {}'.format(words_lab_mlf,monophones,results_nosilence_mlf))
    out, _ = pipe.communicate()
    regex = r'WORD.*Acc=(-?[\d\.]*)'
    return float(re.search(regex,str(out)).group(1))

def hvite(indir,wdnet,dic,monophones,scp,results_mlf):
    macros = os.path.join(indir, 'macros')
    hmm = os.path.join(indir, 'hmmdefs')
    call('HVite -H {} -H {} -S {} -i {} -w {} -p 0.0 -s 5.0 {} {}'.format(macros,hmm,scp,results_mlf,wdnet,dic,monophones))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing the recognition performance.')
    parser.add_argument('indir', help='The directory of the hmmdefs and macros files')
    parser.add_argument('wdnet', help='The directory of the hmmdefs and macros files')
    parser.add_argument('dict', help='The directory of the hmmdefs and macros files')
    parser.add_argument('monophones', help='The directory of the hmmdefs and macros files')
    parser.add_argument('scp', help='The directory of the hmmdefs and macros files')
    parser.add_argument('mlf', help='The directory of the hmmdefs and macros files')
    parser.add_argument('-s', help="The steps to execute, a selection from 'vr' for Vite and Results.", nargs='?', default='vr')
    parser.add_argument('--htkdir', help='Output files location.',nargs='?',default='htk')
    parser.add_argument('--tempdir', help='Temporary storage.',nargs='?',default='.temp')
    args = parser.parse_args()
    results_mlf = os.path.join(args.htkdir,'results.mlf')
    if 'v' in args.s:
        hvite(args.indir,args.wdnet,args.dict,args.monophones,args.scp,results_mlf)
    if 'r' in args.s:
        r = hresults(args.mlf,args.monophones,results_mlf,args.tempdir)
        print(r)

    

    
