from PIL import Image,ImageDraw, ImageFont
import qrcode
import json
import os
import threading

thread_lock = threading.BoundedSemaphore(value=3)
background_img_path = "./template/qilian.jpg"

def addtext(img, text):
    draw = ImageDraw.Draw(img)
    ttfront = ImageFont.truetype('simhei.ttf', 125)#字体大小
    draw.text((1860, 4275),text,fill=(0,25,25), font=ttfront)#文字位置，内容，字体

def addqrcode(img, text):
    qrcode_img = qrcode.make(text, border = 0)
    qrcode_img = qrcode_img.resize((1550,1450))

    origin = (1485,2780,1485+qrcode_img.size[0],2780+qrcode_img.size[1])
    img.paste(qrcode_img, origin)

def createImg(path, sn):
    qrcode_url =  "https://pay.cnqilian.com/dist/?name=store&sn=" + sn
    base_img = Image.open(background_img_path)
    addtext(base_img, 'NO.'+sn)
    addqrcode(base_img, qrcode_url)
    base_img.save(path+ sn+'.jpg')
    base_img.close()
    thread_lock.release()

def main():
    with open('./example.json','r') as f:
        t = f.read()
        list = json.loads(t)
        records = list['RECORDS']
        length = len(records)

        if os.path.exists('output') is not True:
            os.mkdir('output')
        for i in range(0,int(length/1000)):
            path = './output/'+str(i)+'/'
            if os.path.exists(path) is not True:
                os.mkdir(path)

        for i in range(0,length):
            print('第{}条记录'.format(i))
            path = './output/'+str(int(i/1000))+'/'
            thread_lock.acquire()  # 线程锁
            T = threading.Thread(target = createImg, args=(path, str(records[i]['bh']), ))
            T.start()

if __name__ == '__main__':
    main()