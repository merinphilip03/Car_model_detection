from icrawler.builtin import GoogleImageCrawler

def download_car_image(make_model, num=20):
    google_crawler = GoogleImageCrawler(storage={'root_dir': f'car_images/{make_model.replace(" ", "_")}'})
    google_crawler.crawl(keyword=make_model, max_num=num)

if __name__ == '__main__':
    car_names = ["Hyundai Creta 2025 exterior","Hyundai Creta 2024 exterior", 
                 "Maruti Swift 2025 exterior", "Maruti Swift 2024 exterior",
                 "Mahindra Thar 2025 exterior","Mahindra Thar 2024 exterior",
                 "Jeep Wrangler 2025 exterior","Jeep Wrangler 2024 exterior"]

    for car in car_names:
        download_car_image(car, 20)
