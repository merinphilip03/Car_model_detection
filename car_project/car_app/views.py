from django.shortcuts import render
from django.conf import settings
from .forms import CarImageForm
from ultralytics import YOLO
import os
from PIL import Image, ImageEnhance
from transformers import pipeline
import torch
import re
import easyocr
import numpy as np

model = YOLO(os.path.join(settings.BASE_DIR, 'best.pt'))
pipe = pipeline("object-detection",
                model="nickmuchi/yolos-small-finetuned-license-plate-detection")
reader = easyocr.Reader(['en'])

def preprocess_text(text):
    text = re.sub(r'[^A-Za-z0-9]', '', text)
    return text.upper()

def postprocess_plate(text):
    text = preprocess_text(text)
    fixed = ''
    for i, ch in enumerate(text):
        if i < 2: 
            fixed += _correct_to_letter(ch)
        elif i < 4:
            fixed += _correct_to_digit(ch)
        elif i < len(text) - 4:
            fixed += _correct_to_letter(ch)
        else:
            fixed += _correct_to_digit(ch)

    if re.match(r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$', fixed):
        return fixed

    return text 

def _correct_to_letter(ch):
    digit_to_letter = {
        '0': 'O', '1': 'I', '2': 'Z', '5': 'S', '6': 'G', '8': 'B', '4': 'A'
    }
    return digit_to_letter.get(ch, ch)

def _correct_to_digit(ch):
    letter_to_digit = {
        'O': '0', 'I': '1', 'Z': '2', 'S': '5', 'B': '8', 'Q': '0', 'G': '6', 'A': '4'
    }
    return letter_to_digit.get(ch, ch)

def enhance_plate_image(image: Image.Image) -> Image.Image:
    image = image.convert('L')
    width, height = image.size
    image = image.resize((width * 3, height * 3), Image.LANCZOS)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    return image


def classify_cars(request):
    results = None
    confidence = None
    img_url = None
    number = None

    if request.method == 'POST':
        form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            uploaded_img = request.FILES['image']
            img_path = doc.image.path
            img_url = doc.image.url

            prediction = model(img_path)[0]
            class_id = int(prediction.probs.top1)
            class_name = model.names[class_id]
            confidence = round(prediction.probs.top1conf.item() * 100, 2)
            results = class_name

            outputs = pipe(img_path)
            if outputs:
                top_box = max(outputs, key=lambda x: x['score'])
                box = top_box['box']
                img = Image.open(img_path).convert("RGB")
                crop_img = img.crop((box['xmin'], box['ymin'], box['xmax'], box['ymax']))

                enhanced_img = enhance_plate_image(crop_img)

                cropped_plate_path = os.path.join(settings.MEDIA_ROOT, "cropped_plate.jpg")
                enhanced_img.save(cropped_plate_path)

                crop_np = np.array(enhanced_img)
                ocr_results = reader.readtext(crop_np, detail=0)

                filtered = [preprocess_text(txt) for txt in ocr_results
                            if "IND" not in txt.upper() and len(preprocess_text(txt)) >= 8]

                if filtered:
                    raw_number = filtered[0]
                    number = postprocess_plate(raw_number)
                else:
                    number = "No valid plate number detected."
            else:
                number = "No license plate detected."
    else:
        form = CarImageForm()

    return render(request, 'index.html', {
        'form': form,
        'results': results,
        'confidence': confidence,
        'img_url': img_url,
        'number': number
    })
