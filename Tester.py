'''
Quick test to get stuff goin
https://stackoverflow.com/questions/21352580/matplotlib-plotting-numerous-disconnected-line-segments-with-different-colors
'''

import MicFileTool
import VoxelBorders
from matplotlib import collections as mc
sw, snp = MicFileTool.read_mic_file("395z0.mic.LBFS")
border_list, outside_edges = VoxelBorders.make_borders(snp,sw)

border_lines = []
edges = []
for border in border_list:
    border_lines.append(border[0:2])
for edge in outside_edges:
    edges.append(edge[0:2])
print(border_lines[0])
print(edges[0])

border_collecton = mc.LineCollection(border_lines[0])
edge_collection = mc.LineCollection(edges[0])
fig = plt.figure()
ax_border = fig.add_subplot()
ax.add_collection(border_collecton)
ax.add_collection(edge_collection)
plt.show()
