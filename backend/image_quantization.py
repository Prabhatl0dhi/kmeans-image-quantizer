import numpy as np
import random
from tqdm import tqdm

class Quantize:
    def __init__(self,image,n_colours=5,max_iter=5):
        self.n_colours=n_colours
        self.image=image
        self.max_iter=max_iter
        
    def initial_centroids(self):
        copy_img=np.copy(self.image)
        self.all_vectors=copy_img.reshape(-1,3)
        centers=random.sample(list(self.all_vectors),self.n_colours)
        return np.array(centers)
    
    def update_centroids(self):
        labels=np.zeros((self.image.shape[0],self.image.shape[1]))
        centers=self.initial_centroids()
        for i in tqdm(range(self.max_iter),desc="Training.."):
          distances = np.linalg.norm(self.all_vectors[:, np.newaxis, :] - centers[np.newaxis, :, :], axis=2)
          flat_labels=np.argmin(distances,axis=1)
          labels=flat_labels
        #   print(labels)
          updated_centroids=[]
          for j in range(self.n_colours):
              updated_centroids.append(self.all_vectors[labels==j].mean(axis=0))     
          if(np.array(updated_centroids,dtype=int)==centers.astype(int)).all():
              print(f"number of iterations were:{i+1}")
              return centers,labels
          centers=np.array(updated_centroids,dtype=float)  
             
        print(f"number of iterations were:{i+1}") 
        return centers , labels
    
    def reconstructed_image(self):
        centers,labels=self.update_centroids()
        centers=centers/255
        return centers[labels].reshape(self.image.shape)
    
        
            