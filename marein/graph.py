from prepare import prepare
from train import train
from test import test

import os
import random
import argparse

def graph(sourcedir,regex,config,dictionary,proto,testratio,n,maxk,outfile,mfcdir,outdir,tempdir):

    wdnet, htk_dict, monophones, words_mlf, scp = prepare(sourcedir, mfcdir, outdir, regex, config, dictionary, tempdir)

    with open(scp) as f:
        full_set = set(f.readlines())
    
    test_n = round(len(full_set)*testratio)
    test_set = set(random.sample(full_set,int(test_n)))
    train_set = full_set - test_set

    scp_test = os.path.join(tempdir,'scp_test')
    with open(scp_test,'w') as f:
        f.writelines(test_set)

    if maxk == -1:
        maxk = len(train_set)

    def k_result(k):
        train_k = random.sample(train_set,k)
        scp_k = os.path.join(tempdir,'scp_k')
        with open(scp_k,'w') as f:
            f.writelines(train_k)
        final_dir = train(outdir, config, scp_k, proto, htk_dict, words_mlf, monophones, tempdir)
        return test(outdir, final_dir, wdnet, htk_dict, monophones, scp_test, words_mlf, tempdir)
    
    with open(outfile,'w') as f:
        for i in range(n):
            k = int(round(float(i+1)/n*maxk))
            r = k_result(k)
            f.write('{} {}\n'.format(k,r))
            print('i k r =',i,k,r)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('sourcedir')
    parser.add_argument('regex')
    parser.add_argument('config')
    parser.add_argument('dictionary')
    parser.add_argument('proto')
    parser.add_argument('testratio',type=float)
    parser.add_argument('n',type=int)
    parser.add_argument('outfile')
    parser.add_argument('maxk',type=int,nargs='?',default=-1)
    parser.add_argument('mfcdir',nargs='?',default='mfc')
    parser.add_argument('outdir',nargs='?',default='htk')
    parser.add_argument('tempdir',nargs='?',default='.temp')
    args = parser.parse_args()
    graph(args.sourcedir,args.regex,args.config,args.dictionary,args.proto,args.testratio,args.n,args.maxk,args.outfile,args.mfcdir,args.outdir,args.tempdir)

