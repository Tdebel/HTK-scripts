import hmmdef
import argparse
import numpy as np

# Create a protofile file given:
# outfile - the file to write to
# name - name of the hmm
# kind - the parameter kind (such as MFCC_0_D_N_Z)
# size - the total vector size of the output of each state
# statecount - the number of emitting states
# transkernel - the kernel that is used for constructing the standard causal transition matrix
def proto(outfile, name, kind, size, statecount, transkernel):
    states = [hmmdef.State([0.0]*size,[0.0]*size) for s in range(statecount)]
    transitions = hmmdef.standard_causal_transitions(statecount+2,transkernel)
    hmm = hmmdef.HMM(name, kind, states, transitions)

    hmmdef.write_hmms(outfile, hmm)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a HTK prototype file based on parameters.')
    parser.add_argument('outfile', type=str)
    parser.add_argument('-n', '--name', nargs='?', default='proto', type=str)
    parser.add_argument('-k', '--targetkind', nargs='?', default='MFCC_0_D_N_Z', type=str)
    parser.add_argument('-v', '--vecsize', nargs='?', default=25, type=int)
    parser.add_argument('-s', '--states', nargs='?', default=3, type=int)
    parser.add_argument('-t', '--transkernel', nargs='*', default=[0.6,0.4], type=float)
    args = parser.parse_args()
    proto(args.outfile, args.name, args.targetkind, args.vecsize, args.states, args.transkernel)
