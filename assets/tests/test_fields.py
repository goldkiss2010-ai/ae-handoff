"""Tests of derivatives, field constraints and binary consumer compatibility."""
from pathlib import Path
import json
import struct
import sys
import tempfile
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'generators'))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'core'))
from fields import Field, NAMES
from make_fields import generate
from fld1 import Reader, interpolate

class FieldTests(unittest.TestCase):
    def test_analytic_derivatives_and_hermite_between_samples(self):
        for name in ('vortex-ring','ripple-sheet','plane-to-torus'):
            with self.subTest(name=name):
                field=Field(name,64,12)
                t, eps=1.31,1e-5
                p,v=field.analytic(t)
                numerical=(field.analytic(t+eps)[0]-field.analytic(t-eps)[0])/(2*eps)
                np.testing.assert_allclose(v,numerical,atol=2e-8,rtol=2e-7)
                step=4/32
                p0,v0=field.analytic(t)
                p1,v1=field.analytic(t+step)
                ref=field.analytic(t+.5*step)[0]
                a=np.concatenate((p0[0],v0[0]*step,[1,0]))
                b=np.concatenate((p1[0],v1[0]*step,[1,0]))
                np.testing.assert_allclose(interpolate(a,b,.5,1)[:3],ref[0],atol=6e-5)

    def test_cylinder_boundary_and_integration(self):
        field=Field('wind-tunnel',512,21)
        ang=np.linspace(0,2*np.pi,100,endpoint=False)
        circle=np.column_stack((np.cos(ang),np.sin(ang),np.zeros(100)))
        velocity=field.velocity(circle,1.3)
        np.testing.assert_allclose((circle[:,:2]*velocity[:,:2]).sum(axis=1),0,atol=1e-14)
        for p,v in field.samples(33):
            self.assertGreater(np.hypot(p[:,0],p[:,1]).min(),.99999)
            self.assertTrue(np.isfinite(v).all())

    def test_manufactured_fields_divergence(self):
        for name in ('smoke-plume','wind-tunnel'):
            f=Field(name,12,42)
            p=f.initial.copy(); eps=1e-5
            div=np.zeros(len(p))
            for k in range(3):
                offset=np.zeros_like(p);offset[:,k]=eps
                div+=(f.velocity(p+offset,.8)[:,k]-f.velocity(p-offset,.8)[:,k])/(2*eps)
            np.testing.assert_allclose(div,0,atol=2e-8)

    def test_endpoint_morph_and_stable_sample_zero(self):
        f=Field('plane-to-torus',100,5)
        p0,v0=f.analytic(0);p1,v1=f.analytic(4)
        np.testing.assert_allclose(p0[:,2],0)
        np.testing.assert_allclose(v0,0);np.testing.assert_allclose(v1,0)
        np.testing.assert_allclose((np.hypot(p1[:,0],p1[:,1])-2.55)**2+p1[:,2]**2,.7**2,atol=1e-14)
        for name in NAMES:
            small=Field(name,20,4)
            a=next(small.samples(17))[0].copy()
            b=next(small.samples(49))[0].copy()
            np.testing.assert_array_equal(a,b)
            larger=Field(name,64,4)
            for (p_small,v_small),(p_large,v_large) in zip(small.samples(5),larger.samples(5)):
                np.testing.assert_array_equal(p_small,p_large[:20])
                np.testing.assert_array_equal(v_small,v_large[:20])

    def test_point_emitter_birth_and_trajectories(self):
        f=Field('smoke-plume',256,32)
        np.testing.assert_array_equal(f.initial,0)
        np.testing.assert_array_equal(f.visibility(0),0)
        count=[]
        last=None
        for j,(p,v) in enumerate(f.samples(49)):
            t=j*4/48
            unborn=t<=f.birth
            np.testing.assert_array_equal(p[unborn],0)
            np.testing.assert_array_equal(v[unborn],0)
            self.assertTrue((p[:,2]>=0).all())
            count.append(int((f.visibility(t)>.01).sum()))
            last=p
        self.assertEqual(count,sorted(count))
        self.assertGreater(count[-1],240)
        self.assertGreater(last[:,2].max(),2)
        self.assertGreater(np.ptp(last[:,0]),.2)
        # Birth is continuous rather than a position reset or velocity impulse.
        t=float(f.birth[0]);eps=1e-6
        self.assertEqual(float(f.visibility(t)[0]),0)
        self.assertLess(float(f.visibility(t+eps)[0]),1e-8)

    def test_generated_cache_with_reference_reader_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in NAMES:
                path, meta=generate(name,32,5,8,Path(tmp)/name)
                with Reader(path) as r:
                    self.assertEqual((r.header.particle_count,r.header.frame_count,r.header.sample_rate),(32,5,1))
                    for j in range(5):
                        frame=np.array(r.frame(j))
                        self.assertTrue(np.isfinite(frame).all())
                        if name=='smoke-plume':
                            self.assertTrue(((frame[:,6]>=0)&(frame[:,6]<=1)).all())
                            if j==0:np.testing.assert_array_equal(frame[:,6],0)
                        else:np.testing.assert_array_equal(frame[:,6],1)
                        np.testing.assert_array_equal(frame[:,7],0)
                self.assertEqual(json.loads(meta.read_text())['file_size_bytes'],path.stat().st_size)
                with self.assertRaises(FileExistsError):generate(name,32,5,8,Path(tmp)/name)

if __name__=='__main__':unittest.main()
