"""Generate FLD1 distribution assets, with bounded frame memory and validation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import struct
import tempfile
import time
import numpy as np
from fields import Field, NAMES, DESCRIPTIONS, ROTATIONS

HEADER = struct.Struct('<4sIIIdII')
PRESETS = {
 'quick': {'count':20000,'samples':49},
 'hero': {'count':1000000,'samples':17},
}

def generate(name, count, samples, seed, out, overwrite=False, asset_license=None):
    if not 1 <= count <= 3000000 or not 2 <= samples <= 100000:
        raise ValueError('Require 1..3,000,000 particles and 2..100,000 samples')
    if seed < 0:
        raise ValueError('Seed must be nonnegative')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    stem = f'{name}-{count}-{samples}'
    path, meta_path = out/(stem+'.fld1'), out/(stem+'.json')
    if not overwrite and (path.exists() or meta_path.exists()):
        raise FileExistsError(f'{stem} already exists; choose a different output directory or --overwrite')
    field = Field(name,count,seed)
    record = np.empty((count,8),dtype='<f4')
    record[:,6], record[:,7] = 1.0, 0.0
    digest = hashlib.sha256()
    lo, hi = np.full(3,np.inf), np.full(3,-np.inf)
    fd, temp = tempfile.mkstemp(prefix=stem+'.',suffix='.tmp',dir=out)
    start = time.perf_counter()
    try:
        with os.fdopen(fd,'wb') as f:
            header = HEADER.pack(b'FLD1',1,count,samples,1.0,8,0)
            f.write(header); digest.update(header)
            for j,(positions, derivatives) in enumerate(field.samples(samples)):
                record[:,:3], record[:,3:6] = positions, derivatives
                if name == 'smoke-plume':
                    record[:,6] = field.visibility(j*4.0/(samples-1))
                if not np.isfinite(record).all():
                    raise ValueError(f'Non-finite value at sample {j}')
                lo = np.minimum(lo,record[:,:3].min(axis=0))
                hi = np.maximum(hi,record[:,:3].max(axis=0))
                block = memoryview(record).cast('B')
                f.write(block); digest.update(block)
                if j == 0 or j == samples-1 or j%8 == 0:
                    print(f'{name}: {j+1}/{samples}',flush=True)
        expected = 32+count*samples*32
        if Path(temp).stat().st_size != expected:
            raise ValueError('Unexpected file length')
        # Only replace the final cache after a complete, validated write.
        if path.exists() and not overwrite:
            raise FileExistsError(path)
        os.replace(temp,path)
        meta = {
            'asset':name,'description':DESCRIPTIONS[name],
            'profile':'point3-pv','particle_count':count,'sample_count':samples,
            'sample_rate':1,'progress_coordinate':'stored_sample_index',
            'velocity':'dx/dq per stored sample interval','length_unit':'unitless',
            'coordinate_system':'right-handed XYZ, Z-up','scalar0':'unused, zero',
            'visibility':('0 before emission, smooth activation after birth; Dot mode uses the visibility threshold'
                          if name == 'smoke-plume' else '1 for all slots; particle identities never recycled'),
            'bounds_min':lo.tolist(),'bounds_max':hi.tolist(),'file_size_bytes':expected,
            'sha256':digest.hexdigest(),'seed':seed,
            'generator':'assets/generators/make_fields.py',
            'settings':{'asset':name,'count':count,'samples':samples,'seed':seed,'internal_phase_span':4.0},
            'environment':{'python':platform.python_version(),'numpy':np.__version__},
            'suggested_playback':{'samples_per_second':(samples-1)/4,'sample_offset':0,
                                  'note':'Host-side presentation suggestion; absolute presentation time is not encoded in FLD1.'},
            'suggested_view':{'initial_rotation_xyz_degrees':ROTATIONS[name],
                              'note':'Optional host-side starting orientation; not part of the FLD1 state contract.'},
            'emission':({'source':[0,0,0],'birth_phase_min':.08,'birth_phase_max':3.98,'activation_phase_span':.15,
                         'slot_policy':'fixed count and identity; hidden stationary slots at emitter until their birth'}
                        if name == 'smoke-plume' else None),
            'playback_note':'Suggested 4-second playback is a DCC setting, not an absolute time encoded in FLD1. Endpoint hold; not a seamless loop.',
            'reproducibility':'Seed and settings retained; byte identity across NumPy/platform versions is not guaranteed.',
            'generator_license':'MIT',
            'asset_license':asset_license,
            'distribution_status':'Output license is chosen by the producer; the generator is MIT. No third-party source media is bundled.'}
        fd2, tmp2 = tempfile.mkstemp(prefix=stem+'.',suffix='.json.tmp',dir=out)
        try:
            with os.fdopen(fd2,'w',encoding='utf-8') as f:
                json.dump(meta,f,ensure_ascii=False,indent=2);f.write('\n')
            os.replace(tmp2,meta_path)
        finally:
            Path(tmp2).unlink(missing_ok=True)
        print(f'Saved {path.name}: {expected/1e6:.1f} MB, {time.perf_counter()-start:.1f}s',flush=True)
        return path, meta_path
    finally:
        Path(temp).unlink(missing_ok=True)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--asset',choices=(*NAMES,'all'),default='all')
    p.add_argument('--preset',choices=PRESETS,default='quick')
    p.add_argument('--count',type=int)
    p.add_argument('--samples',type=int)
    p.add_argument('--seed',type=int,default=20261004)
    p.add_argument('--out',type=Path,default=Path('output'))
    p.add_argument('--overwrite',action='store_true')
    p.add_argument('--asset-license',choices=['CC0-1.0'],default=None,
                   help='Optional dedication of your output; specify only if you hold the required rights. Default: no output license declaration.')
    a = p.parse_args()
    preset=PRESETS[a.preset]
    count = a.count if a.count is not None else preset['count']
    samples = a.samples if a.samples is not None else preset['samples']
    if a.preset == 'hero' and a.asset != 'vortex-ring':
        p.error('Hero preset is for --asset vortex-ring; use --count/--samples for other fields')
    for name in NAMES if a.asset=='all' else (a.asset,):
        generate(name,count,samples,a.seed,a.out/name,a.overwrite,a.asset_license)

if __name__ == '__main__':
    main()
