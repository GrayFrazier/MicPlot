"""
'''
Writen by Grayson Frazier

This script contains the "VoxelClick" class which allows for interaction with plot
To be used with plot_mic_patches function in MicFileTool
Newly Updated with Grayson's hopeful attempt to reintroduce borders
'''

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.collections import Collection
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection
import numpy as np
import math


class Voxel():
    '''
    This will be used to efficiently keep track of the different plotted voxels
    Includes the actual voxels as well as the borderlines
    '''
    def __init__(self, shape, border):
        self.shape = shape
        self.border = border
        #use left, right, and middle borders

class VoxelClick():
    '''
    Contains all the Voxels from Mic Data
    Organizes the Voxels for efficiency
    Creates an interactive environment

    Legacy File Format:
        Col 0-2 x, y, z
        Col 3   1 = triangle pointing up, 2 = triangle pointing down
        Col 4 generation number; triangle size = sidewidth /(2^generation number )
        Col 5 Phase - 1 = exist, 0 = not fitted
        Col 6-8 orientation
        Col 9  Confidence
    '''
    def __init__(self, fig, snp, sw, Mic):
        '''
        Canvas figure, snp data, base sidewdth
        '''
        self.snp = snp #all voxel data in legacy format
        self.sw = sw #base generation for triangles
        self.fig = fig
        self.size = self.sw/2**(snp[1,4])
        self.mic = Mic

    def press(self, event):
        if event.key == None:
            return
        if event.key == "enter":
            assert self.clicked_angles != [], "Please click a voxel first"
            self.mic.plot_mic_patches(plotType=1,minConfidence=0.8,maxConfidence=1.0,limitang=True,angles=self.clicked_angles)

    def onclick(self, event):
        if event.xdata == None or event.ydata == None:
            return #ensures the mouse event is on the canvas

        xdata = event.xdata
        ydata = event.ydata

        self.centers = []
        for i in range(len(self.snp)):
            if self.snp[i,3] == 1: #for a triangle pointed up
                self.centers.append([self.snp[i,0]+self.sw/(2**self.snp[i,4])/2 , self.snp[i,1]+self.sw/(2**self.snp[i,4])/2*np.sqrt(3)/2])
            else:
                self.centers.append([self.snp[i,0]+self.sw/2**self.snp[i,4]/2 , self.snp[i,1]-self.sw/(2**self.snp[i,4])/2*np.sqrt(3)/2])
        self.centers = np.array(self.centers) #this is used to place the marker in the center of the triangluar voxel

        def find_indices(x,y):
            closest_x_distance = abs(self.centers[1,0]-x)
            closest_y_distance = abs(self.centers[1,1]-y)
            for i in range(len(self.snp)):
                if abs(self.centers[i,0] - x) < closest_x_distance:
                    closest_x_distance = abs(self.centers[i,0]-x)
                    closest_index = i
                if abs(self.centers[i,1] - y) < closest_y_distance:
                    closest_y_distance = abs(self.centers[i,1]-y)

            indices = [] #should just be one indice, but will include a list to avoid error
            for i in range(len(self.snp)):
                if abs(abs(self.centers[i,0]-x)-closest_x_distance) <= closest_x_distance:
                    if abs(abs(self.centers[i,1]-y)-closest_y_distance) <= closest_y_distance:
                        indices.append(i)
            return indices

        indices = find_indices(xdata, ydata)
        assert len(indices) != 0, "No Indices Found"

        def list_average(L): #just to find the average orientation
            assert type(L) == list
            sum = 0
            for i in L:
                sum += i
            return sum/len(L)

        Orientation1 = [self.snp[i, 6] for i in indices]
        Orientation2 = [self.snp[i, 7] for i in indices]
        Orientation3 = [self.snp[i, 8] for i in indices]
        avg_Orientation1, avg_Orientation2, avg_Orientation3 = list_average(Orientation1), list_average(Orientation2), list_average(Orientation3)

        self.clicked_angles = [avg_Orientation1, avg_Orientation2, avg_Orientation3]

        if len(indices)>1:
            print("------------------------------------------------------\nAverage Euler Angles: (", self.clicked_angles[0], ",", self.clicked_angles[1], ",", self.clicked_angles[2], ")")
            print(self.snp[indices[0]][9])
            print("To replot, press enter")
        else:
            print("------------------------------------------------------\nEuler Angles: (",self.clicked_angles[0], ",", self.clicked_angles[1], ",", self.clicked_angles[2], ")")
            print(self.snp[indices[0]][9])
            print("To replot, press enter")

        #self.mic.plot_mic_patches(plotType=1,minConfidence=0.8,maxConfidence=1.0,limitang=True,angles=self.clicked_angles)
        if event.dblclick: #if event.dblclick:#double click to replot the grain
            print("gonna plot now")
            self.mic.plot_mic_patches(plotType=1,minConfidence=0,maxConfidence=1,limitang=True,angles=self.clicked_angles)

    def connect(self):
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.press)

class VoxelBorders(): #possibly make it derivative of LineCollection
    '''
    This class will highlight different borders of the voxels based on orientation
    To be used in conjuction with RotRep.py
    '''
    def __init__(self, snp, sw):
        self.snp = snp
        self.sw = sw
        self.border_list, self.outside_edges = Make_Borders(snp, sw)

        alpha_levels = []
        lines = []
        for border in self.border_list:
            lines.append(self.border_list[0])
            alpha_levels.append(1)
        self.border_collection = LineCollection(lines)
        self.alpha_levels = alpha_levels

    def draw_borders(self, function):
        '''
        Function which goes through every border and will either make it visible or invisible
        Border is determined by a function inputed from the RotRep
        '''
	for border in self.border_list:
		if function(border) >= threshold:
			border.alpha_level = 0
		else:
			border.alpha_level =1
	return borders
        return None

"""






