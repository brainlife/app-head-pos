# app-head-pos

Draft of an App that computes cHPI from info provided in the `raw.fif` when the cHPI were recorded ([see the mne tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/plot_59_head_positions.html#sphx-glr-auto-tutorials-preprocessing-plot-59-head-positions-py)). The output file is a `.pos` file, which will be read by [`mne.chpi.read_head_pos`](https://mne.tools/stable/generated/mne.chpi.read_head_pos.html?highlight=mne%20chpi%20read_head_pos#mne.chpi.read_head_pos) and can be used in Maxwell Filtering (see the corresponding BL App).
