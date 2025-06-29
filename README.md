# Car_model_detection & License Plate Reader

A Django-based web application that uses **YOLOv8** to classify car models and detect license plates from uploaded images. It then performs **OCR** using **EasyOCR** and refines the detected text with custom postprocessing to return cleaned-up plate numbers.

##  Demo

Upload a car image, and the app:
- Classifies the car model (e.g., Mahindra Thar, Maruti Swift)
- Detects and crops the license plate
- Enhances it and extracts the plate number using OCR

<img width="1470" alt="image" src="https://github.com/user-attachments/assets/a357436a-7731-4c86-b78e-ff6f69624782" />

<img width="1470" alt="image" src="https://github.com/user-attachments/assets/94dd5c2f-e86e-49d8-b11d-425ad13c2541" />

<img width="1470" alt="image" src="https://github.com/user-attachments/assets/c774c032-a5c6-41b6-9b0a-75287e2542c6" />

## Features

-  **Car model classification** using a custom-trained YOLOv8 model (`best.pt`)
-  **License plate detection** using HuggingFace Transformers (YOLOS-small)
-  **OCR** with EasyOCR
-  Smart **postprocessing** to correct common OCR errors (e.g., "0" to "O")
-  **Django web interface** for image upload and result display

## Tech Stack

| Tech        | Description                     |
|-------------|---------------------------------|
| Django      | Python web framework            |
| YOLOv8      | Car model classification        |
| Transformers| License plate detection (YOLOS) |
| EasyOCR     | Optical Character Recognition   |
| Pillow      | Image enhancement and cropping  |
| HTML/CSS    | Basic styling with templates    |

## Project Structure

Car_model_detection/
├── car_project/ 
│   ├── views.py                
│   ├── urls.py                 
│   ├── templates/
│   │   └── index.html          
│   ├── static/
│   │   └── css/style.css       
│   └── forms.py                
│
├── media/                      
│
├── best.pt                    
├── manage.py                   
├── db.sqlite3                  
├── requirement.txt             
├── README.md                   
└── .gitignore   

## Installation

Clone the repository and set it up locally:
   - git clone https://github.com/merinphilip03/Car_model_detection.git
   - cd Car_model_detection

Create and activate virtual environment
   - python -m venv env
   - source env/bin/activate  # On Windows: env\Scripts\activate

Install dependencies
   - pip install -r requirement.txt

Run Django migrations (if needed)
   - python manage.py migrate

Run the server
   - python manage.py runserver

## How It Works

- Upload an image
- YOLOv8 model classifies the car
- YOLOS-small detects the license plate bounding box
- Pillow crops + enhances the plate
- EasyOCR performs OCR on the plate
- Postprocessor cleans and formats the text

## Dependencies

All dependencies are listed in requirement.txt, but main ones include:

- Django
- ultralytics (YOLOv8)
- transformers
- torch
- Pillow
- easyocr
- numpy

## Author

Merin Philip,
 GitHub,
 Email: merinphilip3304@gmail.com
