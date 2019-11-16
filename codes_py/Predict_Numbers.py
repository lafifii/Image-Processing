# -*- coding: utf-8 -*-
"""PDI 7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pMwcWt2gRNB-nCh0B3Iom7HqrXYwh37y
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def loadImg(path):
  img = cv2.imread(path, 0)
  return img
def showImg(img):
  plt.axis("off")
  plt.imshow(img, cmap="gray")
  plt.show()

img = loadImg("image.jpg")
showImg(img)

Gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
Gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
print(Gx)
print(Gy)

mag,ang = cv2.cartToPolar(Gx, Gy)

print(mag)
print(ang*180/np.pi)

showImg(mag)

def hog(img, B):
  gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
  gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
  mag,ang = cv2.cartToPolar(gx, gy)
  bins = np.int32((ang*B)/(2*np.pi))
  bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
  mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
  hists = [np.bincount(b.ravel(), m.ravel(), B) for b,m in zip(bin_cells, mag_cells)]
  hist = np.hstack(hists)
  return hist

img = loadImg("digits.png")
img1 = img[0:20, 0:20]
showImg(img1)

hist = hog(img1, 8)
print(hist.shape)
plt.plot(hist)
plt.show()

img = loadImg("digits.png")

train = []
target = []

for x in range(50):
  for y in range(50):
    train.append( hog(img[20*x:20*(x+1), 20*y:20*(y+1)], 16) )
    target.append(x//5)

train = np.vstack(train)
target = np.vstack(target)

test = []

for x in range(50):
  for y in range(50, 100):
    test.append( hog(img[20*x:20*(x+1), 20*y:20*(y+1)], 16) )
test = np.vstack(test)

train = np.float32(train)
test = np.float32(test)

print(train.shape)
print(test.shape)
print(target.shape)

svm = cv2.ml.SVM_create()
svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setType(cv2.ml.SVM_C_SVC)
svm.setC(2.67)
svm.setGamma(5.383)

svm.train(train, cv2.ml.ROW_SAMPLE, target)

result = svm.predict(test)[1]
mask = (result==target)
correct = np.count_nonzero(mask)
print(correct*100.0/result.size)

import random

x = random.choice(range(0, 50))
y = random.choice(range(50, 100))

img2 = img[20*x:20*(x+1),20*y:20*(y+1)]

hist = hog(img2, 16)
hist = np.float32(hist)
result = int( svm.predict(hist.reshape(1,64))[1][0][0] )
print('La clase del numero es {}'.format(result))

showImg(img2)