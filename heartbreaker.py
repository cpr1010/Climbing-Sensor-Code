#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
from scipy import signal
from IPython.display import clear_output




text_file = open(r"C:\Users\coler\OneDrive\Desktop\CPSC 601 - Climbing Data\heartbreaker.txt", "r")
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

#clear_output(wait=True)



fig, ax = plt.subplots(2)
ax[0].set_title("Acceleration Sum Vector")
ax[0].plot(butter_sumVec, color='r')
ax[0].set_ylim((0,4))
ax[0].set_ylabel("Gravity (G's')")
ax[0].fill_between((300, 380),4, color='grey', alpha=.2)
ax[1].set_title("Hip Distance from Wall")
ax[1].plot(butter_dist)
ax[1].fill_between((300, 380),1000, color='grey', alpha=.2)
ax[1].set_ylim((0, 1000))
ax[1].set_ylabel("Millimeters")
fig.subplots_adjust(hspace=.5)
plt.show()


# In[56]:


def sliding_window3(data_set, dist, win_size):
    
    dynamic_moves = []
    mvs = 0
    
    for index, i in enumerate(data_set):
        position = 0
        index = index+position
        if i >=1.2:
            for j in data_set[index:index+win_size]:
                if j <=0.87:
                    a = [index-10, index+win_size+10]
                    dynamic_moves.append(a)
                    position
                    break
                
                    
                    
                    
                else:
                    position = 0
                    pass
                
                
        else:
            pass
        
    def consecutive2(data, stepsize=1):
        ans = []
        splt = np.split(data, np.where(np.diff(data[:,0]) != stepsize)[0]+1)
        for i in splt:
            a = sum(i)/len(i)
            ans.append(a)

        return ans 
    dynamic_moves = np.array(dynamic_moves)
    ans = consecutive2(dynamic_moves, 1)
    
    hip_moves = []
    for i in ans:
        a = dist[round(i[0]): round(i[1])]
        hip_moves.append(a)
        
    accel_moves = []
    for i in ans:
        a = data_set[round(i[0]): round(i[1])]
        accel_moves.append(a)
   
                
    fig, ax = plt.subplots(2)
#ax[0].plot(sumVec)
    ax[0].plot(data_set, color='r')
    ax[0].set_title("Acceleration Sum Vector")
    ax[0].set_ylabel("Gravity")
    ax[1].plot(dist)
    ax[1].set_title("Hip Distance From the Wall")
    ax[1].set_ylabel("Distance in Millimeters")
    ax[1].set_xlabel("Frames at 25 ms(p)")
    for i in ans:
        ax[0].fill_between(i,1.5, color='grey', alpha=.2)
        ax[1].fill_between(i,1000, color='grey', alpha=.2)
        ax[1].set_ylim((0, 1000))
    fig.subplots_adjust(hspace=.5)
                
    return np.array(hip_moves), np.array(accel_moves)

    
hip_moves, accel_moves = sliding_window3(butter_sumVec[150:350], butter_dist[150:350],10)

   
    



# In[54]:


for i in hip_moves:
    a = round(np.max(i) - np.min(i),2)
    print("Hips moved " + str(a) + " closer to the wall")

hip_max = []
hip_min = []
for i in hip_moves[0:-2]:
    a = np.max(i)
    b = np.min(i)
    hip_max.append(a)
    hip_min.append(b)
    
print(round(np.mean(hip_max),2))
print(round(np.mean(hip_min),2))

peak_accel = 0
min_accel = 0
for i in accel_moves:
    peak_accel += np.max(i)
    min_accel += np.min(i)
    
av_peak = peak_accel/len(accel_moves)
av_min = min_accel/len(accel_moves)
print("Average peak acceleration " + str(round(av_peak, 2)))
print("Average min acceleration " + str(round(av_min, 2)))


# In[55]:


for i in range(0, len(hip_moves)):
    
    hm = hip_moves[i]
    am = accel_moves[i]

    minn = np.min(hm)
    ind = 0
    for i in hm:
        if i == minn:
            break

        else: 
            ind += 1


    min2 = np.min(am)
    ind2 = 0
    for i in am:
        if i == min2:
            break

        else: 
            ind2 += 1


    ans = ind - ind2
    print(ans)


# In[3]:


fig, ax = plt.subplots(2)
ax[0].set_title("Acceleration Sum Vector")
ax[0].plot(butter_sumVec[300:380], color='r')
ax[0].set_ylim((0,2))
ax[0].set_ylabel("Gravity (G's)")
ax[1].set_title("Hip Distance from Wall")
ax[1].plot(butter_dist[300:380])
ax[1].set_ylim((0, 1000))
ax[1].set_ylabel("Millimeters")
fig.subplots_adjust(hspace=.5)
fig.set_figwidth(3)
plt.show()


# In[4]:


import numpy as np
import matplotlib.pyplot as plt
from scipy import pi
from scipy.fftpack import fft

sample_rate = 100
N = (2 - 0) * sample_rate

frequency = np.linspace (0.0, 50, int (N/2))

freq_data = fft(sumVec)
y = 2/N * np.abs (freq_data [0:np.int (N/2)])

plt.plot(frequency, y)
plt.title('Frequency domain Signal for Acceleration Magnitude')
plt.xlabel('Frequency in Hz')
plt.ylabel('Amplitude')
plt.show()
plt.savefig(r"C:\Users\coler\OneDrive\Desktop\FFT_sumVec.jpg")


# In[5]:


import numpy as np
import matplotlib.pyplot as plt
from scipy import pi
from scipy.fftpack import fft

sample_rate = 100
N = (2 - 0) * sample_rate

frequency = np.linspace (0.0, 50, int (N/2))

freq_data = fft(dist)
y = 2/N * np.abs (freq_data [0:np.int (N/2)])

plt.plot(frequency, y)
plt.title('Frequency domain Signal for Distance data')
plt.xlabel('Frequency in Hz')
plt.ylabel('Amplitude')
plt.show()
plt.savefig(r"C:\Users\coler\OneDrive\Desktop\FFT_dist.jpg")


# In[ ]:




