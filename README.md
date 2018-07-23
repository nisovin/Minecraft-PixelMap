Minecraft PixelMap
====================

This is a python script that generates an overhead map for Minecraft with one pixel per block, similar to the in-game map system.
This was created for use with 1.13, since other mapping software has not been updated. It **only** works with maps that have
been fully converted to the 1.13 format (or were generated in 1.13 in the first place).

The script generates one image per region. Subsequent runs will only generate new images if the region file has been updated.
It also generates a javascript file that contains an array of all the images. This can 
then be used in a webpage (the example index.html uses this). These could theoretically be used with something like Leaflet,
but I haven't bothered to try it.

This script is provided as-is. It was created for my specific server, but should work in general. The code is messy, 
the result is imperfect, but it's good enough for my purposes right now.

Setup
-----

You'll need to install Python. Then you will need the [NBT library by twoolie](https://github.com/twoolie/NBT).
The easiest way to get this is to use PIP (```pip install NBT```).

You will also want to change the path variables at the top of the python script.