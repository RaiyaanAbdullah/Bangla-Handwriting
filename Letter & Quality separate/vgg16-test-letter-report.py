import cv2 
import os 
import numpy as np 
from random import shuffle 
from tqdm import tqdm 
import tensorflow as tf
from tensorflow.keras import layers,Sequential,optimizers,applications, Model, applications 
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import model_from_json, load_model
import csv

num_classes=12
batch_size = 8 #more means better faster convergence but takes more resources
train_data_num = 6850 #change it accordingly

letter_array=['a','b','c','d','e','f','g','h','i','j','k','x']


    
data= np.load('augmented_data_mini_letter.npy', allow_pickle=True)

print(np.shape(data))
'''Running the training and the testing in the dataset for our model'''

img_data = np.array([i[0] for i in data]).reshape(-1,224,224,3)
lbl_data = np.array([i[1] for i in data]).reshape(-1,num_classes)



tst_img_data = img_data[train_data_num:,:,:,:]
tst_lbl_data = lbl_data[train_data_num:,:]


model = load_model('vgg16_model_letter.h5')

print('Testing on unseen data:')
x_test = applications.vgg16.preprocess_input(tst_img_data)
y_test = tst_lbl_data

with open('reports/letter_vgg16_report.csv',mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['Input', 'Output','Labels'])

    prediction = model.predict(x_test)    
    for i in range(len(y_test)):
        
        letter_label=letter_array[np.argmax(y_test[i])]
        letter_predict=letter_array[np.argmax(prediction[i])]
    
        if i<num_classes:
            csv_writer.writerow([letter_label, letter_predict,letter_array[i]])
        else:
            csv_writer.writerow([letter_label, letter_predict])        
 


    

