import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

a = Image.open('logo/master.png').convert('RGBA').split()[3]
m = a.crop(a.point(lambda v: 255 if v > 40 else 0).getbbox())

def crown(width, bold=0, S=3, fill=False):
    W = width * S
    H = int(m.height * W / m.width)
    bn = np.array(m.resize((W, H), Image.BICUBIC)) > 110
    if bold:
        bn = ndi.distance_transform_edt(~bn) <= bold * S
    if fill:
        bn = ndi.binary_fill_holes(bn)
    f = Image.fromarray((bn * 255).astype('uint8'))
    f = f.filter(ImageFilter.GaussianBlur(0.7 * S))
    return f.resize((width, int(H / S)), Image.LANCZOS)

def gold(mask):
    w, h = mask.size
    t = np.linspace(0, 1, h)[:, None]
    top = np.array([255, 241, 184.])
    mid = np.array([224, 176, 74.])
    bot = np.array([150, 100, 25.])
    c = np.where(t < 0.5, top + (mid - top) * (t / 0.5),
                 mid + (bot - mid) * ((t - 0.5) / 0.5))
    im = Image.fromarray(np.repeat(c[:, None, :], w, axis=1).astype('uint8'))
    im = im.convert('RGBA')
    im.putalpha(mask)
    return im

def canvas(size, cw, bold, bg=None):
    cv = Image.new('RGBA', (size, size), bg or (0, 0, 0, 0))
    c = gold(crown(cw, bold))
    cv.alpha_composite(c, ((size - c.width) // 2, (size - c.height) // 2))
    return cv

os.makedirs('assets', exist_ok=True)
os.makedirs('notif', exist_ok=True)
canvas(1024, 660, 5).save('assets/icon-foreground.png')
Image.new('RGB', (1024, 1024), (0, 0, 0)).save('assets/icon-background.png')
canvas(1024, 700, 5, (0, 0, 0, 255)).convert('RGB').save('assets/icon-only.png')
sp = canvas(2732, 1000, 7, (0, 0, 0, 255)).convert('RGB')
sp.save('assets/splash.png')
sp.save('assets/splash-dark.png')
canvas(1152, 760, 6).save('notif/splash_icon.png')
canvas(256, 200, 2, (0, 0, 0, 255)).convert('RGB').save('notif/ic_large_supreme.png')
s = crown(84, 2.5, S=4, fill=True)
w = Image.new('RGBA', s.size, (255, 255, 255, 255))
w.putalpha(s)
o = Image.new('RGBA', (96, 96), (0, 0, 0, 0))
o.alpha_composite(w, ((96 - s.width) // 2, (96 - s.height) // 2))
o.save('notif/ic_stat_supreme.png')
print('assets ok')
