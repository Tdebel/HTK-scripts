# example of running prepare, train and test in sequence


python prepare.py ../../material/segmentations "cut_\d*_\d*_(\w*).wav" input/config input/current_wordlist.txt
python train.py htk/scp htk/dict htk/words.mlf htk/monophones input/proto input/config
python test.py htk/htk5 htk/wdnet htk/dict htk/monophones htk/scp htk/words.mlf
