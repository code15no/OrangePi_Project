import os

root = "Vehicles-Open/"
dirs = ['train', 'valid', 'test']

for i, dir_name in enumerate(dirs):
    all_image_names = sorted(os.listdir(f"{root}{dir_name}/images/"))
    for j, image_name in enumerate(all_image_names):
        if (j % 2) == 0:
            file_name = image_name.split('.jpg')[0]
            os.remove(f"{root}{dir_name}/images/{image_name}")
            os.remove(f"{root}{dir_name}/labels/{file_name}.txt")