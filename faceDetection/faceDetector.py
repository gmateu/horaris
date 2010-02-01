# -*- coding: utf-8 -*-
import os
import sys, os
from opencv.cv import *
from opencv import adaptors
from opencv.highgui import *

DIR_FOTOS="/home/liceu/Imatges/Fotografies/2010/01/28"
DIR_DESTI="/home/liceu/Imatges/curs2009/"
PATRO_XML="haarcascade_frontalface_alt.xml"
MARGE_LATERAL=100
MARGE_VERTICAL=150

def detectObjects(image,file,k):
     grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
     cvCvtColor(image, grayscale, CV_BGR2GRAY)
     
     storage = cvCreateMemStorage(0)
     cvClearMemStorage(storage)
     cvEqualizeHist(grayscale, grayscale)
     cascade = cvLoadHaarClassifierCascade(PATRO_XML,cvSize(1,1))
     faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2,CV_HAAR_DO_CANNY_PRUNING, cvSize(50,50))
     i=0
     if faces:
         for f in faces:
             img = adaptors.Ipl2PIL(image) ##.resize((320,240))
             box = (f.x-MARGE_LATERAL, f.y-MARGE_VERTICAL, f.x+f.width+MARGE_LATERAL, f.y+f.height+MARGE_VERTICAL)
             region = img.crop(box)
             print "k",k
             i=i+1
             region.save(DIR_DESTI+str(k)+'_'+str(i)+'.jpg')
 
def main():
    k=0
    for root,dirs,files in os.walk(DIR_FOTOS):
        files.sort()
        for file in [f for f in files if f.lower().endswith("jpg")]:
            image = cvLoadImage(file, 1)
            k=k+1
            print k,file
            detectObjects(image,file,k)
 
if __name__ == "__main__":
  main()

