import mne
import json


# Test version
print(mne.__version__)

# Load inputs from config.json
with open('config.json') as config_json:
    config = json.load(config_json)

# Get cHPI
data_file = str(config.pop('input_raw'))
raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)  # raw file must contain cHPI info
chpi_amplitudes = mne.chpi.compute_chpi_amplitudes(raw, **config['params_chpi_amplitudes'])
chpi_locs = mne.chpi.compute_chpi_locs(raw.info, chpi_amplitudes, **config['params_chpi_locs'])
head_pos = mne.chpi.compute_head_pos(raw.info, chpi_locs, **config['params_head_pos'])

# Save file
mne.chpi.write_head_pos(config['output'], head_pos)
