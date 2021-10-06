from PIL import Image,ImageDraw, ImageFont
import qrcode
import json

def addtext(img, text):
    draw = ImageDraw.Draw(img)
    ttfront = ImageFont.truetype('simhei.ttf', 125)#字体大小
    draw.text((1860, 4275),text,fill=(0,25,25), font=ttfront)#文字位置，内容，字体
    # img.show()

def addqrcode(img, text):
    qrcode_img = qrcode.make(text, border = 0)
    print(qrcode_img.size)
    qrcode_img = qrcode_img.resize((1550,1450))
    print(qrcode_img.size)

    origin = (1485,2780,1485+qrcode_img.size[0],2780+qrcode_img.size[1])
    img.paste(qrcode_img, origin)

# 读取模板图片
base_img = Image.open('./qrcode_bg_sn.png')
# print(base_img.size)  # (4501, 6751)

# sn = '1026730337'
# qrcode_url =  "https://pay.cnqilian.com/dist/?name=store&sn=" + sn
# addtext(base_img, 'NO.'+sn)
# addqrcode(base_img, qrcode_url)
# base_img.show()

with open('./qrcode.json','r') as f:
    t = f.read()
    list = json.loads(t)
    print(list['RECORDS'][0])
    print(type(list['RECORDS'][0]['bh']))

    records = list['RECORDS']
    for i in range(0,1000):
        print(records[i])
        base_img = Image.open('./qrcode_bg_sn.png')
        sn = str(records[i]['bh'])
        qrcode_url =  "https://pay.cnqilian.com/dist/?name=store&sn=" + sn
        addtext(base_img, 'NO.'+sn)
        addqrcode(base_img, qrcode_url)
        base_img.save('./output/'+sn+'.png')
        # base_img.show()
