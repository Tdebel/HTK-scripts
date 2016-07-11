# example of running graph.py

python graph.py ../../material/segmentations/ "cut_\d*_\d*_(\w*).wav" input/config input/current_wordlist.txt input/proto 0.1 3 k_results
# 0.1 = test set ratio
# 3 = amount of k values to use (so with 100 input files and a value of 3 we get k=33, k=67 and k=100)
# k_results = output file name for accuracy values (no actual graph is made)

# previously, before graph.py:

#python prepare.py ../../material/segmentations "cut_\d*_\d*_(\w*).wav" input/config input/current_wordlist.txt
#python train.py htk/scp htk/dict htk/words.mlf htk/monophones input/proto input/config
#python test.py htk/htk5 htk/wdnet htk/dict htk/monophones htk/scp htk/words.mlf
