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
    [[x1,y1], [x2,y2], left/up, right/down]
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