'''
Writen by Grayson Frazier

Please consult a very elegant user guide for how to use basic functions

This script contains the "VoxelClick" class which allows for interaction with plot
To be used with plot_mic_patches function in MicFileTool

Modified by Doyee Byun
Added feature that supports the new square matrix data format

Modified Once Again by Grayon Frazier
Added borders to the pixel matrix
'''

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.collections import Collection
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
from matplotlib.collections import PatchCollection
import numpy as np

class SquareVoxelClick():
    '''
    modified VoxelClick for squarematrix data format

    Squre mic data format
    image already inverted, x-horizontal, y-vertical, x dow to up, y: left to right
    :param squareMicData: [NVoxelX,NVoxelY,10], each Voxel conatains 10 columns:
            0-2: voxelpos [x,y,z]
            3-5: euler angle
            6: hitratio
            7: maskvalue. 0: no need for recon, 1: active recon region
            8: voxelsize
            9: additional information

    Legacy File Format:
        Col 0-2 x, y, z
        Col 3   1 = triangle pointing up, 2 = triangle pointing down
        Col 4 generation number; triangle size = sidewidth /(2^generation number )
        Col 5 Phase - 1 = exist, 0 = not fitted
        Col 6-8 orientation
        Col 9  Confidence
    '''
    def __init__(self, fig, smd,squaremic,minHitRatio,misor_thresh):
        '''
        Canvas figure, snp data, base sidewdth
        '''
        self.smd = smd
        self.squaremic = squaremic
        self.fig = fig
        self.size = smd[0,0,8]
        self.minHitRatio = minHitRatio
        self.misor_thresh = misor_thresh


    def onclick(self, event):
        if event.xdata == None or event.ydata == None:
            return #ensures the mouse event is on the canvas

        xdata = event.xdata+495
        ydata = event.ydata+495
        #print(xdata)
        #print(ydata)

        def find_indices(x,y):
            xi = int(x/10)
            yi = int(y/10)
            indices = (xi,yi) #should just be one indice, but will include a list to avoid error
            return indices

        (xi,yi) = find_indices(xdata, ydata)
        #assert len(indices) != 0, "No Indices Found"

        orient1 = self.smd[xi,yi,3]
        orient2 = self.smd[xi,yi,4]
        orient3 = self.smd[xi,yi,5]

        self.clicked_angles = [orient1, orient2, orient3]
        print("------------------------------------------------------")
        print("X_index: ",xi)
        print("Y_index: ",yi)
        print("X_value: ",self.smd[xi,yi,0])
        print("Y_value: ",self.smd[xi,yi,1])
        print("Angles:", orient1, orient2, orient3)

        if event.dblclick:#double click to replot the grain
            self.squaremic.plot_orientation([xi,yi],minHitRatio = self.minHitRatio,misor_thresh=self.misor_thresh)

    def connect(self):
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)



