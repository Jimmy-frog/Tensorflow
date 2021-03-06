import numpy as np 
import tensorflow
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D,\
BatchNormalization,Dropout, Dense, Flatten,AveragePooling2D
from keras.models import Model
from keras.layers import Input, concatenate

def Conv2d_BN(x, nb_filter, kernel_size, padding ="same", strides=(1,1),name=None):
    x = Conv2D(nb_filter, kernel_size, padding = padding, strides = strides, activation = "relu")(x)
    x = BatchNormalization(axis=3)(x)
    return x

def Inception(x, nb_filter,name = None):
    
    branch1x1 = Conv2d_BN(x, nb_filter,(1,1), padding="same", strides=(1,1),name=None)
    
    branch3x3 = Conv2d_BN(x, nb_filter,(1,1), padding="same", strides=(1,1),name=None)
    branch3x3 = Conv2d_BN(branch3x3, nb_filter,(3,3), padding="same", strides=(1,1),name=None)
    
    branch5x5 = Conv2d_BN(x, nb_filter,(1,1), padding="same", strides=(1,1),name=None)
    branch5x5 = Conv2d_BN(branch5x5, nb_filter,(1,1), padding="same", strides=(1,1),name=None)
    
    branchpool = MaxPooling2D(pool_size = (3,3), padding="same", strides=(1,1))(x)
    branchpool = Conv2d_BN(branchpool, nb_filter,(1,1), padding="same", strides=(1,1),name=None)
    
    x = concatenate([branch1x1,branch3x3,branch5x5,branchpool],axis=3)
    return x

inpt = Input(shape=(224,224,3))
x = Conv2d_BN(inpt, 64, (7,7), strides=(2,2),padding="same")
x = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding="same")(x)
x = Conv2d_BN(x, 192, (3,3), strides=(1,1),padding="same")
x = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding="same")(x)
x = Inception(x,64)
x = Inception(x,120)
x = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding="same")(x)
x = Inception(x,128)
x = Inception(x,128)
x = Inception(x,128)
x = Inception(x,132)
x = Inception(x,208)
x = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding="same")(x)
x = Inception(x,208)
x = Inception(x,256)
x = AveragePooling2D(pool_size=(7,7),strides=(7,7),padding="same")(x)
x = Dropout(0.4)(x)
x = Dense(1000, activation = "relu")(x)
x = Dense(1000, activation = "softmax")(x)

model = Model(inpt, x ,name = "Inception")
model.summary()
