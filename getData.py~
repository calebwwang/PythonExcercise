import urllib
import os

# get data
f = urllib.urlopen("https://cooper.edu/")
s = f.read()
f.close()

# write data
outputFile = open("output.htm", "w")
outputFile.write(s)
outputFile.close()

# run cmd prompt command to open the html file
command=" output.htm "
os.system(command)

