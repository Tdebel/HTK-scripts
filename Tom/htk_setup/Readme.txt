#################################################
###		Tom Janssen Groesbeek	      ###
###			06/07/2016	      ###
#################################################

Uitleg script files:

Deze map mist nu nog 4 belangrijke folders, namelijk: 
  - segmentations (bevat ALLE .wav files), 
  - testing (een lege folder waar uiteindelijk de test .wav files in zullen komen
  - training (een lege folder waar uiteindelijk ALLE training .wav files in zullen komen
    - een "k" folder in de training folder (waar een % aan training .wav files in terecht zullen komen)

Belangrijk: in het bestand "data_prep.py" moet je zelf nog aangeven hoe groot je de test en training sizes wilt.
Onder "def execute(self)" in "data_prep.py" staat voor de eerste run "s = Sorter() s.execute(0.90,0.10)".
Dit geeft aan dat de training size 90% van alle segmentations zal zijn en dat vervolgens hiervan 10% daadwerkelijk gebruikt wordt om te trainen.
Voor opvolgende runs is het van belang dat deze 2 lijnen code weg gehaald worden en vervolgens de volgende 2 lijnen code gebruikt worden.
Namelijk "s = Sorterk() s.execute(k)". Want na de eerste run zijn de training en test files al verdeeld en ben je alleen
geinteresseerd in het vergroten van je k-folder. Dit deel van de code zorgt er voor dat je uit je training folder een bepaald percentage "k" in de k-folder zet.

Nu de volgorde van gebruik:
 1) Als je dus hebt bepaald hoe de verdeling eruit ziet run je eerst "data_prep.py"
  - python data_prep.py
 2) Daarna run je "monophone_creator.py"

Als het goed is worden hierdoor de verschillende hmm0-7 folders aangemaakt en zal je uiteindelijk ook de results te zien krijgen.
