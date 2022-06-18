from PIL import Image,ImageDraw, ImageFont
import qrcode
import json
import os
import threading

thread_lock = threading.BoundedSemaphore(value=3)
background_img_path = "./template/qilian_1.jpg"

def addtext(img, text):
    draw = ImageDraw.Draw(img)
    ttfront = ImageFont.truetype('simhei.ttf', 125)#字体大小
    draw.text((1852, 4696),text,fill=(0,25,25), font=ttfront)#文字位置，内容，字体

def addqrcode(img, text):
    qrcode_img = qrcode.make(text, border = 0)
    qrcode_img = qrcode_img.resize((1586,1586))

    origin = (1455,3057,1455+qrcode_img.size[0],3057+qrcode_img.size[1])
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

        for i in range(0,length):
            print('第{}条记录'.format(i))
            path = './output/'
            thread_lock.acquire()  # 线程锁
            T = threading.Thread(target = createImg, args=(path, str(records[i]['bh']), ))
            T.start()
            if i ==  0:
                break

if __name__ == '__main__':
    main()
