
from logging import exception
from selenium import webdriver
import time
import re
import csv

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--disable-dev-shm-usage")

user_name = input("Enter your username >>")

password = input("Enter your password >>")

query = input("Enter Image Types, If Type is more than 1 word seperate with a + sign >>> ")

def scrap(arg):
    with webdriver.Chrome(executable_path="./Driver/chromedriver", options=chrome_options) as driver:

        search_values = arg

        image_links = []

        driver.get("https://wallhaven.cc/login")

        time.sleep(1)

        driver.execute_script("document.getElementById('username').value = " + user_name)

        driver.execute_script("""document.querySelectorAll("input[name='password']")[0].value = """ + password)

        time.sleep(1)

        driver.execute_script("document.getElementsByClassName('button big-green')[0].click()")

        time.sleep(2)
        
        for search in search_values.split(' '):

            if search == "" or search == " " or "\n" in search:
                continue

            driver.get(f"https://wallhaven.cc/search?categories=100&purity=100&sorting=date_added&order=asc&page=2")

            time.sleep(3) 

            last_height = driver.execute_script("return document.body.scrollHeight")

            page = 0

            while True:

                # Scroll down to the bottom.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load the page.
                time.sleep(3)

                # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                # stop scrolling when at the bottom of the page or page hits 60
                if (new_height == last_height) or (page == 35):

                    break
                
                page += 1
                last_height = new_height

                print(f"On page " + str(page) + "/ 35", flush=True)

            images = driver.execute_script("return document.querySelectorAll('img.loaded')")

            image_dimensions_raw = driver.execute_script("return document.getElementsByClassName('wall-res')")
            
            image_dimensions = []

            counter = 0

            inner_text = []

            amount_of_images_left = len(images)
            processed_image = 1

            for i in images:

                try:
                    time.sleep(0.7)
                    
                    driver.execute_script(f"document.getElementsByClassName('jsAnchor thumb-tags-toggle tagged')[{counter}].click()")

                    time.sleep(1.4)

                    image_id = i.get_attribute('src').split('/')[-1].split('.jpg')[0]

                    tag_data = driver.execute_script(f"return document.getElementsByClassName('thumb-tags tags-{image_id}')[0]")
                    

                    if tag_data is None:

                        print("Skipping due to no meta data", flush=True)
                        counter += 1
                        
                    else:

                        image_links.append(i.get_attribute('src'))
                        inner_text.append(str(tag_data.get_attribute('innerText')))
                        image_dimensions.append(image_dimensions_raw[counter].get_attribute('innerHTML'))
                        print(f"Processing meta data on image " + str(processed_image) + " / " + str(amount_of_images_left), flush=True)
                        processed_image += 1
                        counter += 1
                
                except:
                    
                    break

                
            buildObject(image_links, inner_text, image_dimensions)

            image_links = []
            inner_text = []
            image_dimensions = []
            counter = 0
            tag_counter = 0
            processed_image = 1
            
            page = 0

            time.sleep(20)

def buildObject(images, tags, dimensions):

    items = []

    with open(f'./database.csv', 'a', encoding='utf-8') as output_csv:

        fields = ["full-image", "label-image", "tags", "height", "width", "clicks"]

        output_writer = csv.DictWriter(output_csv, fieldnames=fields)

        #output_writer.writeheader()

        print(len(tags), flush=True)

        print(len(images), flush=True)

        for img in range(len(images)):

            full_image = re.sub(r'\n', '', re.sub(r'small', 'full', re.sub(r'th.', 'w.', images[img]))).split('/')

            full_image[5] = 'wallhaven-' + full_image[5]

            full_image_joined = '/'.join(full_image)

            fixed = re.sub(r'https:/', 'https:/', full_image_joined)

            width = dimensions[img].split(' x ')[0]

            height = dimensions[img].split(' x ')[1]

            obj = {
                "full-image": fixed,
                "label-image": images[img],
                "height": int(height),
                "width": int(width),
                "clicks": 0,
                'tags': re.sub(r'[0-9,]*', '', (re.sub(r'\n', '', tags[img]).lower()))
            }

            output_writer.writerow(obj)

    print("Finished Processing")
    




while query not in "no exit stop quit":
    scrap(query)

    query = input("Would you like to process another image type? If not just type quit, no, exit, or stop.  ")