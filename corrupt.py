from speechbrain.processing.signal_processing import rescale, reverberate
from speechbrain.utils.data_utils import get_all_files
import torchaudio
from pathlib import Path
import librosa
import os
import numpy as np
import torch
import soundfile as sf
import random
from tqdm import tqdm
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--wavs_folder', type=str)
    args = parser.parse_args()

    WAVS_FOLDER = args.wavs_folder
    LIBRIPARTY_PATH = './LibriParty/'
    RIRS_NOISE_PATH = './rirs_noises/'
    out_path = './TWH_PARTY/'

    levels = {'low':{'n_party':6, 'X':0.75, 'y':0.10, 'dry':0.55, 'speech_lvl':-3}, 
            'med':{'n_party':8, 'X':0.70, 'y':0.12, 'dry':0.45, 'speech_lvl':-4}, 
            'high':{'n_party':10, 'X':0.65, 'y':0.15, 'dry':0.35, 'speech_lvl':-5}}


    rirs_folders = [os.path.join(RIRS_NOISE_PATH,'simulated_rirs/'), os.path.join(RIRS_NOISE_PATH,'real_rirs_isotropic_noises/')]
    noises_folders = [os.path.join(RIRS_NOISE_PATH,'pointsource_noises/')]

    noises = []
    rirs = []
    for f in noises_folders:
        noises.extend(get_all_files(f, match_and=[".wav"]))
    for f in rirs_folders:
        rirs.extend(get_all_files(f, match_and=[".wav"]))

    twh = get_all_files(WAVS_FOLDER, match_and=['.wav'])
    libriparty = get_all_files(LIBRIPARTY_PATH, match_and=['.wav'])

    np.random.seed(1917)
    info = {}
    for lvl in levels.keys():
        if not os.path.exists(os.path.join(out_path, lvl)):
            os.makedirs(os.path.join(out_path, lvl), exist_ok=True)

        # Get parameters for each level
        params = levels[lvl]
        n_party = params['n_party']
        speech_lvl = params['speech_lvl']
        X = params['X']
        y = params['y']
        dry = params['dry']
        info[lvl] = {}
        info[lvl]['parameters'] = params

        for idx in tqdm(range(len(twh))):
            # Select Audio
            audio_path = twh[idx]

            # Create Dict for each audio
            info[lvl][audio_path] = {}

            # Define and Create Out Path
            output_path = os.path.join(out_path, str(lvl), os.path.basename(audio_path))
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Load Audio
            sig, sr = torchaudio.load(audio_path)
                
            # Remove if stereo
            if sig.shape[0] > 1:
                sig = sig[0, :].unsqueeze(0)

            # Resample if not in 16kHz
            if sr != 16000:
                    resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
                    sig = resampler(sig)
                    sr = 16000

            # Normalize and rescale
            sig = sig - torch.mean(sig)
            sig = rescale(sig, sig.size(0), speech_lvl, scale="dB", amp_type="peak") 

            # Apply Rever
            rir_path = np.random.choice(rirs, 1)[0]
            info[lvl][audio_path]['reverb_path'] = rir_path
            rir, fs = torchaudio.load(rir_path)
            if rir.shape[0] > 1:
                rir = rir[0, :].unsqueeze(0)
            if fs != 16000:
                    resampler = torchaudio.transforms.Resample(orig_freq=fs, new_freq=16000)
                    rir = resampler(rir)
                    fs = 16000
            waveform_rev = reverberate(sig, rir, "peak")                                           # HOW DOES REVERB CHANGE DB??
            sig = dry*sig + (1-dry)*waveform_rev

            noises_empty = torch.zeros_like(sig)
            noises = np.random.choice(libriparty, n_party)
            info[lvl][audio_path]['noises_libri'] = noises
            for noise in noises:
                noi, sr = torchaudio.load(noise)
                if noi.shape[0] > 1:
                    noi = noi[0, :].unsqueeze(0)
                if sr != 16000:
                        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
                        noi = resampler(noi)
                        sr = 16000
                noises_empty[0,:]+=noi[0, 0:len(sig[0,:])]
            sig = X * sig[0,:] + y * noises_empty[0,:]
            sf.write(output_path, sig, sr)

    np.save(os.path.join(out_path,"info.npy"), info)

if __name__ == '__main__':
    main()
