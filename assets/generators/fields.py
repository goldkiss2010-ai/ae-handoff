"""New procedural fields for FLD1. Coordinates are right-handed XYZ, Z-up.

Internal phase t is a dimensionless design parameter. FLD1 derivatives are
converted to stored-sample-index units by the exporter.
"""
import numpy as np

NAMES = ('vortex-ring', 'smoke-plume', 'ripple-sheet', 'wind-tunnel', 'plane-to-torus')
DESCRIPTIONS = {
 'vortex-ring': 'Analytic toroidal circulation with coherent waves and tube swirl; not a fluid solver.',
 'smoke-plume': 'Continuous emission from one fixed point into a manufactured rising flow with procedural particle dispersion; no fluid solve.',
 'ripple-sheet': 'Analytic travelling waves on a fixed material-point sheet; not a cloth solver.',
 'wind-tunnel': 'Cylinder potential-flow tracers plus a manufactured unsteady streamfunction wake; not CFD.',
 'plane-to-torus': 'Smooth point correspondence from an XY plane to a torus; not a mesh or physical simulation.',
}
ROTATIONS = {'vortex-ring': (0, 0, 0), 'smoke-plume': (-75, 0, 0),
             'ripple-sheet': (15, 0, 0), 'wind-tunnel': (0, 0, 0),
             'plane-to-torus': (0, 0, 0)}

