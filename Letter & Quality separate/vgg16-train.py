import cv2 
import os 
import numpy as np 
from random import shuffle 
from tqdm import tqdm 
import tensorflow as tf
from tensorflow.keras import layers,Sequential,optimizers,applications, Model, applications 
from tensorflow.keras.preprocessing import image

num_classes=12
batch_size = 8 #more means better faster convergence but takes more resources
train_data_num = 6850 #change it accordingly


data= np.load('augmented_data_mini_letter.npy', allow_pickle=True)

print(np.shape(data))
'''Running the training and the testing in the dataset for our model'''

img_data = np.array([i[0] for i in data]).reshape(-1,224,224,3)
lbl_data = np.array([i[1] for i in data]).reshape(-1,num_classes)

tr_img_data = img_data[:train_data_num,:,:,:]
tr_lbl_data = lbl_data[:train_data_num,:]

tst_img_data = img_data[train_data_num:,:,:,:]
tst_lbl_data = lbl_data[train_data_num:,:]


#Code taken from: https://github.com/keras-team/keras/issues/9214
base_model = applications.VGG16(weights='imagenet', include_top=False)
x = base_model.output
x = layers.GlobalMaxPooling2D()(x)
x = layers.Dense(512, activation='relu')(x)
predictions = layers.Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)
#model.summary()
    

        
x_train = applications.vgg16.preprocess_input(tr_img_data)
y_train = tr_lbl_data



 
#unfreezing all layers and retraining with low learning rate
for layer in model.layers:
    layer.trainable = True



optimizer=optimizers.Adam(lr=5e-5)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5 , batch_size=batch_size, shuffle=False, 
          validation_split=0.1) #will try with 5 epochs later

  

print('Testing on unseen data:')
x_test = applications.vgg16.preprocess_input(tst_img_data)
y_test = tst_lbl_data
test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=1)
#model.summary()


model.save('vgg16_model.h5')

print("Saved model to disk")
