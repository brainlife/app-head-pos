import mne
import json
import os
import shutil


def head_pos(raw):
    """Compute time-varying head positions from cHPI and save them in a .pos file.

    Parameters
    ----------
    raw: instance of mne.io.Raw
        Fif file contaning cHPI info 

    Returns
    -------
    head_pos_file: ndarray, shape (n_pos, 10)
        The time-varying head positions.
    """

    chpi_amplitudes = mne.chpi.compute_chpi_amplitudes(raw)
    chpi_locs = mne.chpi.compute_chpi_locs(raw.info, chpi_amplitudes)
    head_pos_file = mne.chpi.compute_head_pos(raw.info, chpi_locs)

    # Save file
    mne.chpi.write_head_pos("out_dir/headshape.pos", head_pos_file)

    return head_pos_file


def main():

    # Generate a json.product to display messages on Brainlife UI
    dict_json_product = {'brainlife': []}

    # Load inputs from config.json
    with open('config.json') as config_json:
        config = json.load(config_json)

    # Read the file and save it in out_dir
    data_file = config.pop('fif')
    raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)  
    raw.save("out_dir/meg.fif", overwrite=True)

    # Read the crosstalk files
    cross_talk_file = config.pop('crosstalk')
    if os.path.exists(cross_talk_file) is True:
        shutil.copy2(cross_talk_file, 'out_dir/crosstalk_meg.fif')  # required to run a pipeline on BL

    # Read the calibration file
    calibration_file = config.pop('calibration')
    if os.path.exists(calibration_file) is True:
        shutil.copy2(calibration_file, 'out_dir/calibration_meg.dat')  # required to run a pipeline on BL

    # Read destination file 
    destination_file = config.pop('destination')
    if os.path.exists(destination_file) is True:
        shutil.copy2(destination_file, 'out_dir/destination.fif')  # required to run a pipeline on BL

    # Read events file 
    events_file = config.pop('events')
    if os.path.exists(events_file) is True:
        shutil.copy2(events_file, 'out_dir/events.tsv')  # required to run a pipeline on BL

    # Apply head pos
    head_pos_file = head_pos(raw)

    # Success message in product.json
    dict_json_product['brainlife'].append({'type': 'success',
                                           'msg': 'Head position file was written successfully.'})

    # Save the dict_json_product in a json file
    with open('product.json', 'w') as outfile:
        json.dump(dict_json_product, outfile)


if __name__ == '__main__':
    main()
