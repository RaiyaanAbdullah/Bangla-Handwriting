import cv2 
import os 
import numpy as np 
from random import shuffle 
from tqdm import tqdm 
import tensorflow as tf
from tensorflow.keras import layers,Sequential,optimizers,applications, Model, applications

num_classes=44
batch_size = 8 #more means better faster convergence but takes more resources
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
base_model = applications.ResNet50(weights='imagenet', include_top=False)
x = base_model.output
x = layers.GlobalMaxPooling2D()(x)
x = layers.Dense(512, activation='relu')(x)
predictions = layers.Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

'''
#the batch normalization layers are not frozen
he_normal = tf.keras.initializers.he_normal()
for layer in base_model.layers:
    #Code taken from: https://towardsdatascience.com/what-if-only-batch-normalization-layers-were-trained-1d13e2d3f35c
    if layer.name.endswith('_bn'):
        new_weights = [
            he_normal(layer.weights[0].shape), # Gamma
            tf.zeros(layer.weights[1].shape), # Beta
            tf.zeros(layer.weights[2].shape), # Mean
            tf.ones(layer.weights[3].shape)] # Std

        layer.set_weights(new_weights)
        layer.trainable = True
    else:
        layer.trainable = False
'''

for layer in base_model.layers:
    layer.trainable = False
    
optimizer=optimizers.Adam(lr=1e-3)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
   
x_train = applications.resnet.preprocess_input(tr_img_data)
y_train = tr_lbl_data



print(model.evaluate(x_train, y_train, batch_size=batch_size, verbose=1))
model.fit(x_train, y_train, epochs=10 , batch_size=batch_size, shuffle=False, 
          validation_split=0.1)


#unfreezing all layers and retraining with low learning rate
for layer in model.layers:
    layer.trainable = True

optimizer2=optimizers.Adam(lr=1e-4)
model.compile(optimizer=optimizer2, loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=25 , batch_size=batch_size, shuffle=False, 
          validation_split=0.1) #will try with 5 epochs later


print('Testing on unseen data:')
x_test = applications.resnet.preprocess_input(tst_img_data)
y_test = tst_lbl_data
test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=1)
#model.summary()
model.save('resnet_model.h5')

print("Saved model to disk")

