# Resume3Dprint
This is a python script to edit the G-code on a 3D print that has stopped anywhere in the print. Go to ReadMe for use and limitations.

## About and Limitations
This solution may not be right for all problems with continuing a stopped print and may need some adjustment for your set up. I am using Cura to splice my code for an Ender 3 pro printer. The code I am editing has Ender 3 custom start G-code, this should work for other G-codes, but may need slight adjustments in your start point for deleting code.  
When looking for a solution, this tutorial was the closest one I could find for restarting a print that stopped at any layer height:  
https://forums.creality3dofficial.com/save-print-from-airprinting/  
However, this solution requires that your printer did not turn off since the start of the print. This is required because of where your printer thinks the Z height is, when it turns off, it will think it is at 0, rather than the height the print stopped at, making all the G-code heights relative to the stop point, rather than the printing bed.
This python script is the first version in an attempt to make a more generalized solution for stopped prints when your printer has turned off. It effectively changes all the Z heights so that the printer can continue from where it is.

You will need to figure out what layer your print stopped at, we will be starting again at that layer, however it will be printing the entire layer again. I have found that it does not seem to affect the print too much.

- Adaptive layer height: This code should work with adaptive layer height and consistent layer height.

## Usage
This solution requires you to edit the G code and modify the python script before running.


## Editing the Gcode
1. Save a copy of your g-code that does not get edited, in case you have to start over.
2. Fixing the auto home. This line of code will be found very early in your G code, if there are multiple, just consider the first one, the following ones will be deleted later on. This will make sure the extruder doesn’t go back to the bed height and crush your print.  

Change:
```gcode
G28 ; Home all axes
```
To:  
```gcode
G28 X Y; Home
```
3. Finding the layer to resume print from. To find what layer the print stopped at, I used a caliper to measure how tall the print is. For the Fidget Star example, it was 17.8mm. You can also use a camera to count the layers that it has printed if you have an obvious point to start from. It is important to have the print start from the right layer.
This height measurement correlated to a height layer perfectly in my code, but if yours does not, use the layer that is closest to the Z value below this height. 
For the Fidget Star, this was layer 176. Keep in mind that the Z value for a layer will be above the layer number in the code.

- Line Offset: The offset value in your modified python script will be the layer height **before** your desired start layer. This will be the Z value above the previous layer. For the Fidget Star this was layer 175 with corresponding Z value 17.7.

4. Delete G code.
We no longer need the startup processes, such as printing the line and skirt that Cura adds, and the layers that have already printed. So we will be deleting a large chunk of G-code. The start point will be immediately after the "G28 X Y; Home" that was just edited.
The End point will be before the layer we want to start at. For the fidget-Star Example, this was layer 176, we want to keep some of the code before the line:
```gcode
;Layer:176
```
because it changes the Z value before the layer label. Looking at the gcode, the Z value is changed right after the previous label :
```gcode
;MESH:NONMESH"
```
So we will make the end point right before this label, which was line #299199

## Editing the Python script
There are 4 values in the python script you will need to change to fit your print. 
On line 13, replace “YourPrint” with the name of your gcode file.
On line 16, make startLine equal the line number that the following line is on: 
```gcode
G28 X Y; Home
```  
Line 20 is the last line you want the script to run on. In your gcode, find the line that has:
```gcode
;End of Gcode
```
The line number for this code is the value you will place here. This is so the script does not edit any end of file settings.  
Line 24 will be the offset value from step 3 in Editing the gcode.  

## Resuming the Print
Make sure that EditGCode.py is in the same folder as your gcode and run the python script. If you do not get "Program finished, exiting ..." after running it, the output file may be incomplete. Once you are ready to resume the print, remember to clean the nozzle of any material that comes out as the printer is warming up, as this may catch on your print and break it.
