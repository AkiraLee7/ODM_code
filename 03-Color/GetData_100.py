import numpy as np
import random
import os
from imageio import imread, imsave


def Get_Height_Width(Img_Size, Edge_Dis):
    Size_Limit = min(Img_Size)
    _Height = random.randint(2, np.floor(0.1 * Size_Limit))
    _Width = random.randint(2 * _Height, 0.9 * Size_Limit - Edge_Dis * 2)
    
    return _Height, _Width


def Get_Objecet_Info(Angle_Value, Img_Size, Edge_Dis):
    Height, Width = Get_Height_Width(Img_Size, Edge_Dis)
    if Angle_Value == 0:
        x1 = random.randint(Edge_Dis, Img_Size[1] - Width - Edge_Dis)
        y1 = random.randint(Edge_Dis, Img_Size[0] - Height - Edge_Dis)
        x2 = x1
        y2 = y1 + Height - 1
        x3 = x1 + Width - 1
        y3 = y1 + Height - 1
        x4 = x1 + Width - 1
        y4 = y1
    elif Angle_Value == 1:
        x1 = random.randint(Edge_Dis, Img_Size[1] + 1 - Width - Height - Edge_Dis)
        y1 = random.randint(Width + Edge_Dis, Img_Size[0] - Height - Edge_Dis)
        x2 = x1 + Height - 1
        y2 = y1 + Height - 1
        x3 = x1 + Height + Width - 2
        y3 = y1 + Height - Width
        x4 = x1 + Width - 1
        y4 = y1 - Width + 1
    elif Angle_Value == 2:
        x1 = random.randint(Edge_Dis, Img_Size[1] - Height - Edge_Dis)
        y1 = random.randint(Edge_Dis, Img_Size[0] - Width - Edge_Dis)
        x2 = x1
        y2 = y1 + Width - 1
        x3 = x1 + Height - 1
        y3 = y1 + Width - 1
        x4 = x1 + Height - 1
        y4 = y1
    elif Angle_Value == 3:
        x1 = random.randint(Edge_Dis, Img_Size[1] + 1 - Width - Height - Edge_Dis)
        y1 = random.randint(Height + Edge_Dis, Img_Size[0] - Width - Edge_Dis)
        x2 = x1 + Width - 1
        y2 = y1 + Width - 1
        x3 = x1 + Height + Width - 2
        y3 = y1 - Height + Width
        x4 = x1 + Height - 1
        y4 = y1 - Height + 1
    else:
        print('Angle_Value Error !')
        
    _Object_Info = [x1, y1, x2, y2, x3, y3, x4, y4, Height, Width]
    
    return _Object_Info

def Object_Filling(Angle_Value, Object_Info, Img_Size, Img_BG, Object_Color):
    if Angle_Value == 0 or Angle_Value == 2:
        for i in range(Object_Info[0], Object_Info[4] + 1):
            for j in range(Object_Info[1], Object_Info[5] + 1):
                Img_BG[j,i] = Object_Color
    elif Angle_Value == 1 or Angle_Value == 3:
        k1 = (Object_Info[3] - Object_Info[1]) / (Object_Info[2] - Object_Info[0])
        k2 = (Object_Info[5] - Object_Info[3]) / (Object_Info[4] - Object_Info[2])
        k3 = (Object_Info[7] - Object_Info[5]) / (Object_Info[6] - Object_Info[4])
        k4 = (Object_Info[1] - Object_Info[7]) / (Object_Info[0] - Object_Info[6])
        b1 = Object_Info[1] - k1 * Object_Info[0]
        b2 = Object_Info[3] - k2 * Object_Info[2]
        b3 = Object_Info[5] - k3 * Object_Info[4]
        b4 = Object_Info[7] - k4 * Object_Info[6]
        k = [k1, k2, k3, k4]
        b = [b1, b2, b3, b4]
        for j in range(0, Img_Size[1]):
            for i in range(0, Img_Size[0]):
                conv_sum = j - k[0] * i
                conv_dif = j - k[1] * i
                if b[0] >= conv_sum >= b[2] and b[1] >= conv_dif >= b[3]:
                    Img_BG[j,i] = Object_Color
    else:
        print('Angle_Value Error !')
        
    _Get_Image = Img_BG
    
    return _Get_Image

