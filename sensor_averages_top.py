# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# add plot inline in the page
# %matplotlib inline

import mne
import MNEpythonQC

mne.set_log_level('INFO')



data_path = '/Volumes/TimeMachineBackups/MEG_Data/bad_baby/bad_134b/'
raw_fname = 'bad_134b_mmn_raw_tsss_mc.fif'
title = 'bad_134b_mmn_raw_tsss_mc'
trigger = 1
evoked = MNEpythonQC.sensor_averages(data_path, raw_fname, title, trigger)
print("Averaging done.")
