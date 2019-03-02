import json

from drive.drive_api import Drive
import matplotlib.pyplot as plt

try:
    path = "paths.txt"
    d = Drive()
    annotations = d.load_file()

    image_paths = open(path, 'r').readlines()

    for i in range(len(image_paths)):
        img = plt.imread(image_paths[i].strip("\n"))
        plt.imshow(img)
        plt.show()
        caption = input("Enter Caption: ")
        if caption == "s":
            continue
        elif caption == "q":
            paths = ''.join(image_paths[i:])
            with open(path, 'w') as f:
                f.write(paths)
            with open('drive\\annotations.json', 'w') as outfile:
                json.dump(annotations, outfile)
            d.upload_file()
            break
        else:
            img_dict = {"image_id": int(image_paths[i].split('\\')[-1].split('_')[-1].split('.')[0]),
                        "caption": caption}
            annotations['annotations'].append(img_dict)
            paths = ''.join(image_paths[i:])
            with open(path, 'w') as f:
                f.write(paths)
            with open('drive\\annotations.json', 'w') as outfile:
                json.dump(annotations, outfile)


except FileNotFoundError as error:
    print(error)