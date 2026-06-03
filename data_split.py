# Split the dataset, place the original dataset in dataset_org, and generate the processed data in dataset
# It is necessary to use one's own dataset to establish  dataset_org
import os
import shutil
import random

# division ratio
split_rate = [0.8, 0.1, 0.1]
split_names = ["train", "valid", "test"]

split_rate[1] = sum(split_rate[:2])

#
shuffle = True

def replace_expand_name(file_name, ex_name):
    return ".".join(file_name.split(".")[:-1] + [ex_name])

if os.path.exists("dataset"):
    shutil.rmtree("dataset")
os.makedirs("dataset")
for name in split_names:
    os.makedirs(os.path.join("dataset", name, "images"))
    os.makedirs(os.path.join("dataset", name, "labels"))

image_folder = r"dataset_org/images"   #Change one's own path
label_folder = r"dataset_org/labels"    #Change one's own path

image_files = os.listdir(image_folder)
if shuffle == True:
    random.shuffle(image_files)
label_files = [replace_expand_name(name, 'txt') for name in image_files]

def write_files(image_files, label_files, split):
    for image_file, label_file in zip(image_files, label_files):
        shutil.copy(os.path.join(image_folder, image_file), os.path.join("dataset", split, "images", image_file))
        shutil.copy(os.path.join(label_folder, label_file), os.path.join("dataset", split, "labels", label_file))

data_len = len(image_files)
write_files(image_files[:int(split_rate[0]*data_len)], label_files[:int(split_rate[0]*data_len)], split_names[0])
write_files(image_files[int(split_rate[0]*data_len):int(split_rate[1]*data_len)], label_files[int(split_rate[0]*data_len):int(split_rate[1]*data_len)], split_names[1])
write_files(image_files[int(split_rate[1]*data_len):], label_files[int(split_rate[1]*data_len):], split_names[2])