class Field:
    def __init__(self, name, count, seed):
        if name not in NAMES or count < 1:
            raise ValueError('Unknown field or invalid particle count')
        self.name, self.count, self.seed = name, count, seed
        streams = np.random.SeedSequence(seed).spawn(5)
        self.u, self.v, self.w = (np.random.default_rng(s).random(count) for s in streams[:3])
        if name == 'smoke-plume':
            self.initial = np.zeros((count,3),dtype=np.float64)
            self.birth = .08+3.90*self.u
        elif name == 'wind-tunnel':
            # Fixed slots: a finite packet crossing the visible region, never recycled.
            # Flow ribbons make advection visible without exporting per-point color.
            def coords(u, v):
                x = -9.0+13.0*u
                y = -3.0+6.0*v
                ribbons = self.w < .72
                y[ribbons] = -2.7+5.4*np.floor(19*v[ribbons])/18+.025*np.sin(17*u[ribbons])
                return x, y
            x, y = coords(self.u,self.v)
            rx, ry = (np.random.default_rng(s) for s in streams[3:])
            inner = np.hypot(x,y) < 1.08
            while np.any(inner):
                nx, ny = coords(rx.random(count),ry.random(count))
                x[inner], y[inner] = nx[inner], ny[inner]
                inner = np.hypot(x,y) < 1.08

            self.initial = np.column_stack((x, y, (self.w-.5)*.28))

    @property
    def integrated(self):
        return self.name in ('smoke-plume', 'wind-tunnel')

    def analytic(self, t):
        if self.name == 'vortex-ring':
            u = 2*np.pi*self.u + .20*t
            v = 2*np.pi*self.v + 1.35*t
            rho = np.sqrt(self.w)
            a = 3*u-.45*t
            b = 2*u+.32*t
            c = 4*u-.28*t
            ra = 2.75+.28*np.sin(a)+.10*np.sin(c)
            dra = .28*np.cos(a)*.15+.10*np.cos(c)*.52
            rr = .68*rho*(1+.18*np.sin(b))
            drr = .68*rho*.18*np.cos(b)*.72
            z0 = .25*np.sin(2*u-.38*t)
            dz0 = .25*np.cos(2*u-.38*t)*.02
            rv = ra+rr*np.cos(v)
            drv = dra+drr*np.cos(v)-1.35*rr*np.sin(v)
            p = np.column_stack((rv*np.cos(u),rv*np.sin(u),z0+rr*np.sin(v)))
            d = np.column_stack((drv*np.cos(u)-.20*rv*np.sin(u),
                                 drv*np.sin(u)+.20*rv*np.cos(u),
                                 dz0+drr*np.sin(v)+1.35*rr*np.cos(v)))
        elif self.name == 'ripple-sheet':
            x, y = 8*(self.u-.5), 5.6*(self.v-.5)
            a, b, c = 1.5*x-.9*t, .8*x+1.7*y-1.4*t, 2.4*y+.6*t
            edge = .35+.65*(x+4)/8
            z = edge*(.55*np.sin(a)+.22*np.sin(b))+.1*np.sin(c)
            dz = edge*(-.495*np.cos(a)-.308*np.cos(b))+.06*np.cos(c)
            p = np.column_stack((x,y,z))
            d = np.column_stack((np.zeros_like(x),np.zeros_like(y),dz))
        elif self.name == 'plane-to-torus':
            s = np.clip(t/4,0,1)
            f = s*s*s*(10-15*s+6*s*s)
            df = 30*s*s*(1-s)*(1-s)/4
            u, v = 2*np.pi*self.u, 2*np.pi*self.v
            start = np.column_stack((7.2*(self.u-.5),4.8*(self.v-.5),np.zeros(self.count)))
            target = np.column_stack(((2.55+.7*np.cos(v))*np.cos(u),
                                      (2.55+.7*np.cos(v))*np.sin(u),.7*np.sin(v)))
            p = start+f*(target-start)
            d = df*(target-start)
        else:
            raise ValueError('This field requires integration')
        return p, d

    def velocity(self, p, t):
        x, y, z = p.T
        if self.name == 'smoke-plume':
            # Fixed point emitter. Per-slot dispersion widens the rising plume.
            base = np.column_stack((.30*np.sin(1.2*z+.65*t)+.14*np.sin(2*y-1.1*t)
                                    +.23*np.cos(2*np.pi*self.v+1.8*t)+.35*(self.u-.5),
                                    .26*np.cos(z-.5*t)+.12*np.sin(1.6*x+.9*t)
                                    +.23*np.sin(2*np.pi*self.u+1.55*t)+.35*(self.v-.5),
                                    .65+.20*np.sin(x+.8*t)*np.sin(y-.5*t)+.18*(self.w-.5)))
            return base*self.visibility(t)[:,None]
        if self.name != 'wind-tunnel':
            raise ValueError('This field has no Eulerian velocity')
        a2 = 1.0
        r2 = np.maximum(x*x+y*y,1e-12)
        inv, inv2 = 1/r2, 1/(r2*r2)
        uniform = 1.05*(1+.06*np.cos(3*z))
        u = uniform*(1-a2*inv+2*a2*y*y*inv2)
        v = -2*uniform*a2*x*y*inv2
        # psi_w = A B H G sin(kx-wt); u=+dpsi/dy, v=-dpsi/dx.
        # B and its gradient vanish on the cylinder boundary.
        e = 1-a2*inv
        b, bx, by = e*e, 4*a2*x*e*inv2, 4*a2*y*e*inv2
        h = 1/(1+np.exp(np.clip(-3*(x-1.35),-700,700)))
        hx = 3*h*(1-h)
        g = np.exp(-((x-3)/3.0)**2-(y/.9)**2)
        gx, gy = -2*(x-3)/9*g, -2*y/.81*g
        ph = 2.6*x-1.8*t
        sn, cs = np.sin(ph), np.cos(ph)
        amp = .16
        u += amp*h*(by*g+b*gy)*sn
        v -= amp*((bx*h*g+b*hx*g+b*h*gx)*sn+b*h*g*2.6*cs)
        return np.column_stack((u,v,np.zeros_like(x)))

    def visibility(self, t):
        if self.name != 'smoke-plume':
            return np.ones(self.count)
        age = np.clip((t-self.birth)/.15,0,1)
        # Smooth activation keeps position and its derivative continuous at birth.
        return age*age*(3-2*age)

    def advance(self, p, t0, t1, max_step=.04):
        steps = max(1,int(np.ceil((t1-t0)/max_step)))
        dt = (t1-t0)/steps
        for k in range(steps):
            t = t0+k*dt
            a = self.velocity(p,t)
            b = self.velocity(p+.5*dt*a,t+.5*dt)
            c = self.velocity(p+.5*dt*b,t+.5*dt)
            d = self.velocity(p+dt*c,t+dt)
            p = p+dt/6*(a+2*b+2*c+d)
        return p

    def samples(self, samples):
        if samples < 2:
            raise ValueError('Need at least two samples')
        step = 4.0/(samples-1)
        p = self.initial.copy() if self.integrated else None
        for j in range(samples):
            t = j*step
            if self.integrated:
                if j:
                    p = self.advance(p,(j-1)*step,t)
                derivative = self.velocity(p,t)
            else:
                p, derivative = self.analytic(t)
            # Sample-index derivative, not a velocity in seconds.
            yield p, derivative*step
