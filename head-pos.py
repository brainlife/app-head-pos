import mne
import json

# Generate a json.product to display messages on Brainlife UI
dict_json_product = {'brainlife': []}

# Load inputs from config.json
with open('config.json') as config_json:
    config = json.load(config_json)

# Get cHPI
data_file = str(config.pop('fif'))
raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)  # raw file must contain cHPI info
chpi_amplitudes = mne.chpi.compute_chpi_amplitudes(raw)
chpi_locs = mne.chpi.compute_chpi_locs(raw.info, chpi_amplitudes)
head_pos = mne.chpi.compute_head_pos(raw.info, chpi_locs)

# Save file
mne.chpi.write_head_pos("out_dir/head_pos.pos", head_pos)

# Success message in product.json
dict_json_product['brainlife'].append({'type': 'success',
                                       'msg': 'head position file was written successfully.'})

# Save the dict_json_product in a json file
with open('product.json', 'w') as outfile:
    json.dump(dict_json_product, outfile)
