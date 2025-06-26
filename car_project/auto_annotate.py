import os
from PIL import Image

# INPUT: your dataset folder
SOURCE_DIR = "car_images"
OUTPUT_DIR = "car_dataset_yolo"

# Default box size: 80% of image (centered)
DEFAULT_BOX_RATIO = 0.8

# Step 1: Class name to ID mapping
class_names = sorted([folder for folder in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, folder))])
class_to_id = {name: idx for idx, name in enumerate(class_names)}

# Save class list for later YOLO training
with open("class_list.txt", "w") as f:
    for name in class_names:
        f.write(name + "\n")

# Step 2: Loop through all images
for class_name in class_names:
    class_dir = os.path.join(SOURCE_DIR, class_name)
    for img_name in os.listdir(class_dir):
        if img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(class_dir, img_name)

            try:
                image = Image.open(img_path)
                w, h = image.size

                # Convert image mode if needed (JPEG doesn't support RGBA or P)
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")

                # Create output directories
                img_out_dir = os.path.join(OUTPUT_DIR, "images", "all")
                lbl_out_dir = os.path.join(OUTPUT_DIR, "labels", "all")
                os.makedirs(img_out_dir, exist_ok=True)
                os.makedirs(lbl_out_dir, exist_ok=True)

                # Save image
                img_out_name = f"{class_name}_{img_name}".replace(" ", "_")
                img_out_path = os.path.join(img_out_dir, img_out_name)
                image.save(img_out_path)

                # Create label
                box_w, box_h = DEFAULT_BOX_RATIO * w, DEFAULT_BOX_RATIO * h
                x_center = w / 2
                y_center = h / 2

                # Normalize
                x_c = x_center / w
                y_c = y_center / h
                bw = box_w / w
                bh = box_h / h

                label = f"{class_to_id[class_name]} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n"

                lbl_out_name = img_out_name.replace(".jpg", ".txt").replace(".png", ".txt")
                lbl_out_path = os.path.join(lbl_out_dir, lbl_out_name)
                with open(lbl_out_path, "w") as f:
                    f.write(label)

            except Exception as e:
                print(f" Failed to process {img_path}: {e}")
                
