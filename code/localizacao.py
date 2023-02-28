#-----Script do algoritmo de localização do LANDROVER-----#

x = 0
y = 0
tempo = 2
vel = 40 #default
d = 'F' #default
h = 'H' #default
#irei considerar a velocidade constante, logo acelaração = 0

if(h=='H'):
    if(d=='F'):
        if(vel==10):
            x = x + (4.826/0.5)*tempo
        elif(vel==20):
            x = x + (14.986/0.5)*tempo
        elif(vel==30):
            x = x + (27.178/0.5)*tempo
        elif(vel==40):
            x = x + (40.132/0.5)*tempo
        elif(vel==50):
            x = x + (59.436/0.5)*tempo
        elif(vel==60):
            x = x + (78.486/0.5)*tempo
        elif(vel==70):
            x = x + (106.426/0.5)*tempo
        elif(vel==80):
            x = x + (129.54/0.5)*tempo
        elif(vel==90):
            x = x + (153.924/0.5)*tempo
        else:
            x = x + (169.672/0.5)*tempo
    if(d=='B'):
        if(vel==10):
            x = x - (3.556/0.5)*tempo
        elif(vel==20):
            x = x - (10.414/0.5)*tempo
        elif(vel==30):
            x = x - (18.796/0.5)*tempo
        elif(vel==40):
            x = x - (30.48/0.5)*tempo
        elif(vel==50):
            x = x - (43.688/0.5)*tempo
        elif(vel==60):
            x = x - (60.198/0.5)*tempo
        elif(vel==70):
            x = x - (76.454/0.5)*tempo
        elif(vel==80):
            x = x - (91.44/0.5)*tempo
        elif(vel==90):
            x = x - (105.156/0.5)*tempo
        else:
            x = x - (115.062/0.5)*tempo
if(h=='V'):
    if(d=='F'):
        if(vel==10):
            y = y + (4.826/0.5)*tempo
        elif(vel==20):
            y = y + (14.986/0.5)*tempo
        elif(vel==30):
            y = y + (27.178/0.5)*tempo
        elif(vel==40):
            y = y + (40.132/0.5)*tempo
        elif(vel==50):
            y = y + (59.436/0.5)*tempo
        elif(vel==60):
            y = y + (78.486/0.5)*tempo
        elif(vel==70):
            y = y + (106.426/0.5)*tempo
        elif(vel==80):
            y = y + (129.54/0.5)*tempo
        elif(vel==90):
            y = y + (153.924/0.5)*tempo
        else:
            y = y + (169.672/0.5)*tempo
    if(d=='B'):
        if(vel==10):
            y = y - (3.556/0.5)*tempo
        elif(vel==20):
            y = y - (10.414/0.5)*tempo
        elif(vel==30):
            y = y - (18.796/0.5)*tempo
        elif(vel==40):
            y = y - (30.48/0.5)*tempo
        elif(vel==50):
            y = y - (43.688/0.5)*tempo
        elif(vel==60):
            y = y - (60.198/0.5)*tempo
        elif(vel==70):
            y = y - (76.454/0.5)*tempo
        elif(vel==80):
            y = y - (91.44/0.5)*tempo
        elif(vel==90):
            y = y - (105.156/0.5)*tempo
        else:
            y = y - (115.062/0.5)*tempo
print(x + y)