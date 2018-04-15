"""

This code uses the unsplash api to run a search call can download the pictures returned with each search query
along with its tags. You can extend as many search queries as you like, given your unsplash developer account app facilitates it

Before running this code, these steps should be followed:
    - Create an unsplash developer account
    - Create an app (free tier comes with 50 requests per hour)
    - Obtain the Access Key given for the created app

**Note: Because of the limited no. of request allowed by unsplash api per hour, this code might run into access denial on a free tier app
To increase the limit you will have to contact unsplash and justify your requirements.

** What this code facilitates
    - Downloading 30 photos from each search query
    - Obtaining user created tags for each photo
    - Creating a dataset with downloaded photos along with a directory of tags
"""
import urllib.request, json 
import os

# lists to store data
img_ids = []
img_tags = []
img_tags_temp = []

#unsplash search tags
search_tags = ['nature','home','city','business','computer','love','house','people','animals','outdoor','portrait','sea','beach','summer','sky', 'space']

#looping over search tags
for query in search_tags:
    
    #sending request unsplash search api with the query and your access key (replace YOUR_ACCESS_KEY here)
    with urllib.request.urlopen("https://api.unsplash.com/search/photos/?query=" + query +"&per_page=30&client_id=YOUR_ACCESS_KEY") as url:
        data = json.loads(url.read().decode())

        #loop over no. of results returned from the api call
        for photo in range(0,30):
        	
            # get the download image url from data
            download_url = data['results'][photo]['links']['download_location']

            # open the download url
            with urllib.request.urlopen(download_url + "/?client_id=YOUR_ACCESS_KEY") as d_url:
                d_data = json.loads(d_url.read().decode())
                # opening the download url with access key gives the direct download url (Note: you should replace YOUR_ACCESS_KEY here)
                s_url = d_data['url']
                print(s_url)

                fullfilename = os.path.join('/output' , data['results'][photo]['id'] + '.jpg')

                #obtain the image from the direct download url
                urllib.request.urlretrieve(s_url, fullfilename)
                #Append the image named to list
                img_ids.append(data['results'][photo]['id'])

            # loop over the tags senction of data    
            for tag in range(0,4):
                #capture 5 or less tags
                try:
                    imag_tag = data['results'][photo]['photo_tags'][tag]['title']
                    print(imag_tag)
                    #Append the tags into a temperory list
                    img_tags_temp.append(imag_tag)
                except IndexError:
                    pass
                continue        
            # Store the image particula tags in the main list    
            img_tags.append(img_tags_temp)
            img_tags_temp = []  


print(img_ids)
print(img_tags)

#save the image name and tags to file in the output directory in the end
with open('/output/data.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write(str(img_ids))
    myfile.write(str(img_tags))    