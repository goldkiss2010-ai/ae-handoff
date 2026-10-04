"""Render reference point previews directly from FLD1 (not an AE render).

Requires NumPy, Pillow and ffmpeg on PATH. The FLD1/AE workflow needs none of
these preview-only dependencies when using already generated caches.
"""
import argparse
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PALETTE = {'vortex-ring':(80,210,255),'smoke-plume':(180,210,240),
           'ripple-sheet':(250,175,90),'wind-tunnel':(90,240,195),
           'plane-to-torus':(180,130,255)}

def rotation(degrees):
    x,y,z = np.radians(degrees)
    cx,sx,cy,sy,cz,sz=np.cos(x),np.sin(x),np.cos(y),np.sin(y),np.cos(z),np.sin(z)
    return np.array(((cz,-sz,0),(sz,cz,0),(0,0,1))) @ np.array(((cy,0,sy),(0,1,0),(-sy,0,cy))) @ np.array(((1,0,0),(0,cx,-sx),(0,sx,cx)))

def font(size):
    candidates=('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf')
    for p in candidates:
        if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def load(path, max_points):
    meta=json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
    with path.open('rb') as f:
        magic,version,n,frames,rate,stride,res=struct.unpack('<4sIIIdII',f.read(32))
    if (magic,version,rate,stride,res)!=(b'FLD1',1,1.0,8,0):raise ValueError('Expected normalized FLD1')
    if path.stat().st_size!=32+frames*n*32:raise ValueError('Unexpected file length')
    cache=np.memmap(path,dtype='<f4',mode='r',offset=32,shape=(frames,n,8))
    ids=np.arange(min(n,max_points))
    # Random uniform source positions make a prefix a useful reference preview.
    data=np.array(cache[:,ids,:],dtype=np.float64)
    return meta,data

def at(data,q):
    j=min(int(q),len(data)-1); k=min(j+1,len(data)-1); s=q-j
    h00,h10,h01,h11=2*s**3-3*s*s+1,s**3-2*s*s+s,-2*s**3+3*s*s,s**3-s*s
    return h00*data[j,:,:3]+h10*data[j,:,3:6]+h01*data[k,:,:3]+h11*data[k,:,3:6]

def render(meta,data,q,frame,view,width=960,height=600):
    mat,center,scale=view
    xyz=at(data,q)@mat.T
    x=np.rint(width/2+(xyz[:,0]-center[0])*scale).astype(int)
    y=np.rint(height/2+10-(xyz[:,1]-center[1])*scale).astype(int)
    j=min(int(q),len(data)-1);k=min(j+1,len(data)-1);s=q-j
    visibility=(1-s)*data[j,:,6]+s*data[k,:,6]
    # Match the current AE Dot visibility gate, without inventing opacity fade.
    ok=(x>=0)&(x<width)&(y>=75)&(y<height-45)&(visibility>.01)
    x,y=x[ok],y[ok]
    mass=np.zeros((height,width),dtype=np.float32)
    np.add.at(mass,(y,x),1)
    intensity=1-np.exp(-.40*mass)
    gray=Image.fromarray(np.uint8(intensity*255))
    bloom=np.asarray(gray.filter(ImageFilter.GaussianBlur(1.5)),dtype=np.float32)/255
    light=np.minimum(1,intensity+.85*bloom)
    base=np.array((6,10,20),dtype=float)
    color=np.array(PALETTE[meta['asset']],dtype=float)
    rgb=np.uint8(np.clip(base[None,None,:]+light[:,:,None]*color,0,255))
    image=Image.fromarray(rgb)
    draw=ImageDraw.Draw(image)
    title=meta['asset'].replace('-',' ').title()
    draw.text((28,20),title,font=font(24),fill=(225,235,245))
    draw.text((28,51),f"{meta['particle_count']:,} cached particles / {len(data)} stored samples",font=font(14),fill=(125,155,180))
    draw.text((28,height-31),'FLD1 reference preview | subset of points | AE appearance will differ',font=font(13),fill=(110,140,165))
    if meta['asset']=='plane-to-torus':
        draw.text((width-190,27),f'Plane -> Torus  {q/(len(data)-1):.0%}',font=font(14),fill=(200,165,255))
    return image

def preview(path,out,fps=24,duration=4,max_points=20000):
    meta,data=load(path,max_points)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    name=meta['asset']
    mat=rotation(meta['suggested_ae']['object_rotation_xyz_degrees'])
    bbox=data[:,:,:3].reshape(-1,3)@mat.T
    lo,hi=bbox.min(axis=0),bbox.max(axis=0)
    span=np.maximum(hi-lo,.1)
    view=(mat,(lo+hi)/2,min(860/span[0],450/span[1]))
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg:raise RuntimeError('ffmpeg is required only to generate preview videos')
    command=[ffmpeg,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','960x600','-r',str(fps),'-i','-',
             '-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(out/(name+'.mp4'))]
    process=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for frame in range(round(fps*duration)):
            q=(len(data)-1)*frame/(round(fps*duration)-1)
            image=render(meta,data,q,frame,view)
            if frame==round(fps*duration)//2:image.save(out/(name+'.png'))
            if frame in (0,round(fps*duration)-1) and name=='plane-to-torus':
                image.save(out/(name+('-start.png' if frame==0 else '-end.png')))
            process.stdin.write(image.tobytes())
        process.stdin.close()
        if process.wait()!=0:raise RuntimeError('Preview encoder failed')
    finally:
        if process.poll() is None:process.kill();process.wait()
    print('Preview:',name,flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('cache',type=Path)
    p.add_argument('--out',type=Path,default=Path('previews'))
    p.add_argument('--max-points',type=int,default=20000)
    a=p.parse_args()
    files=sorted(a.cache.rglob('*.fld1')) if a.cache.is_dir() else [a.cache]
    if not files:p.error('No FLD1 files found')
    for f in files:preview(f,a.out,max_points=a.max_points)
    if len(files)>1:
        tile=Image.new('RGB',(1440,1350),(6,10,20))
        for i,f in enumerate(files):
            name=json.loads(f.with_suffix('.json').read_text())['asset']
            im=Image.open(a.out/(name+'.png')).resize((720,450))
            tile.paste(im,((i%2)*720,(i//2)*450))
        draw=ImageDraw.Draw(tile)
        x,y=760,950
        lines=[('AE Handoff | Field Assets v01',26),
               ('5 newly generated fields',22),
               ('Quick set: 20,000 particles / 49 samples each',17),
               ('Hero: Vortex Ring, 1,000,000 particles / 17 samples',17),
               ('FLD1 + source + seed/settings + previews',17),
               ('Reference rendering; AE appearance will differ',15),
               ('Smoke and wake are procedural flow models',15)]
        for line,size in lines:
            draw.text((x,y),line,font=font(size),fill=(150,180,205))
            y+=48 if size>=22 else 34
        tile.save(a.out/'overview.png')

if __name__=='__main__':main()
