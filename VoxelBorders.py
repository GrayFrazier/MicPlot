'''
Quick test for the voxel borders function
Place holder, requires hand-made data
'''
from MicFileTool import read_mic_file
import numpy as np

#Self-made Row Dictionary:  Using 395z0.mic.LBFS
sw, snp = read_mic_file("395z0.mic.LBFS")

def make_borders(snp, sw):
    y_value = snp[0,1] #initial value
    row_num = 0

    row_dict = dict()
    row_y_values = []

    #making rows to later make a border
    for voxel in snp:

        if round(voxel[1], 6) in row_y_values:
            indx = row_y_values.index(round(voxel[1],6))
        else:
            row_y_values.append(round(voxel[1], 6))
            row_y_values.sort()
            indx = len(row_y_values)-1 #last index



        if voxel[3] ==1: #triangle up
            if (indx, 'u') in row_dict.keys():
                row_dict[(indx, 'u')].append(voxel)
                row_dict[(indx, 'u')] = sorted( row_dict[(indx, 'u')], key=lambda k: [k[0], k[1], k[3]])
            else:
                row_dict[indx, 'u'] = [voxel]

        if voxel[3] == 2: #triangle down
            if (indx, 'd') in row_dict.keys():
                row_dict[(indx, 'd')].append(voxel)
                row_dict[(indx, 'd')] = sorted( row_dict[(indx, 'd')], key=lambda k: [k[0], k[1], k[3]])
            else:
                row_dict[indx, 'd'] = [voxel]


    row_keys = row_dict.keys()
    row_keys = list(row_dict.keys())


    border_list = np.array([]) #in the form [line segment, left/up voxel, right/down voxel]
    outside_edges = np.array([]) #these are just outside borders in the form [line segment, voxel]






    '''The Row-to-row Borders''' #make sure last one doesn't call an errors
    for row in row_dict.keys():
        if row[1] == 'd': #dealing with down triangles"range((len(row_dict.keys())-len(row_dict.keys())%2)/2): #for every row (accounts for up and down hence the modulus)" <-- nevermid, ditched this format (too much work)
            for row1indx in range(len(row_dict[row])):#the row1indx is just the index of that row, just to make it easier for Grayson
                if (row[0]+1, 'u') in row_dict.keys():
                    for row2indx in range(len(row_dict[(row[0]+1, "u")])): #testing points in next row which are up triangless
                        bottom_key = (row[0] +1, "u") #just for ease on the eyes
                        if abs(row_dict[bottom_key][row2indx][0]-row_dict[row][row1indx][0]) <= 1.01*sw/2: #if the two points are within the desired side width (think right triangles)
                            if row_dict[row][row1indx][0] - row_dict[bottom_key][row2indx][0] <= 0: #the bottom row's point is to the left
                                if row1indx != 0: #the point is not the first in the index
                                    border_list = np.append(border_list, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[row][row1indx-1], row_dict[bottom_key][row2indx]])
                                    #                                      ^Line Segment                                                         ^Left/Upper Voxel          ^Lower/Right Voxel
                                else: #if first index, it is a left edge
                                    outside_edges = np.append(outside_edges, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]], row_dict[bottom_key][row2indx]])
                            else: #bottom row index to the right
                                if row2indx != len(row_dict[(row[0] + 1, 'd')])-1: #the point is not the last in the index
                                    border_list = np.append(border_list, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[bottom_key][row2indx-1], row_dict[row][row1indx]])
                                else: #iif last index, it is a right edge
                                    outside_edges = np.append(outside_edges, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[bottom_key][row2indx-1]])
                            break #break to save computing time

    print("Check 1: Row-to-Row a-ok")







    '''The Same-Row (i.e. horizontal) Borders'''
    for row in row_dict.keys():
        if row[1] == 'u':
            for i in range(len(row_dict[row])-1): #-1 to account for the last edge
                x = row_dict[row]
                y = x[i]
                z = y[0:2]

                border_list = np.append(border_list, [ [row_dict[row][i][0:2],        row_dict[row][i][0:2]],                 row_dict[row][i],         row_dict[(row[0], "d")][i]])
                #border_list = np.append(border_list, [ [row_dict[row][i][0:2],        row_dict[row][i][0:2]],                row_dict[row][(row[0], "d")]])

                #border_list = np.append(border_list, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[row][row1indx-1], row_dict[bottom_key][row2indx]])
                #######Something went wrong here.................................................................
                #based on border_list = np.append(border_list, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[row][row1indx-1], row_dict[bottom_key][row2indx]])

    print("Check 2: Same-Row okeedokee")







    '''The Top and Bottom Edges'''
    if (0, "u") in row_dict.keys():
        for i in range(len(row_dict[row])):
            point = row_dict[(0, "u")][i][0:2]
            sl = row_dict[(0, "u")][i][4] #generation number
            left_line =  [ [point, [point[0] + sl/2, point[1] + sl*np.sqrt(3)/2]] ]
            right_line = [ [[point[0] + sl/2, point[1] + sl*np.sqrt(3)/2]], [point[0] + sl, point[1]] ]

            outside_edges = np.append(outside_edges, [ left_line, row_dict[(0, "u")][i]])
            outside_edges = np.append(outside_edges, [ right_line, row_dict[(0, "u")][i]])
    print("Check 3: Top and Bottom doin mighty fine")







    """
    blah = [] #sorry, coulldn't think of a name
    for term in row_dict.keys():
        blah.append(term[0]) #row number
    if (max(blah), "d") in row_dict.keys():
        point = row_dict[(max(blah), "d")][i][0:2]
        sl = row_dict[(max(blah), "d")][i][4] #generation number
        left_line =  [ [point, [point[0] + sl/2, point[1] - sl*np.sqrt(3)/2]] ]
        right_line = [ [[point[0] + sl/2, point[1] - sl*np.sqrt(3)/2]], [point[0] + sl, point[1]] ]

        outside_edges = np.append(outside_edges, [ left_line, row_dict[(max(blah), "d")][i]])
        outside_edges = np.append(outside_edges, [ right_line, row_dict[(max(blah), "d")][i]])
    """


make_borders(snp,sw)
