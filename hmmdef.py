import numpy as np

# classes and functions for dealing with HMM definitions as used in HTK

class HMM:
    def __init__(self, name, kind, states, transitions):
        self.name = name # string
        self.kind = kind # 
        self.states = states # list of State objects
        self.transitions = np.array(transitions) # transition matrix of floats

class State:
    def __init__(self, mean, variance):
        if len(mean) != len(variance):
            raise ValueError('Mean vector length not equal to variance vector length.')
        self.mean = mean # list of floats
        self.variance = variance # list of floats

    def __len__(self):
        return len(self.mean)

# write a number of HMM objects to an output file
def write_hmms(outfile, *hmms):
    with open(outfile,'w') as f:
        wrln = lambda s: f.write(s+'\n')
        for hmm in hmms:
            wrln('<BeginHMM>')
            wrln('\t<VecSize> {}'.format(len(hmm.states[0])))
            wrln('\t<{}>'.format(hmm.kind))
            wrln('\t<NumStates> {}'.format(len(hmm.states)+2))
            for i,state in enumerate(hmm.states):
                wrln('\t\t<State> {}'.format(i+2))
                wrln('\t\t\t<Mean> {}'.format(len(state)))
                wrln('\t\t\t\t{}'.format(' '.join(map(str,state.mean))))
                wrln('\t\t\t<Variance> {}'.format(len(state)))
                wrln('\t\t\t\t{}'.format(' '.join(map(str,state.variance))))
            wrln('\t<TransP> {}'.format(len(hmm.states)+2))
            for row in hmm.transitions:
                wrln('\t\t{}'.format(' '.join(map(str,row))))
            wrln('<EndHMM>')
            wrln('')

# create a standard causal transition matrix, that is, a matrix A where
# A[i,j] = 0 if j < i. length is the number of rows and kernel is a vector K
# for which holds A[i,i+k] = K[k], except that each row in A is normalized.
def standard_causal_transitions(length,kernel):
    # TODO: improve by using actual numpy idioms
    # see http://stackoverflow.com/questions/20360675/roll-rows-of-a-matrix-independently
    m = np.zeros([length,length])
    m[0,1] = 1
    for i in range(1,len(m)):
        m[i,i:min(len(m),i+len(kernel))] = np.array(kernel)[:min(len(m)-i,len(kernel))]
        m[i] = m[i] / m[i].sum()
    return m

