'''
Quick test to get stuff goin
https://stackoverflow.com/questions/21352580/matplotlib-plotting-numerous-disconnected-line-segments-with-different-colors
https://matplotlib.org/examples/pylab_examples/line_collection2.html
'''

import MicFileTool
import VoxelBorders
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np


def run_triangle():
    #sw, snp = MicFileTool.read_mic_file("Al_final_z1_refit.mic")
    sw, snp = MicFileTool.read_mic_file("395z0.mic.LBFS")
    border_list, outside_edges = VoxelBorders.make_triangle_borders(snp,sw)

    border_lines = []
    edges = []
    for border in border_list:
        border_lines.append(border[0])
    for edge in outside_edges:
        edges.append(edge[0])

    border_collecton = mc.LineCollection(border_lines)
    edge_collection = mc.LineCollection(edges)
    ax = plt.axes()
    ax.add_collection(border_collecton)
    ax.add_collection(edge_collection)

    fig = plt.gcf()
    ax.set_xlim((-1,1))
    ax.set_ylim((-1,1))
    #plt.show()

    ############################################################################
    border_lines = []
    edges = []
    for border in border_list:
        border_lines.append(border[0])
    for edge in outside_edges:
        edges.append(edge[0])

    c = [] #to colorize
    for indx in range(len(border_lines)):
        border = border_lines[indx]
        voxel1 = border_list[indx][1]
        voxel2 = border_list[indx][2]
        angs1 = voxel1[3:6]
        angs2 = voxel2[3:6]
        c.append(angle_is_close(angs1, angs2))
    border_collection = mc.LineCollection(border_lines)
    edge_collection = mc.LineCollection(edges)
    border_collection.set_color(c)
    ax = plt.axes()
    ax.add_collection(border_collection)


    fig = plt.gcf()
    ax.set_xlim((-1,1))
    ax.set_ylim((-1,1))
    plt.show()

def write_smd(mic_data):
    smd = np.load(mic_data)[0]
    fname = mic_data+".txt"
    file = open(fname, "w")
    for line in smd:
        file.write(str(line)+"\n")
    file.close()

def angle_is_close(ang_list1, ang_list2):
    color = [1,1,1]
    for i in range(len(ang_list1)):
        ang1 = ang_list1[i]
        ang2 = ang_list2[i]
        if abs(ang1-ang2) > .9:
            color = [0,0,0]
            break

    return color

def run_square():
    smd = np.load("SearchBatchSize_13000_100x100_0.01.npy")
    #write_smd("SearchBatchSize_13000_100x100_0.01.npy")
    #print (smd)
    border_list, outside_edges = VoxelBorders.make_square_borders(smd)

    border_lines = []
    edges = []
    for border in border_list:
        border_lines.append(border[0])
    for edge in outside_edges:
        edges.append(edge[0])

    c = [] #to colorize
    for indx in range(len(border_lines)):
        border = border_lines[indx]
        voxel1 = border_list[indx][1]
        voxel2 = border_list[indx][2]
        angs1 = voxel1[3:6]
        angs2 = voxel2[3:6]
        c.append(angle_is_close(angs1, angs2))
    border_collection = mc.LineCollection(border_lines)
    edge_collection = mc.LineCollection(edges)
    border_collection.set_color(c)
    ax = plt.axes()
    ax.add_collection(border_collection)


    fig = plt.gcf()
    ax.set_xlim((-1,1))
    ax.set_ylim((-1,1))
    plt.show()


#run_triangle()
#run_square()

from MicFileTool import MicFile
MicFile("395z0.mic.LBFS").plot_mic_patches()
