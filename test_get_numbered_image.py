import requests as r
import os
import numpy as np
from PIL import Image, ImageFilter
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
from mpl_toolkits.axes_grid1 import ImageGrid
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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
    
    new_image=np.array(Image.fromarray(np.uint8(img_compressed)).convert('RGB').filter(ImageFilter.CONTOUR))
    Image.fromarray(np.uint8(img_compressed)).convert('RGB').filter(ImageFilter.CONTOUR).show()

    vertical=np.vstack((np.ones(new_image.shape[1]),new_image[1:,:,0]!=new_image[:-1,:,0]))
    horizontal=np.hstack((np.ones((new_image.shape[0],1)),new_image[:,1:,0]!=new_image[:,:-1,0]))
    numbers_to_be_displayed=vertical*horizontal
    zzz=pd.DataFrame((labels+1).reshape(new_image.shape[:2])*numbers_to_be_displayed)
    zzzzz=zzz.reset_index().melt('index').copy()
    zzzzz=zzzzz.query('value>0').copy()
    zzzzz=zzzzz.rename(columns={'index':'row', 'variable':'column'})
    zzzzz['value']=zzzzz['value'].astype(int).astype(str)
    zzzzz.row=zzz.shape[0]-zzzzz.row

    scatter=px.scatter(zzzzz, x='column', y='row', text='value', opacity=0)
    scatter=scatter.update_traces(textfont_size=10)

    fig = go.Figure()
    layout= go.Layout(images= [dict(
                    source= Image.fromarray(new_image),
                    xref= "x",
                    yref= "y",
                    y=768,
                    x=0,
                    sizex= 1024,
                    sizey= 768,
                    sizing= "stretch",
                    opacity= 1,
                    layer= "below")])
    fig=go.Figure(data=[scatter.data[0]],layout=layout)
    fig.show()

    
    return img_compressed, labels, values, zzzzz

if __name__=='__main__':
    url=input('Pass the full path to the image or the url please \t')
    if url=='': url=r'C:\Users\eldii\Pictures\pics/'+np.random.choice(os.listdir(r'C:\Users\eldii\Pictures\pics'))
    #print(url)
    n=int(input('How many colors you want to use? \t'))
    i,l,v,b=get_new_image(
        get_image_from_web(url) if url.startswith('http') else get_image_standard_size(url),
        n)
    
