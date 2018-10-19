'''
Written By Grayson Frazier
Contains the code to make borders for both .mic formats
'''

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
        
    

def make_square_borders(SquareMic, SquareMicData):
    '''
    Returns a collection of borders
    Includes the two points, and the left/up voxel and the right/down voxel
    voxel data in form of:
        0-2: voxelpos [x,y,z]
        3-5: euler angle
        6: hitratio
        7: maskvalue. 0: no need for recon, 1: active recon region
        8: voxelsize
        9: additional information
    In the form [(x,y), (x,y), left/up, right/down]
    '''
    #Data organized by column, row, then orientation

    def make_left_side(SquareMic, data):
        '''
        Make left wall
        Returns list
        '''
        point1 = [data[i][0], data[i][1], data[i][2]]
        point2 = [data[i][0], data[i][1], data[i][2]]
        left_border = [point1, point2, None, data]
        return left_border

    def make_right_side(SquareMic, data)
        '''
        Make right wall
        '''
        point1 = [data[i][0], data[i][1], data[i][2]]
        point2 = [data[i][0], data[i][1], data[i][2]]
        right_border = [point1, point, data, None ]
        return right_border

def order_snp(snp):
    '''
    Takes the points in snp data and orders it
    Left to Right and then Top to Bottom (like reading)
    This is already assumed in the files, but just to be safe :)
    Assumes all z are the same
    '''
    snp = sorted(snp , key=lambda k: [k[1], k[0], k[3]]) #also sorts by triangle orientation (row, column, then orientation)
    return snp

#Are you bored yet?  Ha, get it?  Borders?
#ok, I'll stop now


def make_triangle_border(snp, sw):
    '''
    Used to make a dictionary of rows
    To be implemented for triangular voxel type w/ legacy file format
    Assume that the data is ordered by x,y,z
    
    RowDict in the form [x, 'u'/'d'] = [voxelData]
    
    Legacy File Format:
    Col 0-2 x, y, z
    Col 3   1 = triangle pointing up, 2 = triangle pointing down
    Col 4 generation number; triangle size = sidewidth /(2^generation number )
    Col 5 Phase - 1 = exist, 0 = not fitted
    Col 6-8 orientation
    Col 9  Confidence
    '''
    
    x = snp[0][0] #takes the first x value'
    for voxel in snp:
        diff = x - snp[0]
        if voxel[3] == 1: #triangle up
            if round(diff, 5) <= .00001:
                row[x,]
        if abs(voxel[0][0]-x) <= 1e-4:
            row[x,]
    
    #initialize values
    y_value = snp[0,0] #initial value
    if snp[0][3] == 1: #Pointing up
        row = (0,'u')
    else:
        row = (0,'d')
    row_dict[row] = []

    #making rows to later make a border
    for i in range(len(snp)):
        if abs(snp[i,1] - y_value)<= .000001: #agrees with the accuracy of most mic files
            if snp[i,3] == 1: #Triangle facing up
               	 np.append(row_dict[(row[0], "u")], snp[i])

            else:
                row_dict[(row[0], "d")].append(snp[i])
        else:
            row = (row[0]+1, 'u')###change here
            y_value = snp[i,1]
            row_dict[row] = snp[i] #start a new row term
        

