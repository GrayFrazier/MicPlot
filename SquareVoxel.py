'''
Code By Doyee Byun
Organized/Modified by Grayson Frazier

Basic functions for plotting square format
'''
class SquarePoint():
    def __init__(self, xi, yi):
        self.x = xi
        self.y = yi
        self.coords = (xi,yi)
        self.up = (xi,yi+1)
        self.right = (xi+1,yi)
        self.down = (xi,yi-1)
        self.left = (xi-1,yi)
        self.up_blocked = False
        self.right_blocked = False
        self.down_blocked = False
        self.left_blocked = False
        self.angles = [0.0,0.0,0.0]
        return

    def block_up(self):
        self.up = None
        self.up_blocked = True
        return

    def block_right(self):
        self.right = None
        self.right_blocked = True
        return

    def block_down(self):
        self.down = None
        self.down_blocked = True
        return

    def block_left(self):
        self.left = None
        self.left_blocked = True
        return

    def set_angles(self, angles):
        self.angles = angles

    def check_points(self,data,xlim,ylim,misor_thresh):
        upx,upy = self.up
        rightx,righty = self.right
        downx,downy = self.down
        leftx,lefty = self.left
        if upx < 0 or upx > xlim or upy < 0 or upy > ylim:
            self.block_up()
        if rightx < 0 or rightx > xlim or righty < 0 or righty > ylim:
            self.block_right()
        if downx < 0 or downx > xlim or downy < 0 or downy > ylim:
            self.block_down()
        if leftx < 0 or leftx > xlim or lefty < 0 or lefty > ylim:
            self.block_left()

        angles = np.array([self.angles])
        if not self.up_blocked:
            upangles = np.array([[data[upx,upy,3],data[upx,upy,4],data[upx,upy,5]]])
            up_misor = RotRep.MisorinEulerZXZ(angles,upangles)
            if up_misor > misor_thresh:
                self.block_up()
        if not self.right_blocked:
            rightangles = np.array([[data[rightx,righty,3],data[rightx,righty,4],data[rightx,righty,5]]])
            right_misor = RotRep.MisorinEulerZXZ(angles,rightangles)
            if right_misor > misor_thresh:
                self.block_right()
        if not self.down_blocked:
            downangles = np.array([[data[downx,downy,3],data[downx,downy,4],data[downx,downy,5]]])
            down_misor = RotRep.MisorinEulerZXZ(angles,downangles)
            if down_misor > misor_thresh:
                self.block_down()
        if not self.left_blocked:
            leftangles = np.array([[data[leftx,lefty,3],data[leftx,lefty,4],data[leftx,lefty,5]]])
            left_misor = RotRep.MisorinEulerZXZ(angles,leftangles)
            if left_misor > misor_thresh:
                self.block_left()

def square_angle_limiter(x,y, data, coords, misor_thresh=1.0):
    points = []
    xi = coords[0]
    yi = coords[1]
    angles = []
    angles.append(data[xi,yi,3])
    angles.append(data[xi,yi,4])
    angles.append(data[xi,yi,5])
    current_point = SquarePoint(xi,yi)
    current_point.set_angles(angles)
    current_point.check_points(data,x,y,misor_thresh)
    points.append(current_point)
    if not current_point.up_blocked:
        points = recursive_limiter(x,y,data,points,[xi,yi+1],misor_thresh)
    if not current_point.right_blocked:
        points = recursive_limiter(x,y,data,points,[xi+1,yi],misor_thresh)
    if not current_point.down_blocked:
        points = recursive_limiter(x,y,data,points,[xi,yi-1],misor_thresh)
    if not current_point.left_blocked:
        points = recursive_limiter(x,y,data,points,[xi-1,yi],misor_thresh)
    return points

def recursive_limiter(x,y,data,points,coords,misor_thresh):
    new_point = None
    xi = coords[0]
    yi = coords[1]
    for i in range(0,len(points)):
        if coords[0] == points[i].x and coords[1] == points[i].y:
            new_point = points[i]
            return points
    if new_point is None:
        new_point = SquarePoint(coords[0],coords[1])
        new_angles = []
        new_angles.append(data[xi,yi,3])
        new_angles.append(data[xi,yi,4])
        new_angles.append(data[xi,yi,5])
        new_point.set_angles(new_angles)
        points.append(new_point)
    new_point.check_points(data,x,y,misor_thresh)
    if not new_point.up_blocked:
        points = recursive_limiter(x,y,data,points,[xi,yi+1],misor_thresh)
    if not new_point.right_blocked:
        points = recursive_limiter(x,y,data,points,[xi+1,yi],misor_thresh)
    if not new_point.down_blocked:
        points = recursive_limiter(x,y,data,points,[xi,yi-1],misor_thresh)
    if not new_point.left_blocked:
        points = recursive_limiter(x,y,data,points,[xi-1,yi],misor_thresh)
    return points



