# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:20:41 2022

@author: coler
"""

import pandas as pd
import numpy as np
from scipy import signal
from IPython.display import clear_output


while True:

    text_file = open(r"C:\Users\coler\OneDrive\Desktop\wearable_climbing.txt", "r")
    lines = text_file.readlines()

    values = lines[0].split(",")

    values = np.array(values)

    arr = []

    for i in values[0:-2]:
        a = float(i)
        arr.append(a)

    dist = arr[0::2]
    sumVec = arr[1::2]


    def butter_lowpass(cutoff, nyq_freq, order=4):
        normal_cutoff = float(cutoff) / nyq_freq
        b, a = signal.butter(order, normal_cutoff, btype='lowpass')
        return b, a

    def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
        # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
        b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
        y = signal.filtfilt(b, a, data)
        return y

    butter_dist = butter_lowpass_filter(dist, 40, 50, 4)

    butter_sumVec = butter_lowpass_filter(sumVec, 40, 50, 4)

    import matplotlib.pyplot as plt

    clear_output(wait=True)



    fig, ax = plt.subplots(2)
    ax[0].set_title("Acceleration Sum Vector")
    ax[0].plot(butter_sumVec[-100:-1], color='r')
    ax[0].set_ylim((0,4))
    ax[0].set_ylabel("Gravity (G's')")
    ax[1].set_title("Hip Distance from Wall")
    ax[1].plot(butter_dist[-100:-1])
    ax[1].set_ylim((0, 1000))
    ax[1].set_ylabel("Millimeters")
    fig.subplots_adjust(hspace=.5)
    plt.show()