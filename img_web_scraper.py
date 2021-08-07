# Web scraping to build dataset in training the Machine Learning Model 
# Run this script to download plant/tree images scraped from the web to your local machine 
# Required libraries: bs4, requests, collections, os

from bs4 import BeautifulSoup
import requests 
import os 
from collections import defaultdict 

vegetation_dict = defaultdict(list)

# Unlimited arguments can be passed into this function, following this format (keyword=category_name)
# Note: Category_name will be the folder which the images will be inserted into 
def find_img_from_keyword(**kwargs): 
  for word, category_name in kwargs.items():
    url = 'https://www.google.com/search?q=' + str(word) + '&source=lnms&tbm=isch'
    page = requests.get(url) 
    soup = BeautifulSoup(page.content, 'html.parser') 
    for img in soup.find_all('img', class_="yWs4tf"): 
      img_src = img.attrs['src'] 
      vegetation_dict[category_name].append(img_src) 

def find_img_from_url(url, category_name, *args): 
  page = requests.get(url) 
  soup = BeautifulSoup(page.content, 'html.parser') 
  for attribute in args: 
    img = soup.find('img', alt=attribute)
    img_src = img.attrs['src'] 
    vegetation_dict[category_name].append(img_src)
    
def image_download(img_url_list, directory):
  os.makedirs(directory)
  for count, i in enumerate(img_url_list): 
    img_file = os.path.join(directory, "{category}{num}.jpg".format(category=directory, num=count))
    img = requests.get(i)
    with open(img_file, 'wb') as file: 
      file.write(img.content)
  
def all_img_download(): 
  os.makedirs("images")
  img_folder = os.path.join(os.getcwd(), "images")
  os.chdir(img_folder)
  for category in vegetation_dict: 
    image_download(vegetation_dict[category], category) 
    
def main(): 
  find_img_from_keyword(tree='trees', trees='trees', plants='plants', garden_plant='plants', outdoor_plants='plants', backyard_trees='trees')
  find_img_from_url('https://treesunlimitednj.com/how-do-i-recognize-when-a-tree-is-sick/', 'sick', "Diseased-Tree", "Aphid-Infestation-on-Elder")
  find_img_from_keyword(unhealthy_tree='sick', wrinkled_plant_leaves='sick', tree_disease_spots='sick', dying_leaves_plants='sick', pests_attack_plants='sick') 
  all_img_download()

if __name__ == '__main__': 
  main()

