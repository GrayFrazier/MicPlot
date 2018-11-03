'''
Quick test to get stuff goin
https://stackoverflow.com/questions/21352580/matplotlib-plotting-numerous-disconnected-line-segments-with-different-colors
https://matplotlib.org/examples/pylab_examples/line_collection2.html
'''

import MicFileTool
import VoxelBorders
import matplotlib.pyplot as plt
from matplotlib import collections as mc
sw, snp = MicFileTool.read_mic_file("395z0.mic.LBFS")
border_list, outside_edges = VoxelBorders.make_borders(snp,sw)

border_lines = []
edges = []
for border in border_list:
    border_lines.append(border[0])
for edge in outside_edges:
    edges.append(edge[0])

i=2




border_collecton = mc.LineCollection(border_lines)
edge_collection = mc.LineCollection(edges)
ax = plt.axes()
ax.add_collection(border_collecton)
#ax.add_collection(edge_collection)

fig = plt.gcf()
ax.set_xlim((-1,1))
ax.set_ylim((-1,1))
plt.show()
