from shutil import copyfile
from os import listdir
from os.path import isfile, join

# file = open('train.txt', 'r')

# lines = file.readlines()
paste_path = "people_dataset\\"

# for line in lines:
#     copy_path = "E:\Python\Scene_Description_Show_and_Tell\\" + line.strip("\n")
#     paste = paste_path + line.split("/")[-1].strip("\n")
#     copyfile(copy_path, paste)


onlyfiles = [paste_path + f for f in listdir(paste_path) if isfile(join(paste_path, f))]
onlyfiles.sort(reverse=True)
paths = '\n'.join(onlyfiles)

with open("train_people2.txt", 'w') as f:
    f.write(paths)
