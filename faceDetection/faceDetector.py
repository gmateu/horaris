# -*- coding: utf-8 -*-
import os
import sys, os
from opencv.cv import *
from opencv import adaptors
from opencv.highgui import *

DIR_FOTOS="/home/guillem/Dropbox/fotosalumnes/2010/" #directori on hi ha les fotos, el darrer "/" és important
DIR_DESTI="/home/guillem/Dropbox/compartides/lluisFusterGuillem/fotosAlumnes2010/" #directori on es guarden els rostres, el darrer "/" és important
PATRO_XML="haarcascade_frontalface_alt.xml" #patrons a buscar
MARGE_LATERAL=70 #les cares s'han d'ampliar tan cap als laterals com en la zona vertical
MARGE_VERTICAL=190
xRATIO=480
yRATIO=640
hResized=150 #alçada de les imatges redimensionades
RESIZE=True #en aquest cas redimensinarem les cares
RENAME=True #en aquest cas reanomenam les captures segons l'ordre en que es van prendre

def detectObjects(image,k,file):
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
             img = adaptors.Ipl2PIL(image)
             box = (f.x-MARGE_LATERAL, f.y-100, f.x+f.width+MARGE_LATERAL, f.y+f.height+MARGE_VERTICAL)
             #redimensionam la capsa per evitar deformacions a l'hora de pujar al gestib
             faceY=box[3]-box[1]
             faceX=(faceY*xRATIO)/yRATIO
             #box=(f.x-MARGE_LATERAL, f.y-MARGE_VERTICAL, f.x+faceX,f.y+f.height+MARGE_VERTICAL)
             print "box",box
             region = img.crop(box)
             factor=float(hResized)/region.size[1]
             wResized=region.size[0]*factor
             sizeRedim=(int(wResized),int(hResized))
             if RESIZE:
                region=region.resize(sizeRedim)   
                print "region.size",region.size,"sizeRedim",sizeRedim
             i=i+1
             nom=DIR_DESTI+file
             if RENAME:
                 nom=DIR_DESTI+str(k)+'_'+str(i)+'.jpg'    
                 print "rename nom",nom
             region.save(nom)
 
def main():
    k=0
    for root,dirs,files in os.walk(DIR_FOTOS):
	print "roots",root,"dirs",dirs,"files",files
        files.sort()
        for file in [f for f in files if f.lower().endswith("jpg")]:
            picture=root+"/"+file
            image = cvLoadImage(picture, 1)
            k=k+1
            print k,picture,"file",file
            detectObjects(image,k,file)
 
if __name__ == "__main__":
  main()
