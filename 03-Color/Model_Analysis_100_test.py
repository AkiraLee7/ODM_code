import numpy as np
import os

Image_Number = 1000

Filename1 = 'Output/Target_100.txt'
Filename2 = 'Result/Pre_100_test.txt'

Target_t = np.loadtxt(Filename1)
Pre_t = np.loadtxt(Filename2)
Target = Target_t[0:Image_Number]
Pre = Pre_t[0:Image_Number]


count = 0
for i in range(0,Image_Number):
    if Target[i] == Pre[i]:
        count += 1
    else:
        print(i)
        print(Target[i], Pre[i])
        

Accuracy = (1.0 * count) / (1.0 * Image_Number) * 100

print('#######Result Analysis...#######')
print("Total: %04d"%Image_Number + " Correct: %04d"%count)
print("Accuracy: %3d"%Accuracy)

os.system('pause')
