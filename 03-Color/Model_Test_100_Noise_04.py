import numpy as np
from imageio import imread, imsave
import os

def addsalt_pepper(img, SNR):
    img_ = img.copy()
    img_ = img_.transpose(2, 1, 0)
    c, h, w = img_.shape
    mask = np.random.choice((0, 1, 2), size=(c, h, w), p=[(1 - SNR), SNR/2.0, SNR/2.0])
    mask = np.repeat(mask, 1, axis=0)
    img_[mask == 1] = 255
    img_[mask == 2] = 0
    img_ = img_.transpose(2, 1, 0)
    return img_

def Model(Image, threshold):
    m, n, k = Image.shape
    count_0 = np.zeros(Image.shape)
    count_1 = np.zeros(Image.shape)
    count_2 = np.zeros(Image.shape)
    count_3 = np.zeros(Image.shape)
    count = np.zeros([8, 1])
    for c in range(k):
        for i in range(m - 1):
            for j in range(n - 1):
                scaner = Image[i:i+2, j:j+2, c]
                diff1 = abs(float(scaner[0, 0]) - float(scaner[0, 1]))
                diff2 = abs(float(scaner[0, 0]) - float(scaner[1, 0]))
                diff3 = abs(float(scaner[0, 0]) - float(scaner[1, 1]))
                diff4 = abs(float(scaner[0, 1]) - float(scaner[1, 0]))
                diff5 = abs(float(scaner[0, 1]) - float(scaner[1, 1]))
                diff6 = abs(float(scaner[1, 0]) - float(scaner[1, 1]))
                if diff1 <= threshold and diff2 > threshold and diff3 > threshold and diff4 > threshold and diff5 > threshold and diff6 <= threshold:
                    count_0[i,j,c] = 1
                    count[0] += 1
                    count[6] += 1
                elif diff1 > threshold and diff2 <= threshold and diff3 > threshold and diff4 > threshold and diff5 <= threshold and diff6 > threshold:
                    count_2[i,j,c] = 1
                    count[2] += 1
                    count[7] += 1
                elif diff1 > threshold and diff2 > threshold and diff3 > threshold and diff4 <= threshold and diff5 <= threshold and diff6 <= threshold:
                    count_1[i,j,c] = 1
                    count[1] += 1
                    count[4] += 1
                elif diff1 <= threshold and diff2 <= threshold and diff3 > threshold and diff4 <= threshold and diff5 > threshold and diff6 > threshold:
                    count_1[i,j,c] = 1
                    count[1] += 1
                    count[4] += 1
                elif diff1 > threshold and diff2 <= threshold and diff3 <= threshold and diff4 > threshold and diff5 > threshold and diff6 <= threshold:
                    count_3[i,j,c] = 1
                    count[3] += 1
                    count[5] += 1
                elif diff1 <= threshold and diff2 > threshold and diff3 <= threshold and diff4 > threshold and diff5 <= threshold and diff6 > threshold:
                    count_3[i,j,c] = 1
                    count[3] += 1
                    count[5] += 1
    Angle_Value = 5
    Angle_Count = 0
    count[0] -= count[7]
    count[1] -= count[5]
    count[2] -= count[6]
    count[3] -= count[4]
    for i in range(4):
        if Angle_Count <= count[i]:
            Angle_Value = i
            Angle_Count = count[i]
    return Angle_Value
    

def main():
    Img_Number = 10000
    SNR = 4
    Filename1 = 'Input/Size_100/'
    Filename2 = 'Result/Pre_100_Noise_%02d.txt'%SNR
    Filename3 = 'Output/Target_100.txt'
    file = open(Filename2,'w')
    for t in range(30):
        print('Noise: %02d'% SNR,'Time: ', t)
        Angle_Pre = np.zeros([Img_Number, 1])
        for i in range(Img_Number):
            print('\r', 'Testing...', i, '/', Img_Number, end="", flush=True)
            Threshold = 10
            Name = Filename1 + '%04d.png' % i
            Image = imread(Name)
            Image_SNR = addsalt_pepper(Image, SNR/100.0)
            Angle_Pre[i] = Model(Image_SNR, Threshold)  
        print('Model_Test_100 Over !')

        Target_t = np.loadtxt(Filename3)
        Target = Target_t[0:Img_Number]
        count = 0
        for i in range(0,Img_Number):
            if Target[i] == Angle_Pre[i]:
                count += 1
                
        Accuracy = (1.0 * count) / (1.0 * Img_Number) * 100

        print('#######Result Analysis...#######')
        print("Total: %04d"%Img_Number + " Correct: %04d"%count)
        print("Accuracy: %3d"%Accuracy)
        file.write(str(Accuracy) + '\n')
    file.close()

main()
os.system('pause')
