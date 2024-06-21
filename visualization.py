import pygame
import math
import random
import os
import time
import string

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

def variable_threshold001(variable):
    if variable > 0.01:
        return variable
    
    return 0.01
def variable_threshold1(variable):
    if variable < 1:
        return variable
    
    return 1
def scalar_multiply(scalar, vec):
    #数乘
    result = [scalar * vec[i] for i in range(3)]
    return result

def randomname():
    letters = ''.join(random.choices(string.ascii_letters, k=6))
    return letters
pygame.init()


width=1000
height=600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

pygame.display.set_caption("可视化")
messagewidthrate=0.25
messageheightrate=0.33

RED = (255, 0, 0)
BLUE = (0, 0, 255)
Black=(0,0,0)
font = pygame.font.Font(None, int(height/32.0))
PI=3.1415926535
dragging = False  
posx=0
posy=800
theta=0
phi=0
r=20
rtarget=20
cenposcam=(0,0,0)#摄影机位置
reposcam=(0,0,0)
poscam=(0,0,0)
vecx=(0,0,0)
vecy=(0,0,0)
vecz=(0,0,0)
stars=[]
starmessages={}
target=(0,0,0)
targetname=''
targetcolor=[0,0,0,255]
targetcloud=0
totar=False
text=''
nstar0=1145
stardensity=0.004

rmap0=(nstar0*6/(stardensity*PI))**(1/3)/2
print(rmap0)
for i in range(0,math.ceil(nstar0*6/PI)):
    xstar0=random.uniform(-rmap0, rmap0)
    ystar0=random.uniform(-rmap0, rmap0)
    zstar0=random.uniform(-rmap0, rmap0)
    name=randomname()
    if xstar0**2+ystar0**2+zstar0**2<rmap0**2:
        starmessages[name]=name+'s introduction'+'\n'+'testline,114514'
        stars.append([(xstar0,ystar0,zstar0),(0,0,0),0,(0,0),random.uniform(1000, 12000),random.uniform(1/10000, 10000000),random.randint(0,4),name,random.uniform(0.0005, 0.1)*0.000016])
	    #             绝对坐标               相对坐标 距 屏坐标           色温                     功率 倍太阳                       类型          编号         半径
ctoss=[]#                                                                                                               类型：戴森云铺设规模
ctos=(0,0,0)#          0                        1    2   3               4                        5                                6             7           8
posonscx=0
posonscy=0
mposx=0
mposy=0

