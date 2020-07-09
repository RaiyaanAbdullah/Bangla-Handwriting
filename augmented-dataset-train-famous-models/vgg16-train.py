import cv2 
import os 
import numpy as np 
from random import shuffle 
from tqdm import tqdm 
import tensorflow as tf
from tensorflow.keras import layers,Sequential,optimizers,applications, Model, applications

num_classes=44
batch_size = 10 #more means better faster convergence but takes more resources
train_data_num = 6400 #change it accordingly

data= np.load('augmented_data_mini.npy', allow_pickle=True)

print(np.shape(data))
'''Running the training and the testing in the dataset for our model'''

img_data = np.array([i[0] for i in data]).reshape(-1,224,224,3)
lbl_data = np.array([i[1] for i in data]).reshape(-1,44)

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


for layer in base_model.layers:
    layer.trainable = False


optimizer=optimizers.Adam(lr=1e-3)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
x_train = applications.vgg16.preprocess_input(tr_img_data)
y_train = tr_lbl_data

'''
model.add(layers.InputLayer(input_shape=[224,224,3]))
model.add(layers.Conv2D(32, kernel_size=5, activation='relu'))
model.add(layers.MaxPooling2D(pool_size=3))
model.add(layers.Conv2D(64, kernel_size=5, activation='relu'))
model.add(layers.MaxPooling2D(pool_size=5))
model.add(layers.Conv2D(128, kernel_size=5, activation='relu'))
model.add(layers.MaxPooling2D(pool_size=5))
#model.add(layers.Dropout(0.25))
model.add(layers.Flatten())
model.add(layers.Dense(512,activation='relu'))
#model.add(layers.Dropout(0.5))
model.add(layers.Dense(256,activation='relu'))
'''

print(model.evaluate(x_train, y_train, batch_size=batch_size, verbose=1))
model.fit(x_train, y_train, epochs=17 , batch_size=batch_size, shuffle=False, 
          validation_split=0.1)

#unfreezing all layers and retraining with low learning rate
for layer in model.layers:
    layer.trainable = True

optimizer2=optimizers.Adam(lr=1e-5)
model.compile(optimizer=optimizer2, loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10 , batch_size=batch_size, shuffle=False, 
          validation_split=0.1) #will try with 5 epochs later

print('Testing on unseen data:')
test_loss, test_acc = model.evaluate(tst_img_data,  tst_lbl_data, verbose=1)
#model.summary()
model.save('vgg16_model.hdf5')

print("Saved model to disk")

