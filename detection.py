import sys, os
from opencv.cv import *
from opencv.highgui import *

def detectObjects(image):
  """Converts an image to grayscale and prints the locations of any 
     faces found"""
  grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
  cvCvtColor(image, grayscale, CV_BGR2GRAY)

  storage = cvCreateMemStorage(0)
  cvClearMemStorage(storage)
  cvEqualizeHist(grayscale, grayscale)
  #cascade = cvLoadHaarClassifierCascade('haarcascade_frontalface_alt2.xml', cvSize(1,1))
  #cascade = cvLoadHaarClassifierCascade('haarcascade_frontalface_alt2.xml', cvSize(1,1))
  cascade = cvLoadHaarClassifierCascade('haarcascade_frontalface_alt2.xml',cvSize(1,1))
  cascade_eyes = cvLoadHaarClassifierCascade('haarcascade_mcs_eyepair_big.xml',cvSize(1,1))
  cascade_nose = cvLoadHaarClassifierCascade('haarcascade_mcs_nose.xml',cvSize(1,1))
  cascade_mouth = cvLoadHaarClassifierCascade('haarcascade_mcs_mouth.xml',cvSize(1,1))

  #faces = cvHaarDetectObjects(img,cascade, storage, 1.2, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(20, 20));
  #faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(50,50))
  faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(50,50))
  eyes = cvHaarDetectObjects(grayscale, cascade_eyes, storage, 1.15, 3, 0, cvSize(25,15))
  nose = cvHaarDetectObjects(grayscale, cascade_nose, storage, 1.15, 3, 0, cvSize(25,15))
  mouth = cvHaarDetectObjects(grayscale, cascade_mouth, storage, 1.15, 4, 0, cvSize(25,15))

  print "faces"
  if faces:
    for f in faces:
      print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
  print "eyes"
  if eyes:
    for f in eyes:
      print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
  print "nose"
  if nose:
    for f in nose:
      print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
  print "mouth"
  if mouth:
    for f in mouth:
      print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))



def main():
  image = cvLoadImage(sys.argv[1]);
  detectObjects(image)

if __name__ == "__main__":
  main()
