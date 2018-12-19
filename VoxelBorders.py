'''
Written By Grayson Frazier
Contains the code to make borders for both .mic formats
'''

from MicFileTool import read_mic_file
import numpy as np

def order_square_data():
    '''
    Top to Bottom and then Left to Right
    This is already assumed in the files, but just to be safe :)
    Assumes all z are the same
    '''
    snp = sorted(snp , key=lambda k: [k[1], k[0], k[3]]) #also sorts by triangle orientation (column, ro, then orientation)
    return snp

class border():
    '''
    simple class just to make things prettier
    in the form
    [[x1,y1], [x2,y2], left/up data, right/down data]
    '''
    def __init__(self, point1, point2, luvoxel = None, rdvoxel=None):
        self.point1 = point1
        self.point2 = point2
        self.luvoxel = luvoxel
        self.rdvoxel = rdvoxel

def make_triangle_borders(snp, sw):
    '''
    Makes Triangular Borders for Legacy Formatted .mic data
    Returns two border lists:
        border_list #in the form [line segment, left/up voxel, right/down voxel]
        outside_edges #these are just outside borders in the form [line segment, voxel]

    Legacy File Format:
        Col 0-2 x, y, z
        Col 3   1 = triangle pointing up, 2 = triangle pointing down
        Col 4 generation number; triangle size = sidewidth /(2^generation number )
        Col 5 Phase - 1 = exist, 0 = not fitted
        Col 6-8 orientation
        Col 9  Confidence
    '''
    side = sw/2**snp[0,4]
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
                row_dict[(indx, 'u')] = sorted( row_dict[(indx, 'u')], key=lambda k: [k[0], k[1], k[2]])
            else:
                row_dict[indx, 'u'] = [voxel]

        if voxel[3] == 2: #triangle down
            if (indx, 'd') in row_dict.keys():
                row_dict[(indx, 'd')].append(voxel)
                row_dict[(indx, 'd')] = sorted( row_dict[(indx, 'd')], key=lambda k: [k[0], k[1], k[2]])
            else:
                row_dict[indx, 'd'] = [voxel]


    row_keys = row_dict.keys()
    row_keys = list(row_dict.keys())


    border_list = [] #in the form [line segment, left/up voxel, right/down voxel]
    outside_edges = [] #these are just outside borders in the form [line segment, voxel]

    row_num_list = []
    for key in list(row_dict.keys()):
        row_num_list.append(key[0])
    max_row = max(row_num_list)

    print("row_dict is alive!")

    #########################################################################################################################
    rcount = 0
    lcount = 0 #for debugging...
    #Connecting Rows (Attempt 501)
    #Start with down-facing and so on...
    count=0
    for row_key1 in list(row_dict.keys()):
        row_num = row_key1[0]
        if row_num == max_row:
            break
        row_orient = row_key1[1] #'u' or 'd'
        if row_orient == 'd':
            row_key2 = (row_num+1, 'u')
            if row_key2 not in list(row_dict.keys()):
                break
            for indx1 in range(len(row_dict[row_key1])):
                voxel1 = row_dict[row_key1][indx1]
                x1 = voxel1[0]
                y1 = voxel1[1]
                for indx2 in range(len(row_dict[row_key2])):
                    voxel2 = row_dict[row_key2][indx2]
                    x2, y2 = voxel2[0], voxel2[1]
                    old_side = side
                    side = sw/2**voxel1[4]
                    if side != old_side:
                        print("side different")
                    #case 1, to the right
                    if abs(x2-x1) <= side*1.49 and x2>x1 and indx2 != 0 and indx1!=0: #new point is to da right
                        count +=1
                        voxel2 = row_dict[row_key2][indx2-1]
                        segment = [[x1,y1],[x2,y2]]
                        border_list.append([segment, voxel1, voxel2])
                        rcount += 1
                        if rcount ==1:
                            print(abs(x2-x1) - side)


                    #case 2, to the left
                    #NOTE: changing the above to 1.49 drastically changes amount plotted...maybe use 2 ifs?
                    elif abs(x2-x1) <= side*1.49 and x2<x1 and indx1 != 0 and indx2!=0: #new point is to da right
                        count +=1
                        voxel1 = row_dict[row_key1][indx1-1]
                        segment = [[x1,y1],[x2,y2]]
                        border_list.append([segment, voxel1, voxel2])
                        lcount += 1
                        if lcount ==1:
                            print((abs(x2-x1) - side)/side)
    print("Row-to-Row a-ok")



    #The Same-Row (i.e. horizontal) Borderss
    for row in row_dict.keys():
        if row[1] == 'u':
            row_num = row[0]
            for voxel1 in row_dict[row]:
                x1,y1 = voxel1[0], voxel1[1]
                for voxel2 in row_dict[row_num, 'd']:
                    if abs(voxel2[0]-x1)<.0001 and abs(voxel2[1]-y1) <= .001:
                        x2,y2 = voxel2[0]+side, voxel2[1]
                        segment = [[x1,y1], [x2,y2]]
                        border_list.append([segment, list(voxel1), list(voxel2)])
                        break #for time

    print("Same-Row okeedokee")


    #The Top Edges
    if (0, "u") in list(row_dict.keys()):
        print("Doin Top Edges")
        row = (0, 'u')
        for voxel in row_dict[row]:
            x1 = voxel[0]
            y1 = voxel[1]
            x2 = voxel[0] + side/2
            y2 = voxel[1] + side*np.sqrt(3)/2
            x3 = x1 + side
            y3 = y1
            segment1 = [[x1,y1], [x2,y2]]
            segment2 = [[x2,y2], [x3,y3]]
            outside_edges.append([segment1, voxel])
            outside_edges.append([segment2, voxel])

    print("Top doin mighty fine")



    #The Bottom Edges
    if (max_row, 'd') in list(row_dict.keys()):
        row = (max_row, 'd')
        print("Doin Bottom Row")
        for voxel in row_dict[row]:
            x1 = voxel[0]
            y1 = voxel[1]
            x2 = voxel[0] + side/2
            y2 = voxel[1] - side*np.sqrt(3)/2
            x3 = x1 + side
            y3 = y1
            segment1 = [[x1,y1], [x2,y2]]
            segment2 = [[x2,y2], [x3,y3]]
            outside_edges.append([segment1, voxel])
            outside_edges.append([segment2, voxel])
    print("Bottom Edges Okeedokee")

    side = sw/2**snp[0][4]
    """
    #The Left Edges
    for row in list(row_dict.keys()):
        voxel = row_dict[row][0]
        if row[1] == 'u':
            x1 = voxel[0]
            y1 = voxel[1]
            x2 = x1 + side/2
            y2 = y1 + 3**.5/2*side
            segment1 = [[x1,y1], [x2,y2]]
            segment2 = [[x2,y2], [x3,y3]]
            print(segment1)                                               #Fix here, something has gone wrong, but it compiles at least...lol
            outside_edges.append([segment1, voxel])
            outside_edges.append([segment2, voxel])
        if row[1] == 'd':
            x1 = voxel[0]
            y1 = voxel[1]
            x2 = x1 + side/2
            y2 = y1 - 3**.5/2*side
            segment1 = [[x1,y1], [x2,y2]]
            segment2 = [[x2,y2], [x3,y3]]
            outside_edges.append([segment1, voxel])
            outside_edges.append([segment2, voxel])
    print("Left Edges Lookin' Fine")
    """
    """
    #The Right Edges
    for row in list(row_dict.keys()):
        voxel = row_dict[row][-1]
        if row[1] == 'u':
            x1 = voxel[0]
            y1 = voxel[1]
            x2 = x1 + side/2
            y2 = y1 + np.sqrt(3)/2*side
            segment1 = [[x1,y1], [x2,y2]]
            segment2 = [[x2,y2], [x3,y3]]
            outside_edges.append([segment1, voxel])
            outside_edges.append([segment2, voxel])
        if row[1] == 'd':
            x1 = voxel[0]
            y1 = voxel[1]
            x2 = x1 + side/2
            y2 = y1 - np.sqrt(3)/2*side
            segment1 = [[x1,y1], [x2,y2]]
            segment2 = [[x2,y2], [x3,y3]]
            outside_edges.append([segment1, voxel])
            outside_edges.append([segment2, voxel])
    print("Right Edges All Aboard")
    """
    return border_list, outside_edges



