
import requests as req
import io
from PIL import Image
import os
from sources import IMAGE_DOWNLOAD_PATH, LABEL_SAVE_PATH

def generate_label(category, file_num, cat_idx):
    file_name = f"{category}_{file_num}.txt"
    check_path = f"{LABEL_SAVE_PATH}/{category}"
    file_path = f"{LABEL_SAVE_PATH}/{category}/{file_name}"

    line_to_write = f'{cat_idx} 0.5 0.5 1.0 1.0'

    if not os.path.exists(check_path):
        os.makedirs(check_path)
    with open(file_path, 'w') as file:
        file.write(line_to_write)
    print("Written label: ", file_name)

def download_image(url, category, file_num, cat_idx):
    file_name = f"{category}_{file_num}.jpg"
    image_content = req.get(url).content
    image_file = io.BytesIO(image_content)
    pil_image = Image.open(image_file)

    if len(pil_image.getbands()) == 3:
        check_path = f"{IMAGE_DOWNLOAD_PATH}/{category}"
        file_path = f"{IMAGE_DOWNLOAD_PATH}/{category}/{file_name}"
        if not os.path.exists(check_path):
            os.makedirs(check_path)
        with open(file_path, "wb") as f:
            pil_image.save(f)
        
        print("Downloaded: ", file_name)
        try:
            generate_label(category, file_num, cat_idx)
        except Exception as e:
            print(f"🔵🔵 An error occurred while writing labels ({file_name})! 🔵🔵")
    else:
        print("🔵🔵 An image with alpha channel found, hence discarding it!! 🔵🔵")

