from PIL import Image,ImageDraw, ImageFont
import qrcode
import json
import os
import threading

thread_lock = threading.BoundedSemaphore(value=3)

def addtext(img, text):
    draw = ImageDraw.Draw(img)
    ttfront = ImageFont.truetype('simhei.ttf', 125)#字体大小
    draw.text((1860, 4275),text,fill=(0,25,25), font=ttfront)#文字位置，内容，字体

def addqrcode(img, text):
    qrcode_img = qrcode.make(text, border = 0)
    qrcode_img = qrcode_img.resize((1550,1450))

    origin = (1485,2780,1485+qrcode_img.size[0],2780+qrcode_img.size[1])
    img.paste(qrcode_img, origin)

def createImg(sn):
    base_img = Image.open('./qrcode_bg_sn.png')
    qrcode_url =  "https://pay.cnqilian.com/dist/?name=store&sn=" + sn
    addtext(base_img, 'NO.'+sn)
    addqrcode(base_img, qrcode_url)
    base_img.save('./output/'+sn+'.png')
    thread_lock.release()

# 读取模板图片
base_img = Image.open('./qrcode_bg_sn.png')

# 创建存储文件夹
if os.path.exists('output') is not True:
    os.mkdir('output')

with open('./1.json','r') as f:
    t = f.read()
    list = json.loads(t)
    
    records = list['RECORDS']
    for i in range(0,len(records)):
        print('第{}条记录'.format(i))
        thread_lock.acquire()  # 线程锁
        T = threading.Thread(target = createImg, args=(str(records[i]['bh']), ))
        T.start()
        # createImg(str(records[i]['bh']))
