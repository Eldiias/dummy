import requests as r
import os
import numpy as np
from PIL import Image, ImageFilter
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans


def get_image_from_web(x:str):
    image=r.get(x).content
    last=len(os.listdir(r'./Pictures\pics'))
    with open(r'./Pictures\pics/'+str(last+1)+'.png','wb') as file:
        file.write(image)
    return get_image_standard_size(r'./Pictures\pics/'+str(last+1)+'.png')


def get_image_standard_size(x:str)-> np.array:
    return np.array(Image.open(x).resize((640,480),Image.ANTIALIAS).filter(ImageFilter.MedianFilter(size=7)))

def get_new_image(arr:np.array, n:int)->np.array:
    mkm=MiniBatchKMeans(n_clusters=n)
    mkm.fit(arr.reshape((-1,3 if len(arr.shape)==3 else 1)))
    labels=mkm.labels_
    values=mkm.cluster_centers_
    img_compressed=values[labels].reshape(arr.shape).round()

    Image.fromarray(np.uint8(img_compressed)).convert('RGB').filter(ImageFilter.CONTOUR).show()

    border=(img_compressed[1:,1:,0]==img_compressed[:-1,1:,0]) & (img_compressed[1:,1:,0]==img_compressed[1:,:-1,0])
    border=np.vstack((
        np.hstack((
            [False], 
            img_compressed[0,1:,0]==img_compressed[0,:-1,0])).reshape((1,-1)),
        np.hstack((
            (img_compressed[1:,0,0]==img_compressed[:-1,0,0]).reshape((-1,1)),
             border))))



    _, [ax1,ax2,ax3]=plt.subplots(3,1,sharex=True, figsize=(80,36))

    plt.axis('off')
    ax3.imshow(border, cmap='gray')
    ax3.set_title('borderline')
    ax3.axis('off')
    ax2.imshow(img_compressed.astype(np.uint8))
    ax2.set_title(f'New image with {n} colors')
    ax2.axis('off')
    ax1.imshow(arr.astype(np.uint8))
    ax1.set_title('Original image')
    ax1.axis('off')
    plt.show()
    
    return img_compressed, labels, values, border

if __name__=='__main__':
    url=input('Pass the full path to the image or the url please \t')
    if url=='': url=r'C:\Users\eldii\Pictures\pics/'+np.random.choice(os.listdir(r'C:\Users\eldii\Pictures\pics'))
    print(url)
    n=int(input('How many colors you want to use? \t'))
    i,l,v,b=get_new_image(
        get_image_from_web(url) if url.startswith('http') else get_image_standard_size(url),
        n)