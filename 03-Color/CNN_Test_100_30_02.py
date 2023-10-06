import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

import numpy as np
import os

from imageio import imread, imsave

def GetData(Img_Number, Filename, m, n, k):
    _Data = np.zeros([Img_Number,m,n,k])
    for i in range(Img_Number):
        Name = Filename + '%04d.png' % i
        Image = imread(Name)
        _Data[i,:,:,:] = Image

    return _Data

def main():
    Img_Number = 10000
    dividerate = 0.75
    Filename1 = 'Input/Size_100/'
    Filename2 = 'Output/Target_100.txt'
    Filename3 = 'Result/CNN_Acc_100_30_02.txt'
    Nametem = Filename1 + '%04d.png' % 1
    Imagetem = imread(Nametem)
    m,n,k = Imagetem.shape
    Data = GetData(Img_Number, Filename1, m, n, k)
    Target_t = np.loadtxt(Filename2)
    Target = Target_t[0:Img_Number]
    midpoint = round(Img_Number * dividerate)
    train_x = Data[0:midpoint,:,:]
    train_y = Target[0:midpoint]
    train_labels = train_y.reshape(-1,1)

    test_x = Data[midpoint:Img_Number,:,:]
    test_y = Target[midpoint:Img_Number]
    test_labels = test_y.reshape(-1,1)

    train_images, test_images = train_x / 255.0, test_x / 255.0

    file = open(Filename3,'w')

    for i in range(30):
        print('Time: ', i, '\n')
        
        model = models.Sequential()
        model.add(layers.Conv2D(30, (3, 3), activation='relu', input_shape=(m, n, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(4))

        model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

        history = model.fit(train_images, train_labels, epochs = 20, 
                        validation_data=(test_images, test_labels))
        '''
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0, 1])
        plt.legend(loc='lower right')
        plt.show()
        '''

        test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

        CNN_Acc = test_acc * 100

        file.write(str(CNN_Acc) + '\n')

        print(test_acc)
    file.close()
    print('CNN_Test_100_04_01 Over !')

main()
os.system('pause')
