# Warianty zdjęć galerii jednostek: 480 i 1200 px (tylko pomniejszanie), WebP + JPG. Źródła: _img/u/<jednostka>/
import json, os, glob
from PIL import Image, ImageOps
import concurrent.futures as cf

def proc(k):
    res = []
    for f in sorted(glob.glob(f'_img/u/{k}/*')):
        if os.path.getsize(f) < 1000: continue
        try: im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
        except Exception as e: print('pominięte', f, e); continue
        n = os.path.splitext(os.path.basename(f))[0]; W, H = im.size; ws = []
        os.makedirs(f'assets/img/j/{k}', exist_ok=True)
        for w in (480, 1200):
            ww = min(w, W)
            if ww in ws: continue
            r = im.resize((ww, round(H * ww / W)), Image.LANCZOS) if ww < W else im
            r.save(f'assets/img/j/{k}/{n}-{ww}.jpg', quality=80, optimize=True, progressive=True)
            r.save(f'assets/img/j/{k}/{n}-{ww}.webp', quality=78, method=5)
            ws.append(ww)
        res.append([n, ws, W, H])
    return k, res

if __name__ == '__main__':
    plan = json.load(open('_img/galerie.json'))
    out = {}
    with cf.ProcessPoolExecutor(6) as ex:
        for k, res in ex.map(proc, plan): out[k] = res
    json.dump(out, open('_img/galerie-ws.json', 'w'), indent=0)
    print({k: len(v) for k, v in out.items()})
