# TWH-Party
Contains the scripts and parameters used to generate the TWH-Party.

## Setup Environment
Clone the Repository.
'''bash
git clone https://github.com/leonardoboulitreau/TWH-Party
cd TWH-Party
'''

Enter.
'''bash
pip install -r requirements.txt
'''

## TWH-Party
To generate the TWH party, just download the wav_spk_1 folder available on [this Google Drive](https://drive.google.com/drive/folders/1R-nvdXInAsqvJUuT8EY6fQ0TnbD7jlni?usp=sharing), put it on the project root folder then run:
'''bash
python corrupt.py --wavs_folder ./wav_spk_1
'''

## Corrupting another Folder of Wavs
If you want, you can add new levels of alter the parameters (which were defined manually) on this dict.

Then, simply run
'''bash
python corrupt.py --wavs_folder /path/to/wavs/folder
'''
