# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:20:27 2015

@author: mreilly2
"""
import mne
import numpy as np
from mne.viz import plot_evoked_topo
import matplotlib.pyplot as plt
from mne.report import Report
from mnefun import extract_expyfun_events
import os
from os import path as op

def test_function(test):
    print test
    return;


def sensor_averages(data_path, data_file, title, trigger):

    plt.close("all")
    
    d_path = data_path
    d_file = data_file 
    trig = trigger
    title = title
    print('------------ Start raw import ------------------')
    
    print d_path
    print d_file
    raw_fname = d_path + d_file
    print raw_fname
   
    raw = mne.io.Raw(raw_fname, allow_maxshield=True, preload=True)
    raw.plot(title='Raw Data')
    print('Compute ECG projections')    
    projs, _ = mne.preprocessing.compute_proj_ecg(raw, ch_name = 'MEG0113', tmin=-0.8, tmax = 0.240, n_grad=4, n_mag=4, n_jobs=1, reject=None)
    raw.add_proj(projs, remove_existing=True, )
    raw.plot(title='ECG Projection Chan MEG0113')

    
  
    plt.title(data_file + '_TRIGGER_' + str(trig))
    plt.xlabel('time (s)')
    plt.ylabel('MEG data (T)')
    
    print('------------ End raw plot ------------------')
    
    len(mne.pick_types(raw.info, meg=True, eeg=False, exclude='bads'))
    raw.info['bads']
    
    
    print('------------ Start raw filter ------------------')

    raw.filter(2, 40.0, method='fft')
    
    
    
    print('------------ End raw filter ------------------')
    
    # Define and read epochs
    # First extract events:
    
    print('------------ Start find events ------------------')
    events = mne.find_events(raw, stim_channel='STI101', consecutive = True, min_duration = 0.002)
    fig = mne.viz.plot_events(events, raw.info['sfreq'], raw.first_samp)
    
    
    print('------------ End find events ------------------')
    
    
    
    # Define epochs parameters:
    print('------------ Start find epochs ------------------')
    # ------------------------- SET TRIGGER CHANNEL ------------------
    ####################################################################
    event_id = dict(stim=trig)  # event trigger and conditions
    ###################################################################
    tmin = -0.05  # start of each epoch (ms before the trigger)
    tmax = 0.6  # end of each epoch (ms after the trigger)
    
    # event_id for phantom
    #event_id = 7936
    
    print raw.info['bads']
    
    # The variable raw.info[‘bads’] is just a python list.
    # Pick the good channels:
    
    # Pick the good channels:
    
    picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=False,
                           stim=False, exclude='bads')
      
    # Define the baseline period:
    
    baseline = (None, 0)  # means from the first instant to t = 0
    
    # Define peak-to-peak rejection parameters for gradiometers, magnetometers and EOG:
    
    reject = dict(grad=4000e-13, mag=4e-12)
    
    
    # Read epochs:
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,
                          picks=picks, baseline=baseline, reject=reject)
                        

    
    print('------------ End find epochs ------------------')
    
   
    print('------------ Start average epochs ------------------')
    evoked = epochs.average()

    ylim = dict(grad=[-60,60], mag=[-130,130])  
    
    window_title = 'stim 1' 
    #picks = ([1, 2, 3])
    evoked.plot(exclude='bads', unit=True, show=True,
             ylim=ylim, xlim='tight', proj=True, hline=None,
             units=None, scalings=None, titles=None, axes=None,
             gfp=True, spatial_colors=True, window_title=window_title)

   
    
    
    print('------------ End average epochs ------------------')
    # topography plots
    print('------------ Start plot topo ------------------')
    
   # h0=evoked.plot_topomap(times=np.linspace(-0.01, 0.2, 5), ch_type='mag');
    evoked.plot_topomap(times='peaks', ch_type='mag');
    #h0.savefig('test_save_topo.png', dpi=120, format='png')
    #evoked.plot_topomap(times=np.linspace(-0.01, 0.2, 5), ch_type='grad');
    evoked.plot_topomap(times='peaks', ch_type='grad');
    #evoked.plot_topomap(times=np.linspace(0.05, 0.15, 5), ch_type='eeg');
    print('------------ Start plot topo ------------------')
    #trig = 1;
    title = 'Sensor Ave' + '..' + d_file + '..' + '_Trig_ ' + str(trig)
    print title
    
    h1 = plot_evoked_topo(evoked, title=title)
    h1.patch.set_facecolor('black')
    plot_title = title + '.pdf'
    #plt.savefig(plot_title,facecolor=fig.get_facecolor(), edgecolor='none')
    topoplotname = d_file 
    #h1.savefig('test_save_topo_all.png', dpi=120, format='png')
    print ('----------- Sensor Averages Done --------------------')
    
    title='stim 1'    
    h12 = plot_evoked_topo(evoked, title=title)
    h12.patch.set_facecolor('black')
    plot_title = title + '.pdf'
    plt.savefig(plot_title,facecolor=fig.get_facecolor(), edgecolor='none')
    topoplotname = d_file 

    report = Report()

    
    return(evoked)