def plot_square_mic(SquareMic,squareMicData, minHitRatio,coords, misor_thresh):
    '''
    plot the square mic data
    image already inverted, x-horizontal, y-vertical, x dow to up, y: left to right
    :param squareMicData: [NVoxelX,NVoxelY,10], each Voxel conatains 10 columns:
            0-2: voxelpos [x,y,z]
            3-5: euler angle
            6: hitratio
            7: maskvalue. 0: no need for recon, 1: active recon region
            8: voxelsize
            9: additional information
    :return:
    '''
    assert(len(coords) == 0 or len(coords) == 2), "Please enter the correct number of coordinates"
    anglelim = not (coords == [])
    angles = []
    fig, ax = plt.subplots()
    indx = []
    points = []
    smdCopy = squareMicData.copy()
    (x,y,z) = squareMicData.shape
    if anglelim:
        angles.append(squareMicData[coords[0],coords[1],3])
        angles.append(squareMicData[coords[0],coords[1],4])
        angles.append(squareMicData[coords[0],coords[1],5])
        points = square_angle_limiter(x,y,smdCopy,coords,misor_thresh)
        indx = index_from_points(points)
        for i in range(0,x):
            for j in range(0,y):
                if not (i,j) in indx:
                    smdCopy[i,j,6] = 0.0
                    smdCopy[i,j,3] = angles[0]
                    smdCopy[i,j,4] = angles[1]
                    smdCopy[i,j,5] = angles[2]
    mat = RotRep.EulerZXZ2MatVectorized(smdCopy[:,:,3:6].reshape([-1,3])/180.0 *np.pi )
    quat = np.empty([mat.shape[0],4])
    rod = np.empty([mat.shape[0],3])
    colors, maxangs, minangs = set_color_range_sq(smdCopy,x,y,indx,mat,quat,rod,anglelim)
    hitRatioMask = (smdCopy[:,:,6]>minHitRatio)[:,:,np.newaxis].repeat(3,axis=2)
    #img = ((colors + np.array([1, 1, 1])) / 2).reshape([squareMicData.shape[0],squareMicData.shape[1],3]) * hitRatioMask
    img = (colors).reshape([squareMicData.shape[0],squareMicData.shape[1],3]) * hitRatioMask
    # make sure display correctly
    #img[:,:,:] = img[::-1,:,:]
    img = np.swapaxes(img,0,1)
    minX, minY = smdCopy[0,0,0:2]*1000
    maxX, maxY = smdCopy[-1,-1,0:2]*1000
    #print(minX,maxX, minY,maxY)
    if anglelim:
        (xi_first,yi_first) = indx[0]

        xmin = smdCopy[xi_first,yi_first,0]
        xmax = smdCopy[xi_first,yi_first,0]
        ymin = smdCopy[xi_first,yi_first,1]
        ymax = smdCopy[xi_first,yi_first,1]
        for (xi,yi) in indx:
            if smdCopy[xi,yi,0] <= xmin:
                xmin = smdCopy[xi,yi,0]
            if smdCopy[xi,yi,0] >= xmax:
                xmax = smdCopy[xi,yi,0]
            if smdCopy[xi,yi,1] <= ymin:
                ymin = smdCopy[xi,yi,1]
            if smdCopy[xi,yi,1] >= ymax:
                ymax = smdCopy[xi,yi,1]
        if abs(xmax-xmin) > abs(ymax-ymin):
            side_length = abs(xmax-xmin)
        else:
            side_length = abs(ymax-ymin)
        side_length = side_length / smdCopy[0,0,8] * 10
        xmin = xmin / smdCopy[0,0,8] * 10
        ymin = ymin / smdCopy[0,0,8] * 10
        ax.set_xlim([xmin -10 ,xmin + side_length + 10])
        ax.set_ylim([ymin -10 ,ymin + side_length + 10])
    print("-------------------------------------------------")
    print("MaxRod (R,G,B): ", maxangs)
    print("MinRod (R,G,B): ", minangs)
    ax.imshow(img,origin='lower',extent=[minX,maxX,minY,maxY])

    plt.title('orientation in um')
    voxels = SquareVoxelClick(fig, squareMicData,SquareMic,minHitRatio,misor_thresh)
    voxels.connect()
    plt.show()

class SquareMic():
    def __init__(self,squareMicData=None):
        self.squareMicData = squareMicData

    def load(self,fName):
        self.squareMicData = np.load(fName)

    def plot_orientation(self, coords=[], minHitRatio=0.5, misor_thresh=1.0):
        plot_square_mic(self,self.squareMicData, minHitRatio, coords, misor_thresh)

    def plot_hit_ratio(self):
        img = np.swapaxes(self.squareMicData[:,:,6], 0, 1)
        plt.imshow(img, origin='lower')
        plt.colorbar()
        plt.show()
