INFILES=../../material/segmentations
WORDS=data/words.txt
DICT=data/current_wordlist.txt
python gram.py gram --folder $INFILES --regex "cut_\d*_\d*_(\w*).wav"
HParse gram wdnet
cat $WORDS | LC_ALL=C sort | uniq > wlist
cat $DICT | LC_ALL=C sort | uniq > ordered_dict
python replace_numbers.py ordered_dict
sed -e 's/\t/\t1\t/' -i ordered_dict
HDMan -m -w wlist -n monophones -i dict ordered_dict
echo 'sil' >> monophones
echo -e 'silence\t[silence]\tsil' >> dict
sort dict -o dict
python mlf.py mlf --folder $INFILES --regex "cut_\d*_\d*_(\w*).wav"
python hcopy.py $INFILES mfc
python proto.py proto
cat hcopy_temp.scp | cut -d " " -f 2 > hcompv_temp.scp
python hcompv.py proto hcompv_temp.scp hmmdef0
python hled.py phones.mlf ordered_dict mlf
python hmmcopy.py
python herest.py phones.mlf hcompv_temp.scp hmm0 hmms monophones