def Get_Channel(Img_Size, Filling_Type, Object_Color):
    _Channel_Color = np.zeros(Img_Size)
    color_Type_0 = random.randint(0,1)
    if color_Type_0 == 0:
        Color_Start = random.randint(Object_Color + 15, 255)
        Color_End = random.randint(Object_Color + 15, 255)
    elif color_Type_0 == 1:
        Color_Start = random.randint(0, Object_Color - 15)
        Color_End = random.randint(0, Object_Color - 15)
    else:
        print('Color_Type Error')

    if Filling_Type == 0:
        Color_Step = (Color_End - Color_Start) / (Img_Size[0] - 1)
        Color_Cur = Color_Start
        for i in range(0, Img_Size[0]):
            _Channel_Color[i,:] = Color_Cur
            Color_Cur += Color_Step
    elif Filling_Type == 1:
        Color_Step = (Color_End - Color_Start) / (Img_Size[0] - 1)
        Color_Cur = Color_Start
        for j in range(0, Img_Size[1]):
            _Channel_Color[:,j] = Color_Cur
            Color_Cur += Color_Step
    elif Filling_Type == 2:
        for i in range(0, Img_Size[0]):
            for j in range(0, Img_Size[1]):
                Color_Cur = Color_Start + (i + j) * (Color_End - Color_Start) / (Img_Size[0] + Img_Size[1] - 2)
                _Channel_Color[i,j] = Color_Cur
    elif Filling_Type == 3:
        for i in range(0, Img_Size[0]):
            for j in range(0, Img_Size[1]):
                Color_Cur = Color_Start + (Img_Size[0] - 1 - i + j) * (Color_End - Color_Start) / (Img_Size[0] + Img_Size[1] - 2)
                _Channel_Color[i,j] = Color_Cur
    else:
        print('Filling_Type Error !')

    return _Channel_Color

def Get_Image(Img_Size, Edge_Dis):
    Angle_Value = random.randint(0,3)
    Object_Info = Get_Objecet_Info(Angle_Value, Img_Size, Edge_Dis)
    Filling_Type_0 = random.randint(0,3)
    Filling_Type_1 = random.randint(0,3)
    Filling_Type_2 = random.randint(0,3)
    Object_Color_0 = random.randint(15,240)
    Object_Color_1 = random.randint(15,240)
    Object_Color_2 = random.randint(15,240)
    Channel_Color_0 = Get_Channel(Img_Size, Filling_Type_0, Object_Color_0)
    Channel_Color_1 = Get_Channel(Img_Size, Filling_Type_1, Object_Color_1)
    Channel_Color_2 = Get_Channel(Img_Size, Filling_Type_2, Object_Color_2)
    
    Channel_0 = Object_Filling(Angle_Value, Object_Info, Img_Size, Channel_Color_0, Object_Color_0)
    Channel_1 = Object_Filling(Angle_Value, Object_Info, Img_Size, Channel_Color_1, Object_Color_1)
    Channel_2 = Object_Filling(Angle_Value, Object_Info, Img_Size, Channel_Color_2, Object_Color_2)

    _Image = np.zeros([Img_Size[0], Img_Size[1], 3], np.uint8)

    for i in range(0, Img_Size[0]):
        for j in range(0, Img_Size[1]):
            _Image[i,j,0] = Channel_0[i,j]
            _Image[i,j,1] = Channel_1[i,j]
            _Image[i,j,2] = Channel_2[i,j]

    return _Image, Angle_Value
    

def main():
    Filename1 = 'Input/Size_100/'
    Filename2 = 'Output/Target_100.txt'
    Filename3 = 'Output/Target_Config_100.txt'
    Img_Number = 10000
    Img_Height = 100
    Img_Width = 100
    Edge_Dis = 2
    Img_Size = [Img_Height, Img_Width]
    Target_List = np.zeros([Img_Number, 1])

    file=open(Filename2,'w')

    count = np.zeros([5, 1])

    for i in range(0, Img_Number):
        print('Time: %04d'%i)
        Image, Target_Value = Get_Image(Img_Size, Edge_Dis)
        if Target_Value == 0:
            count[0] += 1
        elif Target_Value == 1:
            count[1] += 1
        elif Target_Value == 2:
            count[2] += 1
        elif Target_Value == 3:
            count[3] += 1
        else:
            count[4] += 1         
        Name = Filename1 + '%04d.png'%i
        imsave(Name, Image)
        file.write(str(Target_Value) + '\n')

    file.close()
    file = open(Filename3,'w')
    file.write(str(count))	
    file.close()
    print('GetData_Color_100 Over !')

main()
os.system('pause')
