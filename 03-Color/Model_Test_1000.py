import numpy as np
from imageio import imread, imsave
import os

def Model(Image, threshold):
    m, n, k = Image.shape
    count_0 = np.zeros(Image.shape)
    count_1 = np.zeros(Image.shape)
    count_2 = np.zeros(Image.shape)
    count_3 = np.zeros(Image.shape)
    count = np.zeros([4, 1])
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
                elif diff1 > threshold and diff2 <= threshold and diff3 > threshold and diff4 > threshold and diff5 <= threshold and diff6 > threshold:
                    count_2[i,j,c] = 1
                    count[2] += 1
                elif diff1 > threshold and diff2 > threshold and diff3 > threshold and diff4 <= threshold and diff5 <= threshold and diff6 <= threshold:
                    count_1[i,j,c] = 1
                    count[1] += 1
                elif diff1 <= threshold and diff2 <= threshold and diff3 > threshold and diff4 <= threshold and diff5 > threshold and diff6 > threshold:
                    count_1[i,j,c] = 1
                    count[1] += 1
                elif diff1 > threshold and diff2 <= threshold and diff3 <= threshold and diff4 > threshold and diff5 > threshold and diff6 <= threshold:
                    count_3[i,j,c] = 1
                    count[3] += 1
                elif diff1 <= threshold and diff2 > threshold and diff3 <= threshold and diff4 > threshold and diff5 <= threshold and diff6 > threshold:
                    count_3[i,j,c] = 1
                    count[3] += 1
    Angle_Value = 5
    Angle_Count = 0
    for i in range(4):
        if Angle_Count <= count[i]:
            Angle_Value = i
            Angle_Count = count[i]
    return Angle_Value
    

def main():
    Img_Number = 10000
    Filename1 = 'Input/Size_1000/'
    Filename2 = 'Result/Pre_1000.txt'
    file = open(Filename2,'w')
    for i in range(Img_Number):
        print('Time: %04d'%i)
        Threshold = 10
        Name = Filename1 + '%04d.png' % i
        Image = imread(Name)
        Angle_Pre = Model(Image, Threshold)
        file.write(str(Angle_Pre) + '\n')
    file.close()
    print('Model_Test_1000 Over !')

main()
os.system('pause')
