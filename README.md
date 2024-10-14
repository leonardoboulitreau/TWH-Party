# TWH-Party
Contains the scripts and parameters used to generate the TWH-Party from the TWH dataset.

## Setup Environment
Clone the Repository.
```bash
git clone https://github.com/leonardoboulitreau/TWH-Party
cd TWH-Party
```

Enter.
```bash
pip install -r requirements.txt
```

Download the Room Impulse Response and Noise Database from [this link](https://openslr.org/28/) and put it on this repo's root folder.
Generate the Libriparty dataset following the instructions in [this link](https://github.com/speechbrain/speechbrain/tree/develop/recipes/LibriParty/generate_dataset) and put it on this repo's root folder.

## TWH-Party
To generate the TWH party, just download the wav_spk_1 folder available on [this Google Drive](https://drive.google.com/drive/folders/1R-nvdXInAsqvJUuT8EY6fQ0TnbD7jlni?usp=sharing), put it on the project root folder then run:
```bash
python corrupt.py --wavs_folder ./wav_spk_1
```

## Corrupting another Folder of Wavs
If you want, you can add new levels of alter the parameters (which were defined manually) on this dict.

Then, simply run
```bash
python corrupt.py --wavs_folder /path/to/wavs/folder
```
