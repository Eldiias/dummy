import requests as r
import os
import numpy as np
from PIL import Image, ImageFilter
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, DBSCAN
from mpl_toolkits.axes_grid1 import ImageGrid
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io
from hdbscan import HDBSCAN

def fig2img(fig) -> Image:
    """Convert a Matplotlib figure to a PIL Image and return it"""
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img
class PicNu:

    def __init__(self, path:str=None, n:int=None):

        self.path = path
        self.number_of_colors = n
        self.new_image = True #not to process an image again and again
        self.web = True if self.path and self.path.startswith('http') else False #scrape or not
        if not (os.path.exists('./Pictures/pics')): os.makedirs('./Pictures/pics'); os.chdir('./Pictures/pics')
        self.NClusters = False
        self.DBClusters = False
        self.HDBClusters = False

    def get_image_from_web(self, x):
        """Download an image, save in pics folder and read it back"""

        image=r.get(self.path).content
        last=len(os.listdir())
        with open(str(last+1)+'.png','wb') as file:
            file.write(image)
        self.get_image_standard_size(str(last+1)+'.png')
        self.new_image=False


    def get_image_standard_size(self, x:str)-> np.array:
        """Open an Image with PIL, convert to 1024x768 size and return a numpy ndarray"""


        self.image = np.array(Image.open(x).resize((1024,768),Image.ANTIALIAS).filter(ImageFilter.MedianFilter(size=7)))






    def get_new_image(self, x:str = None, n:int=-1)->np.array:
        """Decrease the color scheme of an Image"""
        #update path if needed
        if x != self.path: self.path = x; self.new_image = True; self.NClusters=False
        if self.path ==None: raise IOError('You didn\'t specify the path to the image yet')
        self.web = True if self.path and self.path.startswith('http') else False #scrape or not

        if self.number_of_colors!=n and n>0: self.number_of_colors=n
        if self.number_of_colors<0: raise IOError('Specify the number of colors')

        if self.new_image:
            #get the image:
            if self.web: self.get_image_from_web(x)
            else: self.get_image_standard_size(x)

            mkm = MiniBatchKMeans(n_clusters=self.number_of_colors)
            mkm.fit(self.image.reshape((-1,3 if len(self.image.shape)==3 else 1)))
            self.labels = mkm.labels_
            self.values = mkm.cluster_centers_
            self.image_compressed = self.values[self.labels].reshape(self.image.shape).round()
            self.NClusters=True
            self.image_new = Image.fromarray(np.uint8(self.image_compressed)).convert('RGB').filter(ImageFilter.CONTOUR)
            self.image_new.show()

            self.contour_plot = np.array(self.image_new)




    def get_numbers_HDB(self):
        """Get numbers displayed on the contour plot"""
        #x,y,r,g,b
        colors=list(np.where(self.contour_plot[:,:,0]>-1))+[(np.array(self.contour_plot[:,:,0].ravel(), dtype='int64'))]+[(np.array(self.contour_plot[:,:,1].ravel(), dtype='int64'))]+[(np.array(self.contour_plot[:,:,2].ravel(), dtype='int64'))]
        XXX=np.dstack(colors).reshape(-1,5)

        model1=HDBSCAN(min_cluster_size=2).fit(XXX)
        XXX=pd.DataFrame(XXX, columns=['x','y','r','g','b'])
        XXX['labels']=model1.labels_
        XXX['l']=self.labels      
        XXX=XXX.query('labels>-1').groupby('labels').mean()[['x','y','l']].applymap(int)
        XXX.x=768-XXX.x
        self.HDBClusters=True

        print('Stage of Clustering has finished')

    
    def get_numbers_DB(self):
        """Get numbers displayed on the contour plot"""
        #x,y,r,g,b
        colors=list(np.where(self.contour_plot[:,:,0]>-1))+[(np.array(self.contour_plot[:,:,0].ravel(), dtype='int64'))]+[(np.array(self.contour_plot[:,:,1].ravel(), dtype='int64'))]+[(np.array(self.contour_plot[:,:,2].ravel(), dtype='int64'))]
        XXX=np.dstack(colors).reshape(-1,5)

        model2=DBSCAN(min_samples=2, eps=3, n_jobs=-1).fit(XXX)
        XXX=pd.DataFrame(XXX, columns=['x','y','r','g','b'])
        XXX['labels']=model2.labels_
        XXX['l']=self.labels      
        XXX=XXX.query('labels>-1').groupby('labels').mean()[['x','y','l']].applymap(int)
        XXX.x=768-XXX.x
        self.DBClusters=True

        self.XXX=XXX
        print('Stage of Clustering has finished')     



    def plot_final(self):
        scatter=px.scatter(self.XXX, x='y', y='x', text='l', opacity=0)
        scatter=scatter.update_traces(textfont_size=5)

        fig = go.Figure()
        layout= go.Layout(images= [dict(
                        source= Image.fromarray(self.contour_plot),
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


new=PicNu()
new.get_new_image(r'C:\Users\eldii\Downloads/Olha.jpeg', 6)
new.get_numbers_HDB()
new.plot_final()