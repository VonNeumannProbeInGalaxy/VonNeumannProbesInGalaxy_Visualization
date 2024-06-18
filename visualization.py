import pygame
import math
import random
import os

def add_vectors(vec1, vec2):
    
    result = []
    for i in range(3):
        result.append(vec1[i] + vec2[i])
    return result
def subtract_vectors(vec1, vec2):
    
    result = [vec1[i] - vec2[i] for i in range(3)]
    return result
    
def cross_product(vec1, vec2):
    #外积
    result = [
        vec1[1] * vec2[2] - vec1[2] * vec2[1],
        vec1[2] * vec2[0] - vec1[0] * vec2[2],
        vec1[0] * vec2[1] - vec1[1] * vec2[0]
    ]
    return result
def dot_product(vec1, vec2):
    #内积
    result = sum(vec1[i] * vec2[i] for i in range(3))
    return result
    
def normalize_vector(vec):
    #矢量归一化
    length = math.sqrt(sum(vec[i] ** 2 for i in range(3)))
    if length == 0:
        raise ValueError("零向量不能归一化")
    normalized_vec = [vec[i] / length for i in range(3)]
    return normalized_vec   
    
def vector_length(vec):
    #取模
    length = math.sqrt(sum(vec[i] ** 2 for i in range(3)))
    return length
    
def kelvin_to_rgb(temperature):
    #色温转到RGB
    temperature /= 100

    if temperature <= 66:
        red = 255
        green = (-0.60884257109 - 0.00174890002*(temperature-2)+0.40977318429*math.log(temperature - 10))*256
        blue = (-0.99909549742 + 0.00324474355*(temperature - 10)+0.45364683926* math.log(temperature - 10))*256
    else:
        red = (1.38030159086 + 0.00044786845*(temperature - 55) - 0.15785750233*math.log(temperature-55))*256
        green = (1.27627220616 + 0.0003115081*(temperature - 50)-0.11013841706*math.log(temperature-50))*256
        blue = 255

    
    red = max(0, min(255, red))
    green = max(0, min(255, green))
    blue = max(0, min(255, blue))

    return int(red), int(green), int(blue)

def variable_threshold(variable):
    if variable > 0.01:
        return variable
    
    return 0.01
def scalar_multiply(scalar, vec):
    
    result = [scalar * vec[i] for i in range(3)]
    return result

pygame.init()


width=1000
height=600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("可视化")


RED = (255, 0, 0)
BLUE = (0, 0, 255)
Black=(0,0,0)

PI=3.1415926535
dragging = False  
posx=0
posy=800
theta=0
phi=0
r=20
cenposcam=(0,0,0)#摄影机位置
reposcam=(0,0,0)
poscam=(0,0,0)
vecx=(0,0,0)
vecy=(0,0,0)
vecz=(0,0,0)
stars=[]
target=(0,0,0)
totar=False

nstar0=1145
stardensity=0.004

rmap0=(nstar0*6/(stardensity*PI))**(1/3)/2

for i in range(0,math.ceil(nstar0*6/PI)):
    xstar0=random.uniform(-rmap0, rmap0)
    ystar0=random.uniform(-rmap0, rmap0)
    zstar0=random.uniform(-rmap0, rmap0)
    if xstar0**2+ystar0**2+zstar0**2<rmap0**2:
        stars.append([(xstar0,ystar0,zstar0),(0,0,0),0,(0,0),random.uniform(1000, 12000)])
	    #             绝对坐标                相对坐标 距 屏坐标 色温
ctoss=[]
ctos=(0,0,0)
posonscx=0
posonscy=0
mposx=0
mposy=0
# 主循环
running = True

