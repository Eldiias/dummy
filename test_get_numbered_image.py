import requests as r
import os
import numpy as np
from PIL import Image, ImageFilter
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
from mpl_toolkits.axes_grid1 import ImageGrid


def get_image_from_web(x:str):
    image=r.get(x).content
    last=len(os.listdir(r'./Pictures\pics'))
    with open(r'./Pictures\pics/'+str(last+2)+'.png','wb') as file:
        file.write(image)
    return get_image_standard_size(r'./Pictures\pics/'+str(last+2)+'.png')


def get_image_standard_size(x:str)-> np.array:
    return np.array(Image.open(x).resize((1024,768),Image.ANTIALIAS).filter(ImageFilter.MedianFilter(size=7)))

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

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



    fig = plt.figure(1,(40,80))
    grid = ImageGrid(fig, 111,
                    nrows_ncols=(1,3),
                    axes_pad=0.1,
                    )
    loi=[arr.astype(np.uint8), img_compressed.astype(np.uint8), border]
    for i in range(3):
        if i==2:
            grid[i].imshow(loi[i],interpolation='none', cmap='gray')
        else:
            grid[i].imshow(loi[i],interpolation='none')
    plt.show()
    
    return img_compressed, labels, values, border

if __name__=='__main__':
    url=input('Pass the full path to the image or the url please \t')
    if url=='': url=r'C:\Users\eldii\Pictures\pics/'+np.random.choice(os.listdir(r'C:\Users\eldii\Pictures\pics'))
    #print(url)
    n=int(input('How many colors you want to use? \t'))
    i,l,v,b=get_new_image(
        get_image_from_web(url) if url.startswith('http') else get_image_standard_size(url),
        n)
    