scroll_y = 0
targetscroll_y=0
messagex=1000
messagextarget=0
timelast=time.time()
deltatime=0
running = True
clicktime=0
deltaclicktime=1
doubleclick=False
showmessage=False
nearstars=0
current_path = os.path.dirname(__file__)
tieimg=pygame.image.load(os.path.join(current_path, 'gaussian.png'))#贴图加载
tieimg1=pygame.image.load(os.path.join(current_path, 'gaussian1.png'))
tieimg2=pygame.image.load(os.path.join(current_path, 'gaussian2.png'))
tieimg3=pygame.image.load(os.path.join(current_path, 'gaussian3.png'))
mesimg=pygame.image.load(os.path.join(current_path, 'stage0.png'))#贴图加载
mesimg1=pygame.image.load(os.path.join(current_path, 'stage1.png'))
mesimg2=pygame.image.load(os.path.join(current_path, 'stage2.png'))
mesimg3=pygame.image.load(os.path.join(current_path, 'stage3.png'))
mesimg4=pygame.image.load(os.path.join(current_path, 'stage3.png'))
# 主循环________________________________以上为参数和变量们
while running:
    deltatime=time.time()-timelast
    timelast=time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            size = event.size
            width, height = size
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        else:
            if showmessage==False or (showmessage==True and pygame.mouse.get_pos()[0]/width<(1-messagewidthrate)):#文字区域外操作
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # 上滚拉近
                        rtarget /= 1.2
                    elif event.button == 5:  # 下滚拉远
                        rtarget *= 1.2
                    elif event.button == 1:  # 检测鼠标左键
                        
                            dragging = True
                            offset_x = event.pos[0] - posx  
                            offset_y = event.pos[1] - posy
                            deltaclicktime=time.time()-clicktime
                            clicktime=time.time()
                            mposx=event.pos[0]
                            mposy=event.pos[1]
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  
                        dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        posx = event.pos[0] - offset_x 
                        posy = event.pos[1] - offset_y
            elif showmessage==True and pygame.mouse.get_pos()[0]/width>(1-messagewidthrate):#文字区域内操作
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # 上滚
                        if targetscroll_y<0:
                            targetscroll_y+=int(height/32.0)
                        else:
                            targetscroll_y=0
                    elif event.button == 5:  # 下滚
                        targetscroll_y-=int(height/32.0)
    if doubleclick==True:
        deltaclicktime=1
    doubleclick=False

    if deltaclicktime<0.3:
        doubleclick=True
    if showmessage==True:
        messagextarget=0
    else:
        messagextarget=1.5*(width*messagewidthrate)
    scroll_y+=(targetscroll_y-scroll_y)*variable_threshold1(60*deltatime*0.3)
    r+=(rtarget-r)*variable_threshold1(60*deltatime*0.16)
    messagex+=(messagextarget-messagex)*variable_threshold1(60*deltatime*0.3)
    if totar==True:#视角移动
        if vector_length(subtract_vectors(target,cenposcam))>10:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.2*60*deltatime,normalize_vector(subtract_vectors(target,cenposcam))))
        elif vector_length(subtract_vectors(target,cenposcam))>3:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.1*60*deltatime,normalize_vector(subtract_vectors(target,cenposcam))))
        elif vector_length(subtract_vectors(target,cenposcam))>1:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.05*60*deltatime,normalize_vector(subtract_vectors(target,cenposcam))))
        else:
            cenposcam=add_vectors(cenposcam,scalar_multiply(0.05*60*deltatime*vector_length(subtract_vectors(target,cenposcam)),normalize_vector(subtract_vectors(target,cenposcam))))

        if vector_length(subtract_vectors(target,cenposcam))<pow(10,-8):
            totar=False

    if posx>width:#虚拟鼠标位置限定
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
    for element in stars:#星体各项数据   屏幕远1ly，宽1ly
        element[1]=subtract_vectors(element[0],poscam)
        element[2]=vector_length(element[1])
        element[3]=(width*(0.5+0.5*dot_product(vecx,element[1])/(-(dot_product(vecz,element[1])))),
        height*(0.5+0.5*width/height*dot_product(vecy,element[1])/(-(dot_product(vecz,element[1])))))
    stars = sorted(stars, key=lambda x: -x[2])#由远到近排序，建立遮挡关系

    #右侧背景
    backgroundrect=pygame.Rect(width*(1-messagewidthrate)+messagex,0,width*messagewidthrate,height)

    upbackgroungrect=pygame.Rect(width*(1-messagewidthrate)+messagex,0,width*messagewidthrate,height*messageheightrate)
    if showmessage==True:
        text=starmessages[targetname]

    screen.fill((0,0,0))
    
    for i in range(len(stars)):#星星绘制
        color=scalar_multiply(pow(stars[i][5],1/8)/8/(variable_threshold001(100*(stars[i][2]))/100),kelvin_to_rgb(stars[i][4]))
        color0=kelvin_to_rgb(stars[i][4])
        if dot_product(stars[i][1],vecz)<0 and stars[i][3][0]>0 and stars[i][3][0]<width and stars[i][3][1]>0 and stars[i][3][1]<height :#只渲染可见部分
            starrad=width/math.sqrt(variable_threshold001((stars[i][2]/stars[i][8])**2-1))
            ll=100/pow(variable_threshold001(10000*(stars[i][2]))/10000,0.8)*(0.5-0.5*math.tanh(1.5*math.log1p(starrad)))*pow(stars[i][5],1/8)
            if starrad>=1:
                pygame.draw.circle(screen,color0,stars[i][3],starrad)#恒星本体，原色
            if ll<10:
                pygame.draw.rect(screen,scalar_multiply(variable_threshold1(ll*0.5),color0),[stars[i][3][0],stars[i][3][1],1,1],1)#处理过远不显示的情况
            AA=[0,0,0,255]
            
            if ll>1024:
                ll=1024       
            if ll>128:
                modified_image = tieimg.copy()
            elif ll>64:
                modified_image = tieimg1.copy()
            elif ll>32:
                modified_image = tieimg2.copy()
            elif ll<=32:
                modified_image = tieimg3.copy()
            for t in range(3):
                if color0[t]<255:
                    AA[t]=color0[t]
                else:
                    AA[t]=255
            if ll>1:
                modified_image.fill(AA, None, pygame.BLEND_RGBA_MULT)
                modified_image=pygame.transform.smoothscale(modified_image,(ll,ll))
                screen.blit(modified_image,(stars[i][3][0]-0.5*ll,stars[i][3][1]-0.5*ll))
            if doubleclick==True:#左键双击移动坐标系
                if (pygame.mouse.get_pos()[0]-stars[i][3][0])**2+(pygame.mouse.get_pos()[1]-stars[i][3][1])**2 < (max(ll/8,starrad))**2:
                    totar=True
                    target=stars[i][0]
            if pygame.mouse.get_pressed()[2]==True and (showmessage==False or (showmessage==True and pygame.mouse.get_pos()[0]/width<(1-messagewidthrate))):#右键单击显示信息
                
                if (pygame.mouse.get_pos()[0]-stars[i][3][0])**2+(pygame.mouse.get_pos()[1]-stars[i][3][1])**2 < (max(ll/8,starrad))**2:
                    targetname=stars[i][7]
                    showmessage=True
                    targetcolor=[0,0,0,255]
                    targetcloud=stars[i][6]
                    for t in range(3):
                        targetcolor[t]=color0[t]
                    nearstars=nearstars+1
    if pygame.mouse.get_pressed()[2]==True and (showmessage==False or (showmessage==True and pygame.mouse.get_pos()[0]/width<(1-messagewidthrate))):
        if nearstars==0:
            showmessage=False
            targetname=''
        else:
            nearstars=0
    #信息框绘制
    font = pygame.font.Font(None, int(height/32.0))
    pygame.draw.rect(screen,(0,0,0),backgroundrect)
    y0=0
    for line in text.splitlines():
        text_surface = font.render(line, True, (255,255,255))
        screen.blit(text_surface, (width*(1-messagewidthrate)+messagex,y0+height*messageheightrate+scroll_y))
        y0+= int(height/32.0)
    pygame.draw.rect(screen,(0,0,0),upbackgroungrect)
    if targetcloud==0:
        momesimg=mesimg.copy()
    elif targetcloud==1:
        momesimg=mesimg1.copy()
    elif targetcloud==2:
        momesimg=mesimg2.copy()
    elif targetcloud==3:
        momesimg=mesimg3.copy()
    elif targetcloud==4:
        momesimg=mesimg4.copy()
    momesimg.fill(targetcolor, None, pygame.BLEND_RGBA_MULT)
    momesimg=pygame.transform.smoothscale(momesimg,(3/2*height*messageheightrate,height*messageheightrate))
    crop_rect=pygame.Rect(0.5*3/2*height*messageheightrate-0.5*width*messagewidthrate,0.5*height*messageheightrate-0.5*height*messageheightrate,width*messagewidthrate,height*messageheightrate)
    cropped_image=pygame.Surface((width*messagewidthrate,height*messageheightrate))
    cropped_image.blit(momesimg,(0,0),crop_rect)
    screen.blit(cropped_image,(width*(1-messagewidthrate)+messagex,0))
    pygame.display.flip()
    print()
pygame.quit()