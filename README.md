# Crop-Namer

I built this program early 2020 to assist my workflow at my job.  I was hired to scan and archive maps for the Bellefonte Boro Office in Bellefonte, PA.  My duties consisted of physically scanning historical maps, then renaming and organizing them within a database.  I realized that the computer dependant part of the job, manually renaming files based on their page numbers, could be automated using image recognition and computer vision.

Crop-Namer seeks utilize all the open-source resources possible in order to provide functionality for users to quickly rename files.

This program renames image files in bulk, and is intended for images with similar layouts (like series of architectural drawings).  It first asks the user to choose a folder.  It opens the first file with a name beginning with "scan", and prompts the user to box the area of the page number/intended title.   It then crops the given area and names it any text inside, doing the same in the same area to the other images beginning with the word "scan" in the folder.

Currently in progress is a calibration system for images that may not be aligned properly.

### For Potential Users

This was built on Python 3.7; functionality on other versions is untested.

You may have to manually install each module using PIP, either on your entire device or on a venv (virtual environment).  These modules/libraries are listed in setup.py.

Once you have these loaded, you should be able to run source.py.
If not, using source.py as a module, you will have to create a root object with Tkinter, then run the class CropNamer.

It would look something like this:
 ```python
 root = Tk() `
 CropNamer(root)
 ```

If this fails, feel free to contact me or analyze the code yourself if you feel so inclined.
