import os
import shutil
import random

# Paths
BASE_DIR = "car_dataset_yolo"
IMG_SRC = os.path.join(BASE_DIR, "images", "all")
LBL_SRC = os.path.join(BASE_DIR, "labels", "all")
IMG_TRAIN = os.path.join(BASE_DIR, "images", "train")
IMG_VAL = os.path.join(BASE_DIR, "images", "val")
LBL_TRAIN = os.path.join(BASE_DIR, "labels", "train")
LBL_VAL = os.path.join(BASE_DIR, "labels", "val")

# Create output folders
os.makedirs(IMG_TRAIN, exist_ok=True)
os.makedirs(IMG_VAL, exist_ok=True)
os.makedirs(LBL_TRAIN, exist_ok=True)
os.makedirs(LBL_VAL, exist_ok=True)

# Load all image filenames
all_images = [f for f in os.listdir(IMG_SRC) if f.endswith(('.jpg', '.jpeg', '.png'))]
random.shuffle(all_images)

# Train/val split (80/20)
split_idx = int(0.8 * len(all_images))
train_images = all_images[:split_idx]
val_images = all_images[split_idx:]

def move_data(image_list, img_dst, lbl_dst):
    for img_file in image_list:
        label_file = img_file.rsplit('.', 1)[0] + ".txt"
        shutil.copy(os.path.join(IMG_SRC, img_file), os.path.join(img_dst, img_file))
        shutil.copy(os.path.join(LBL_SRC, label_file), os.path.join(lbl_dst, label_file))

move_data(train_images, IMG_TRAIN, LBL_TRAIN)
move_data(val_images, IMG_VAL, LBL_VAL)

# Load class names
with open("class_list.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# Create data.yaml
yaml_content = f"""train: {BASE_DIR}/images/train
val: {BASE_DIR}/images/val

nc: {len(class_names)}
names: {class_names}
"""

with open("data.yaml", "w") as f:
    f.write(yaml_content)