current_path = os.path.dirname(__file__)
tieimg=pygame.image.load(os.path.join(current_path, 'gaussian.png'))
tieimg1=pygame.image.load(os.path.join(current_path, 'gaussian1.png'))
tieimg2=pygame.image.load(os.path.join(current_path, 'gaussian2.png'))
tieimg3=pygame.image.load(os.path.join(current_path, 'gaussian3.png'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            size = event.size
            width, height = size
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 上滚拉近
                r /= 1.2
            elif event.button == 5:  # 下滚拉远
                r *= 1.2
            elif event.button == 1:  # 检测鼠标左键
               
                    dragging = True
                    offset_x = event.pos[0] - posx  
                    offset_y = event.pos[1] - posy
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                posx = event.pos[0] - offset_x 
                posy = event.pos[1] - offset_y

    # 绘制屏幕
    if totar==True:
        if vector_length(subtract_vectors(target,cenposcam))>10:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.2,normalize_vector(subtract_vectors(target,cenposcam))))
        elif vector_length(subtract_vectors(target,cenposcam))>3:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.1,normalize_vector(subtract_vectors(target,cenposcam))))
        elif vector_length(subtract_vectors(target,cenposcam))>1:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.05,normalize_vector(subtract_vectors(target,cenposcam))))
        else:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.05*vector_length(subtract_vectors(target,cenposcam)),normalize_vector(subtract_vectors(target,cenposcam))))

        if vector_length(subtract_vectors(target,cenposcam))<0.0001:
            totar=False
    if posx>width:
        posx-=width
    elif posx<0:
        posx+=width
    if posy>height:
        posy=height
    elif posy<0:
        posy=0
    theta=4*PI*posx/width
    phi=PI*(posy-0.5*height)/height
    reposcam=(r*math.cos(theta)*math.cos(phi),r*math.sin(theta)*math.cos(phi),r*math.sin(phi))#相机相对柱坐标中心天体
    poscam=add_vectors(reposcam,cenposcam)#相机绝对坐标
    vecx=normalize_vector(cross_product((0,0,1),reposcam))#相机局部坐标架
    vecy=normalize_vector(cross_product(reposcam,vecx))
    vecz=normalize_vector(reposcam)
    for element in stars:
        element[1]=subtract_vectors(element[0],poscam)
        element[2]=vector_length(element[1])
        element[3]=(width*(0.5+0.5*dot_product(vecx,element[1])/(-(dot_product(vecz,element[1])))),
        height*(0.5+0.5*width/height*dot_product(vecy,element[1])/(-(dot_product(vecz,element[1])))))
    stars = sorted(stars, key=lambda x: -x[2])
    screen.fill((0,0,0))
    
    for i in range(len(stars)):
        color=kelvin_to_rgb(stars[i][4])
        if dot_product(stars[i][1],vecz)<0 and stars[i][3][0]>0 and stars[i][3][0]<width and stars[i][3][1]>0 and stars[i][3][1]<height and 100/math.sqrt(variable_threshold((stars[i][2])**2-1))>0.2:
            starrad=16/math.sqrt(variable_threshold((stars[i][2])**2-1))
            if starrad>=1:
                pygame.draw.circle(screen,color,stars[i][3],starrad)
            else:
                pygame.draw.rect(screen,color,[stars[i][3][0],stars[i][3][1],1,1],1)
            if stars[i][2]<8:
                modified_image = tieimg.copy()
                AA=[0,0,0,128]
                ll=1500/math.sqrt(variable_threshold((stars[i][2])**2-1))
                for t in range(3):
                    AA[t]=color[t]
                modified_image.fill(AA, None, pygame.BLEND_RGBA_MULT)
                modified_image=pygame.transform.scale(modified_image,(ll,ll))
                screen.blit(modified_image,(stars[i][3][0]-0.5*ll,stars[i][3][1]-0.5*ll))
            elif stars[i][2]<16:
                modified_image = tieimg1.copy()
                AA=[0,0,0,128]
                ll=1500/math.sqrt(variable_threshold((stars[i][2])**2-1))
                for t in range(3):
                    AA[t]=color[t]
                modified_image.fill(AA, None, pygame.BLEND_RGBA_MULT)
                modified_image=pygame.transform.scale(modified_image,(ll,ll))
                screen.blit(modified_image,(stars[i][3][0]-0.5*ll,stars[i][3][1]-0.5*ll))
            elif stars[i][2]<32:
                modified_image = tieimg2.copy()
                AA=[0,0,0,128]
                ll=1500/math.sqrt(variable_threshold((stars[i][2])**2-1))
                for t in range(3):
                    AA[t]=color[t]
                modified_image.fill(AA, None, pygame.BLEND_RGBA_MULT)
                modified_image=pygame.transform.scale(modified_image,(ll,ll))
                screen.blit(modified_image,(stars[i][3][0]-0.5*ll,stars[i][3][1]-0.5*ll))
            elif stars[i][2]<96:
                modified_image = tieimg3.copy()
                AA=[0,0,0,128]
                ll=1500/math.sqrt(variable_threshold((stars[i][2])**2-1))
                for t in range(3):
                    AA[t]=color[t]
                modified_image.fill(AA, None, pygame.BLEND_RGBA_MULT)
                modified_image=pygame.transform.scale(modified_image,(ll,ll))
                screen.blit(modified_image,(stars[i][3][0]-0.5*ll,stars[i][3][1]-0.5*ll))
            if pygame.mouse.get_pressed()[2]==True:
                if (pygame.mouse.get_pos()[0]-stars[i][3][0])**2+(pygame.mouse.get_pos()[1]-stars[i][3][1])**2 < (100/math.sqrt(variable_threshold((stars[i][2])**2-1)))**2:
                    totar=True
                    target=stars[i][0]

                           
            
    pygame.display.flip()

    
pygame.quit()