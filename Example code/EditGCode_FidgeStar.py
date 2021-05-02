#code to print from new layer
#tailered to Fidget Star project
import os
from decimal import Decimal

lineNum = 1
debug = 0
print("Starting EditGCode...\n")
#Start Edit**********************
#DO NOT EDIT OUTSIDE THIS BLOCK 

#replace Fidget-Star with your code file
inFile = open("Fidget-Star(HALF).gcode.txt","r")

#startLine is the line following: "G28 X Y; Home"
startLine = 22;

#endLine is the line number with ";End of Gcode" at the end of your file, do not make it the last line
#as it might edit anything in the settings that has a "z" in it
endLine = 31720;

#Offset will be the layer hieght in the layer before your start layer. You will have to find this in the original
#code, as the edited file should have this value deleted. Reffer to the ReadMe to find this value
offset = Decimal('17.7')

#End Edit******************************

if endLine == 0 or startLine == 0 or offset == 0 :
    print("Error: please edit python script\n")
    exit(0)

outFile = open("output.gcode", "w")

oldvalue = offset
for i in inFile:
    
    if lineNum > startLine and lineNum < endLine:
   
        find = i.find("Z")
        if find >= 0: #if "Z" is in the line, edit the Z value
            if (debug):
                print("Found Z in line: ")
                print(i)
            currentvalue = Decimal(i[(find + 1):])
            currenthieght = currentvalue - oldvalue
            oldvalue = currentvalue
            
            if debug:
                print("\nCurrent hieght: ")
                print(currenthieght)
                print("currentvalue")
                print(currentvalue)
                print("Offset")
                print(offset)
            
            
            newvalue = currentvalue - offset
            
            if debug:
                print("New Value: ")
                print(newvalue)
           
            replace = i[:find] + "Z" + str(newvalue) +"\n"
            i = replace
            
            
    outFile.write(i)
    lineNum = lineNum + 1

print("Program Finsihed, exiting ...")    