from django.shortcuts import render
from django.shortcuts import render
from .forms import CarImageForm
from ultralytics import YOLO
import os
from django.conf import settings

model = YOLO(os.path.join(settings.BASE_DIR, 'best.pt'))

def classify_cars(request):
    result = None
    confidence = None
    img_url = None
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
            result = class_name
            
    else:
        form = CarImageForm()
    return render(request,'index.html',{'form':form, 'result':result,'confidence':confidence,'img_url':img_url})
