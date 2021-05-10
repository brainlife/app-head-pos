import mne
import json
import os
import shutil


def head_pos(raw, param_compute_amplitudes_t_step_min, 
             param_compute_amplitudes_t_window, 
             param_compute_amplitudes_ext_order, 
             param_compute_amplitudes_tmin, 
             param_compute_amplitudes_tmax, param_compute_locs_t_step_max,  
             param_compute_locs_too_close, param_compute_locs_adjust_dig, 
             param_compute_head_pos_dist_limit,
             param_compute_head_pos_gof_limit, param_compute_head_pos_adjust_dig):
    """Compute time-varying head positions from cHPI and save them in a .pos file.

    Parameters
    ----------
    raw: instance of mne.io.Raw
        MEG fif file contaning cHPI info. 
    param_compute_amplitudes_t_step_min: float
        Minimum time step to use to compute cHPI amplitudes. If correlations are sufficiently high, t_step_max 
        will be used. Default is 0.01.
    param_compute_amplitudes_t_window: float
        Time window to use to estimate the amplitudes. Default is 0.2 (200 ms).
    param_compute_amplitudes_ext_order: int
        The external order for SSS-like interfence suppression to compute cHPI amplitudes. Default is 1.
    param_compute_amplitudes_tmin: float 
        Start time of the raw data to use in seconds to compute cHPI amplitudes. Default is 0.
    param_compute_amplitudes_tmax: float or None
        End time of the raw data to use in seconds to compute cHPI amplitudes. Default is None.
    param_compute_locs_t_step_max: float
        Maximum step to use to compute HPI coils locations. Default is 1.
    param_compute_locs_too_close: str
        How to handle HPI positions too close to sensors when computing HPI coils locations. 
        Can be 'raise', (default), 'warning', or 'info'.
    param_compute_locs_adjust_dig: bool
        If True, adjust the digitization locations used for fitting when computing HPI coils locations.
        Default is False.
    param_compute_head_pos_dist_limit: float
        Minimum distance (m) to accept for coil position fitting when computing head positions. Default is 0.005.
    param_compute_head_pos_gof_limit: float
        Minimum goodness of fit to accept for each coil to compute head positions. Default is 0.98.
    param_compute_head_pos_adjust_dig: bool
        If True, adjust the digitization locations used for fitting when computing head positions. Default is False.

    Returns
    -------
    head_pos_file: ndarray, shape (n_pos, 10)
        The time-varying head positions.
    """

    # Extract HPI coils amplitudes as a function of time
    chpi_amplitudes = mne.chpi.compute_chpi_amplitudes(raw, t_step_min=param_compute_amplitudes_t_step_min, 
                                                       t_window=param_compute_amplitudes_t_window, 
                                                       ext_order=param_compute_amplitudes_ext_order, 
                                                       tmin=param_compute_amplitudes_tmin, 
                                                       tmax=param_compute_amplitudes_tmax)
    
    # Compute time-varying HPI coils locations  
    chpi_locs = mne.chpi.compute_chpi_locs(raw.info, chpi_amplitudes, t_step_max=param_compute_locs_t_step_max,  
                                           too_close=param_compute_locs_too_close, adjust_dig=param_compute_locs_adjust_dig)

    # Compute head positions from the coil locations
    head_pos_file = mne.chpi.compute_head_pos(raw.info, chpi_locs, dist_limit=param_compute_head_pos_dist_limit,
                                              gof_limit=param_compute_head_pos_gof_limit, adjust_dig=param_compute_head_pos_adjust_dig)

    # Save file
    mne.chpi.write_head_pos("out_dir/headshape.pos", head_pos_file)

    return head_pos_file


def main():

    # Generate a json.product to display messages on Brainlife UI
    dict_json_product = {'brainlife': []}

    # Load inputs from config.json
    with open('config.json') as config_json:
        config = json.load(config_json)

    # Read the meg file and save it in out_dir
    data_file = config.pop('fif')
    raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)  
    raw.save("out_dir/meg.fif", overwrite=True)

    
    ## Read the optional files ##
    
    # Read the crosstalk file
    cross_talk_file = config.pop('crosstalk')
    if cross_talk_file is not None:
        if os.path.exists(cross_talk_file) is True:
            shutil.copy2(cross_talk_file, 'out_dir/crosstalk_meg.fif')  # required to run a pipeline on BL

    # Read the calibration file
    calibration_file = config.pop('calibration')
    if calibration_file is not None:
        if os.path.exists(calibration_file) is True:
            shutil.copy2(calibration_file, 'out_dir/calibration_meg.dat')  # required to run a pipeline on BL

    # Read destination file 
    destination_file = config.pop('destination')
    if destination_file is not None:
        if os.path.exists(destination_file) is True:
            shutil.copy2(destination_file, 'out_dir/destination.fif')  # required to run a pipeline on BL

    # Read events file 
    events_file = config.pop('events')
    if events_file is not None
        if os.path.exists(events_file) is True:
            shutil.copy2(events_file, 'out_dir/events.tsv')  # required to run a pipeline on BL

    # Read channels file 
    channels_file = config.pop('channels')
    if channels_file is not None
        if os.path.exists(channels_file) is True:
            shutil.copy2(channels_file, 'out_dir/channels.tsv')  # required to run a pipeline on BL

    # Check if param_st_duration is not None
    if config['param_compute_amplitudes_tmax'] == "":
        config['param_compute_amplitudes_tmax'] = None  # when App is run on Bl, no value for this parameter corresponds to ''

    
    ## Define kwargs ##

    # Delete headshape key from config file
    del config['headshape']

    # Delete keys values in config.json when this app is executed on Brainlife
    if '_app' and '_tid' and '_inputs' and '_outputs' in config.keys():
        del config['_app'], config['_tid'], config['_inputs'], config['_outputs'] 
    kwargs = config  

    
    # Apply head pos
    head_pos_file = head_pos(raw, **kwargs)

    # Success message in product.json
    dict_json_product['brainlife'].append({'type': 'success',
                                           'msg': 'Head position file was written successfully.'})

    # Save the dict_json_product in a json file
    with open('product.json', 'w') as outfile:
        json.dump(dict_json_product, outfile)


if __name__ == '__main__':
    main()
