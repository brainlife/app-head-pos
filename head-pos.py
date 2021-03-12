import mne
import json


def head_pos(raw):
    """Compute time-varying head positions from cHPI and save them in a .pos file.

    Parameters
    ----------
    raw: instance of mne.io.Raw
        Fif file contaning cHPI info 

    Returns
    -------
    head_pos: ndarray, shape (n_pos, 10)
        The time-varying head positions.
    """

    chpi_amplitudes = mne.chpi.compute_chpi_amplitudes(raw)
    chpi_locs = mne.chpi.compute_chpi_locs(raw.info, chpi_amplitudes)
    head_pos = mne.chpi.compute_head_pos(raw.info, chpi_locs)

    # Save file
    mne.chpi.write_head_pos("out_dir/head_pos.pos", head_pos)

    return head_pos


def main():

    # Generate a json.product to display messages on Brainlife UI
    dict_json_product = {'brainlife': []}

    # Load inputs from config.json
    with open('config.json') as config_json:
        config = json.load(config_json)

    # Get cHPI
    data_file = config.pop('fif')
    raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)  

    # Apply head pos
    head_pos(raw)

    # Success message in product.json
    dict_json_product['brainlife'].append({'type': 'success',
                                           'msg': 'head position file was written successfully.'})

    # Save the dict_json_product in a json file
    with open('product.json', 'w') as outfile:
        json.dump(dict_json_product, outfile)


if __name__ == '__main__':
    main()
