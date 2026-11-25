<h1 align="center">Compute head positions from cHPI</h1>

<p align="center">
  A time-varying head position file (<code>headshape.pos</code>) from MEG data recorded with continuous head position indicator (cHPI) coils.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.499"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.499-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

This App computes time-varying head positions from the cHPI signals stored in a MEG `.fif` recording, following the [MNE-Python head position tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/plot_59_head_positions.html). It uses `mne.chpi` to estimate the cHPI amplitudes, the coil locations and finally the head positions. The resulting `.pos` file is used for movement compensation in the bad-channel detection and Maxwell filtering Apps.

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Computes time-varying head positions from continuous HPI (cHPI) signals in MEG .fif data with MNE-Python and outputs a headshape.pos file for Maxwell filtering.**

Uses mne.chpi to compute cHPI amplitudes, coil locations and head positions from the raw .fif and writes them with mne.chpi.write_head_pos. Use it before Maxwell filtering (movement compensation) of MEG recordings made with cHPI. The input must contain cHPI recordings; optional calibration, crosstalk and destination files are passed through.

| | |
|---|---|
| **Inputs** | `neuro/meg/fif` · `neuro/meg/fif-override` (optional) |
| **Outputs** | `neuro/meg/fif-override` |
| **Container** | `brainlife/mne:0.23dev` |
| **Resources** | 1 CPUs |
| **Run it** | [doi.org/10.25663/brainlife.app.499](https://doi.org/10.25663/brainlife.app.499) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meg/fif` | yes | MEG data in .fif format containing cHPI data. |
| `Opt` | `neuro/meg/fif-override` | no | Optional destination file computed by app-mean-transformation-matrix. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meg/fif-override` | .pos file containing the time-varying head positions. This file will be used during detection of bad channels in MEG data (app-bad-channels) and Maxwell filtering (app-maxwell-filter) steps. |

<details>
<summary><b>Parameters</b> (11)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `param_compute_amplitudes_t_step_min` | number | `0.01` | Minimum time step to use to compute cHPI amplitudes. If correlations are sufficiently high, t_step_max. This value can be a float. |
| `param_compute_amplitudes_t_window` | number | `0.2` | Time window to use to estimate the amplitudes. This value can be a float. |
| `param_compute_amplitudes_ext_order` | number | `1` | The external order for SSS-like interfence suppression to compute cHPI amplitudes. This value must be an integer. |
| `param_compute_amplitudes_tmin` | number | `0` | Start time of the raw data to use in seconds to compute cHPI amplitudes. This value can be a float. |
| `param_compute_amplitudes_tmax` | number |  | End time of the raw data to use in seconds to compute cHPI amplitudes. This value can be a float. |
| `param_compute_locs_t_step_max` | number | `1` | Maximum step to use to compute HPI coils locations. This value can be a float. |
| `param_compute_locs_too_close` | enum | `raise` | How to handle HPI positions too close to sensors when computing HPI coils locations. Options: `raise`, `warning`, `info`. |
| `param_compute_locs_adjust_dig` | boolean | `false` | If True, adjust the digitization locations used for fitting when computing HPI coils locations. |
| `param_compute_head_pos_dist_limit` | number | `0.005` | Minimum distance (m) to accept for coil position fitting when computing head positions. This value can be a float. |
| `param_compute_head_pos_gof_limit` | number | `0.98` | Minimum goodness of fit to accept for each coil to compute head positions. This value can be a float. |
| `param_compute_head_pos_adjust_dig` | boolean | `false` | If True, adjust the digitization locations used for fitting when computing head positions. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.499](https://doi.org/10.25663/brainlife.app.499), choose a MEG dataset (`neuro/meg/fif`) that contains cHPI recordings and, optionally, a `neuro/meg/fif-override` dataset with a destination file (for example from the [mean head position App](https://github.com/brainlife/app-mean-transformation-matrix)), then press **Execute**. The App archives a `neuro/meg/fif-override` dataset with the head positions.

All parameters are advanced and map onto the MNE-Python functions:

| Parameter | Default | MNE-Python argument |
|---|---|---|
| `param_compute_amplitudes_t_step_min` | 0.01 | `compute_chpi_amplitudes(t_step_min)`: minimum time step for the cHPI amplitudes |
| `param_compute_amplitudes_t_window` | 0.2 | `compute_chpi_amplitudes(t_window)`: time window used to estimate the amplitudes |
| `param_compute_amplitudes_ext_order` | 1 | `compute_chpi_amplitudes(ext_order)`: external order for SSS-like interference suppression |
| `param_compute_amplitudes_tmin` | 0 | `compute_chpi_amplitudes(tmin)`: start time in seconds |
| `param_compute_amplitudes_tmax` | none | `compute_chpi_amplitudes(tmax)`: end time in seconds |
| `param_compute_locs_t_step_max` | 1 | `compute_chpi_locs(t_step_max)`: maximum time step for the coil locations |
| `param_compute_locs_too_close` | `raise` | `compute_chpi_locs(too_close)`: `raise`, `warning` or `info` when coils are too close to the sensors |
| `param_compute_locs_adjust_dig` | false | `compute_chpi_locs(adjust_dig)` |
| `param_compute_head_pos_dist_limit` | 0.005 | `compute_head_pos(dist_limit)`: minimum distance (m) accepted for coil fitting |
| `param_compute_head_pos_gof_limit` | 0.98 | `compute_head_pos(gof_limit)`: minimum goodness of fit for each coil |
| `param_compute_head_pos_adjust_dig` | false | `compute_head_pos(adjust_dig)` |

### Locally

You need [Singularity/Apptainer](https://apptainer.org/). `main` runs `head_pos.py` in the `brainlife/mne:0.23dev` container.

1. Clone this repository with its helper submodule:

   ```bash
   git clone --recursive https://github.com/brainlife/app-head-pos.git
   ```

2. Create `config.json` with the same keys as `config.json.example`, with the paths to your files and the parameter values you want. Only `fif` is required; optional files (`calibration`, `crosstalk`, `destination`, `events`, `channels`, `headshape`) can be `null` or left out:

   ```json
   {
       "fif": "input/rest1-raw.fif",
       "param_compute_amplitudes_t_step_min": 0.01,
       "param_compute_amplitudes_t_window": 0.2,
       "param_compute_amplitudes_ext_order": 1,
       "param_compute_amplitudes_tmin": 0,
       "param_compute_amplitudes_tmax": null,
       "param_compute_locs_t_step_max": 1,
       "param_compute_locs_too_close": "raise",
       "param_compute_locs_adjust_dig": false,
       "param_compute_head_pos_dist_limit": 0.005,
       "param_compute_head_pos_gof_limit": 0.98,
       "param_compute_head_pos_adjust_dig": false
   }
   ```

3. Run the App:

   ```bash
   ./main
   ```

## Outputs

```text
out_dir/
└── headshape.pos    time-varying head positions
product.json         status message shown on brainlife.io
```

The `.pos` file can be read with [`mne.chpi.read_head_pos`](https://mne.tools/stable/generated/mne.chpi.read_head_pos.html). Optional input files given in `config.json` are passed through to `out_dir/`.

## Troubleshooting

- **Error about HPI coils too close to the sensors**: by default `param_compute_locs_too_close` is `raise`; set it to `warning` or `info` to continue.
- **No head positions**: the input must contain cHPI recordings; the App cannot compute positions from data recorded without continuous HPI.

## Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Compute headshape.pos file from cHPI recorded during MEG acquisition. brainlife.io App. [doi:10.25663/brainlife.app.499](https://doi.org/10.25663/brainlife.app.499)
- Gramfort et al. MEG and EEG data analysis with MNE-Python. *Frontiers in Neuroscience* 7 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Aurore Bussalb

**Contributors:** Maximilien Chaumon

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## License

[MIT](LICENSE). MNE-Python is distributed under its own BSD license.