"""
def Make_Square_Borders(snp,sw):
    '''
    Requires the snp data and side width
    Parses through the entire mic file
    Makes borders to later be utilized by Borders class
    Left/Upper Voxel Data and then Right/Lower Voxel Data
    '''

    #MAKE TUPLES (ROW, u/d)  [u/d is just 'u' or 'd']
    order_snp(snp) #just to be sure
    #initializing primary values for the loop
    row_dict = {} #the format will be row:elements
    ################################
    ###Making Some changes##########
    ################################


    #initialize values
    y_value = snp[0,0] #initial value
    if snp[0][3] == 1: #Pointing up
        row = (0,'u')
    else:
        row = (0,'d')
    row_dict[row] = []

    #making rows to later make a border
    for i in range(len(snp)):
        if abs(snp[i,1] - y_value)<= .000001: #agrees with the accuracy of most mic files
            if snp[i,3] == 1: #Triangle facing up
               	 np.append(row_dict[(row[0], "u")], snp[i])

            else:
                row_dict[(row[0], "d")].append(snp[i])
        else:
            row = (row[0]+1, 'u')###change here
            y_value = snp[i,1]
            row_dict[row] = snp[i] #start a new row term
    print("here boi:", row_dict[list(row_dict.keys())[0]])
    print("here boi:", row_dict[(0, 'u')])
    #list(x.keys()) or do for i in x.keys()
    row_i = 1#initial value
    #row_dict[row] = []
    #making rows to later make a border
    for i in range(len(snp)):
        if abs(snp[i,1] - y_value)<= .000001: #agrees with the accuracy of most mic files
            if snp[i,3] == 1: #Triangle facing up
                row_dict[(row_i, "u")].append(snp[i])
            else:
                row_dict[(row_i, "d")].append(snp[i])
        else:
            row_i += 1 #(row+1, 'u')###change here
            x_value = snp[i,0]
            row_dict[(row_i, 'u'] = snp[i] #start a new row term
    #list(x.keys()) or do for i in x.keys()

    #and now it's time to make da borders!  Go top to bottom
    '''
    The thing below is kinda important...
    '''
    border_list = np.array([]) #in the form [line segment, left/up voxel, right/down voxel]
    outside_edges = np.array([]) #these are just outside borders in the form [line segment, voxel]

    '''The Row-to-Row Borders''' #make sure last one doesn't call an error
    for row in row_dict.keys():
        if row[1] == 'd': #dealing with down triangles"range((len(row_dict.keys())-len(row_dict.keys())%2)/2): #for every row (accounts for up and down hence the modulus)" <-- nevermid, ditched this format (too much work)
            for row1indx in range(len(row_dict[row])): #the row1indx is just the index of that row, just to make it easier for Grayson
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
                            if row2indx != len(row_dict[row+1])-1: #the point is not the last in the index
                                border_list = np.append(border_list, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[bottom_key][row2indx-1], row_dict[row][row1indx]])
                            else: #iif last index, it is a right edge
                                outside_edges = np.append(outside_edges, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[bottom_key][row2indx-1]])
                        break #break to save computing time

    '''The Same-Row (i.e. horizontal) Borders'''
    #print row_dict[row_dict.keys[0]]
    for row in row_dict.keys(): #must fix 'u'
        if row[1] == 'u':
            for i in range(len(row_dict[row])-1): #-1 to account for the last edge
                print("Check_0" + str(i))
                print(row_dict[row])
                print(row_dict[row][i])
                x = row_dict[row]
                y = x[i]
                print("y is ", y)
                z = y[0:2]
                print("Check 1: " + str(row_dict[row][i][0:2]))
                print("Check 2: " + str(row_dict[row][i][0:2]))
                print("Check 3: " + str(row_dict[row][i]))
                print("Check 4: " + str(row_dict[(row[0], "d")][i]))

                border_list = np.append(border_list, [ [row_dict[row][i][0:2],        row_dict[row][i][0:2]],                 row_dict[row][i],         row_dict[(row[0], "d")][i]])
                #border_list = np.append(border_list, [ [row_dict[row][i][0:2],        row_dict[row][i][0:2]],                row_dict[row][(row[0], "d")]])
                border_list = np.append(border_list, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[row][row1indx-1], row_dict[bottom_key][row2indx]])
                #######Something went wrong here.................................................................
                #based on border_list = np.append(border_list, [ [row_dict[row][row1indx][0:2], row_dict[bottom_key][row2indx][0:2]] , row_dict[row][row1indx-1], row_dict[bottom_key][row2indx]])

    '''The Top and Bottom Edges'''
    if (0, "u") in row_dict.keys():
        for i in range(len(row_dict[row])):
            point = row_dict[(0, "u")][i][0:2]
            sl = row_dict[(0, "u")][i][4] #generation number
            left_line =  [ [point, [point[0] + sl/2, point[1] + sl*sqrt(3)/2]] ]
            right_line = [ [[point[0] + sl/2, point[1] + sl*sqrt(3)/2]], [point[0] + sl, point[1]] ]

            outside_edges = np.append(outside_edges, [ left_line, row_dict[(0, "u")][i]])
            outside_edges = np.append(outside_edges, [ right_line, row_dict[(0, "u")][i]])

    blah = [] #sorry, coulldn't think of a name
    for term in row_dict.keys():
        blah.append(term[0]) #row number
    if (max(blah), "d") in row_dict.keys():
        point = row_dict[(max(blah), "d")][i][0:2]
        sl = row_dict[(max(blah), "d")][i][4] #generation number
        left_line =  [ [point, [point[0] + sl/2, point[1] - sl*sqrt(3)/2]] ]
        right_line = [ [[point[0] + sl/2, point[1] - sl*sqrt(3)/2]], [point[0] + sl, point[1]] ]

        outside_edges = np.append(outside_edges, [ left_line, row_dict[(max(blah), "d")][i]])
        outside_edges = np.append(outside_edges, [ right_line, row_dict[(max(blah), "d")][i]])

    return border_list, outside_edges #a collection of Borders
"""