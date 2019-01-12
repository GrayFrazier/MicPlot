# MicPlot
! [alt text] (https://pbs.twimg.com/profile_images/909776348490665985/CGYKLZLV_400x400.jpg)
<img src = "https://pbs.twimg.com/profile_images/909776348490665985/CGYKLZLV_400x400.jpg">
A python tool for plotting .mic files which display data for polycrystalline materials.  Based in Carnegie Mellon University Physics/Material Science Department under Professor Robert M. Suter.

##Authors:
Grayson Frazier (Carnegie Mellon)
Doyee Byun (Carnegie Mellon/Vigina Tech)
He Liu (Carnegie Mellon)
Yufeng Shen (Carnegie Mellon)

## How to Use:
The interface is within **MicPlot.py**.  Simply run this program and follow the onscreen prompts to plot files.

There are two different file formats: square and triangular plots.


Use the PlotMic.py tool to plot the .mic file to display.  Upon doing so, the entire image will appear on your display.  To replot a specific grain, click on the said grain.  Doing so will show the average information about that area. To replot, simply press "enter" which will prompt a new window with the more specific grain.  Doing so will enhance the differences in the grain.

<--- Maybe add picture? -->
[logo]: https://pbs.twimg.com/profile_images/909776348490665985/CGYKLZLV_400x400.jpg


# micscanning

A valiant effort by Grayson Frazier to depart from his beloved Euler angles and embrace the harsh reality of misorientation angles.  This also now includes trying to add a slider in the replot.

Click on a voxel to gain its angle information.  Then, if desired, click enter to replot the data.  I am currently working on adding a slider to adjust what is replotted.
=======
# MicPlot
## pixelborders
=======

Branch to modify new HEDM pixel format and add borders.
=======

HEDM visualization tool

Interactive Version!
Parameters used for narrowing down grains are just the euler angles, and thus the selection method still has room for noise.

Color expansion is now based on rodrigues vectors.

Steps to run program:
1. Run python at home directory
2. type "import MicFileTool" + enter
3. type "MicFileTool.run()" + enter
4. Follow on-screen instructions
5. Get a beautiful plot!
>>>>>>> squareBorders
