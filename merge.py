from PIL import Image, ImageEnhance, ImageOps
import os

def merge(background, text, o_path, name):
    try:
        text = ImageOps.invert(Image.open(text))
        w, h = text.size

        bm = 80 #bottom margin, for removing water marks
        text = text.crop((0, 0, w, h-bm))
        text = ImageOps.expand(text, border=bm, fill='black')
        text = text.crop((bm, bm, w+bm, h+bm))
        text = text.convert('RGBA')

        background = ImageEnhance.Brightness(Image.open(background)).enhance(.3)
        background = background.resize((w, h)).convert('RGBA')

        merged = Image.blend(background, text, alpha=0.4).convert("RGB")
        merged = ImageEnhance.Brightness(merged).enhance(1.8)
        merged.save(os.path.join(o_path, str(name))+".jpg")
    except Exception as e:
        print(e)

b_path = "background" #backgroud images path, insta@codingdays
t_path = "quote"   #textual images path, insta@gvoquotes
o_path = "merged" #output images path

background = os.listdir(b_path)
text = os.listdir(t_path)
key = min(len(background), len(text))

idx = 0
for b, t in zip(background[:key], text[:key]):
    b, t = os.path.join(b_path, b), os.path.join(t_path, t)

    print("merging {}".format(idx))
    merge(b, t, o_path, idx)
    idx+=1