class VoxelClick():
    '''
    Contains all the Voxels from Mic Data
    Organizes the Voxels for efficiency
    Creates an interactive environment

    Legacy File Format:
        Col 0-2 x, y, z
        Col 3   1 = triangle pointing up, 2 = triangle pointing down
        Col 4 generation number; triangle size = sidewidth /(2^generation number )
        Col 5 Phase - 1 = exist, 0 = not fitted
        Col 6-8 orientation
        Col 9  Confidence
    '''
    def __init__(self, fig, snp, sw, mic):
        '''
        Canvas figure, snp data, base sidewdth
        '''
        self.snp = snp #all voxel data in legacy format
        self.sw = sw #base generation for triangles
        self.fig = fig
        self.size = self.sw/2**(snp[1,4])
        self.mic = mic

    def onclick(self, event):
        if event.xdata == None or event.ydata == None:
            return #ensures the mouse event is on the canvas

        xdata = event.xdata
        ydata = event.ydata

        self.centers = []
        for i in range(len(self.snp)):
            if self.snp[i,3] == 1: #for a triangle pointed up
                self.centers.append([self.snp[i,0]+self.sw/(2**self.snp[i,4])/2 , self.snp[i,1]+self.sw/(2**self.snp[i,4])/2*np.sqrt(3)/2])
            else:
                self.centers.append([self.snp[i,0]+self.sw/2**self.snp[i,4]/2 , self.snp[i,1]-self.sw/(2**self.snp[i,4])/2*np.sqrt(3)/2])
        self.centers = np.array(self.centers) #this is used to place the marker in the center of the triangluar voxel

        def find_indices(x,y):
            closest_x_distance = abs(self.centers[1,0]-x)
            closest_y_distance = abs(self.centers[1,1]-y)
            for i in range(len(self.snp)):
                if abs(self.centers[i,0] - x) < closest_x_distance:
                    closest_x_distance = abs(self.centers[i,0]-x)
                    closest_index = i
                if abs(self.centers[i,1] - y) < closest_y_distance:
                    closest_y_distance = abs(self.centers[i,1]-y)

            indices = [] #should just be one indice, but will include a list to avoid error
            for i in range(len(self.snp)):
                if abs(abs(self.centers[i,0]-x)-closest_x_distance) <= closest_x_distance:
                    if abs(abs(self.centers[i,1]-y)-closest_y_distance) <= closest_y_distance:
                        indices.append(i)
            return indices

        indices = find_indices(xdata, ydata)
        assert len(indices) != 0, "No Indices Found"

        def list_average(L): #just to find the average orientation
            assert type(L) == list
            sum = 0
            for i in L:
                sum += i
            return sum/len(L)

        Orientation1 = [self.snp[i, 6] for i in indices]
        Orientation2 = [self.snp[i, 7] for i in indices]
        Orientation3 = [self.snp[i, 8] for i in indices]
        avg_Orientation1, avg_Orientation2, avg_Orientation3 = list_average(Orientation1), list_average(Orientation2), list_average(Orientation3)

        self.clicked_angles = [avg_Orientation1, avg_Orientation2, avg_Orientation3]

        if len(indices)>1:
            print("------------------------------------------------------\nAverage Angles:", list_average(Orientation1), list_average(Orientation2), list_average(Orientation3))
        else:
            print("------------------------------------------------------\n Angles:", list_average(Orientation1), list_average(Orientation2), list_average(Orientation3))

        if event.dblclick:#double click to replot the grain
            self.mic.plot_mic_patches(plotType=1,minConfidence=0.8,maxConfidence=1.0,limitang=True,angles=self.clicked_angles)

    def connect(self):
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

#################################################################################################
########### STUFF TO DO WITH BORDERS....#########################################################
#################################################################################################
def order_snp(snp):
    '''
    Takes the points in snp data and orders it
    Left to Right and then Top to Bottom (like reading)
    This is already assumed in the files, but just to be safe :)
    Assumes all z are the same
    '''
    snp = sorted(snp , key=lambda k: [k[1], k[0], k[3]]) #also sorts by triangle orientation (row, column, then orientation)
    return snp
