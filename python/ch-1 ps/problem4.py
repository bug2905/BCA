#display list all files and directories in spacified path using os 
import os

#specify the directory you want to list 
directory = '/kushal/sem5'

#list all files and directories in spacified path
content = os.listdir(directory)

# print each file and directory name 
for item in content:
    print(item)
