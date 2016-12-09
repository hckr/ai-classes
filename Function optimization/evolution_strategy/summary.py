from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

def prepare_summary(title, data):
    fig = plt.figure(figsize=(8, 8))
    fig.patch.set_facecolor('white')
    fig.canvas.set_window_title(title)
    num_plots = len(data)
    subplot_index = 1
    for d in data:
        ax = fig.add_subplot(num_plots, 1, subplot_index)
        ax.plot(d[1], 'm')
        ax.set_title(d[0])
        ax.set_xlabel('Epoch')
        subplot_index += 1
    plt.tight_layout()
        
def show_summaries():
    plt.show()