def make_square_borders(old_smd):
    '''
    Makes square borders
    image already inverted, x-horizontal, y-vertical, x dow to up, y: left to right
    squareMicData: [NVoxelX,NVoxelY,10], each Voxel conatains 10 columns:
            0-2: voxelpos [x,y,z]
            3-5: euler angle
            6: hitratio
            7: maskvalue. 0: no need for recon, 1: active recon region
            8: voxelsize
            9: additional information
    Returns two border lists:
        border_list #in the form [line segment, left/up voxel, right/down voxel]
        outside_edges #these are just outside borders in the form [line segment, voxel]
    '''
    #squareMicData organizes by x values, but I shall alter it b/c I am lazy and it is easier to make borders
    smd = []
    for column_list in old_smd:
        for voxel in column_list:
            smd.append(list(voxel))
    print(smd[0])
    side = smd[0][8]
    y_value = smd[0][1] #initial value
    row_num = 0

    row_dict = dict()
    row_y_values = []
    count = 0
    #making rows to later make a border
    for voxel in smd:
        if round(voxel[1], 6) in row_y_values:
            indx = row_y_values.index(round(voxel[1],6))
        else:
            row_y_values.append(round(voxel[1], 6))
            row_y_values.sort()
            indx = len(row_y_values)-1 #last index

        if indx in row_dict.keys():
            row_dict[indx].append(voxel)
            row_dict[indx] = sorted(row_dict[indx], key=lambda k: [k[0], k[1], k[2]])
        else:
            row_dict[indx] = [voxel]
            count += 1
    print("row-dict is alive!")

    row_keys = row_dict.keys()
    row_keys = list(row_dict.keys())

    border_list = []
    outside_edges = []


    max_row = 0
    for row in list(row_dict.keys()):
        if row >= max_row:
            max_row = row

    #Connecting Rows (Attempt 501)
    #Start with down-facing and so on...
    count=0
    for row_key1 in list(row_dict.keys()):
        if row_key1 == max_row:
            break
        row_key2 = row_key1 + 1
        for indx1 in range(len(row_dict[row_key1])):
            voxel1 = row_dict[row_key1][indx1]
            x1, y1 = voxel1[0], voxel1[1]
            for indx2 in range(len(row_dict[row_key2])):
                voxel2 = row_dict[row_key2][indx2]
                x2,y2 = voxel2[0], voxel2[1]
                if abs(x1-x2) < .0001:
                    segment = [[x1,y1], [x2,y2]]
                    lvoxel = row_dict[row_key2][indx2-1]
                    rvoxel = voxel2
                    border_list.append([segment, lvoxel, rvoxel])


    #The Same-Row (i.e. horizontal) Borderss
    for row1 in row_dict.keys():
        if row1 == max_row:
            break
        row2 = row1 + 1
        for voxel1 in row_dict[row1]:
            x1,y1 = voxel1[0], voxel2[1]
            for voxel2 in row_dict[row2]:
                x2,y2 = voxel2[0], voxel2[1]
                if abs(x1-x2)-side <= .0001:
                    segment = [[x1,y1], [x1 + side,y1]]
                    border_list.append([segment, voxel1, voxel2])


    print("Same-Row okeedokee")

    #quick check to make formatting went a-ok
    for border in border_list:
        if len(border) < 3:
            print(border_list.index(border))

    return border_list, outside_edges


def color_borders(border_list, function, minval=0, maxval =1):
    '''
    return alpha_values for border lines
    border_list in the form [segment, voxel1, voxel2]
    default alpha is 0
    return: alpha_values
    '''


    alpha_list = []
    for border in border_list:
        value1 = function(border[1])
        value2 = function(border[2])
        if abs(value1-value2) <= maxval and abs(value1-value2) >= minval:
            alpha_list.append(1)
        else:
            alpha_list.append(0)

    return alpha_list


def angle_is_close(ang_list1, ang_list2):
    '''
    quick lazy way to color
    '''
    color = [1,1,1]
    for i in range(len(ang_list1)):
        ang1 = ang_list1[i]
        ang2 = ang_list2[i]
        if abs(ang1-ang2) > 1:
            color = [0,0,0]
            break

    return color
