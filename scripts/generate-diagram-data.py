#!/usr/bin/env python3
"""Reproduce the numerical examples used by the geometry diagrams.

Run with a Python environment containing NumPy and SciPy. Generated plot data
are committed, so publishing the Quarto site does not require Python or TeX.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
KL = ROOT / 'posts/the-asymmetry-of-information/figures/source/data'
OT = ROOT / 'posts/the-second-ruler-of-displacement/figures/source/data'
SB = ROOT / 'posts/the-bridge/figures/source/data'
for folder in [KL, OT, SB]:
    folder.mkdir(exist_ok=True)

def normal(x, mean, std):
    return np.exp(-0.5*((x-mean)/std)**2)/(std*np.sqrt(2*np.pi))

def save(path, x, y):
    np.savetxt(path, np.column_stack([x, y]), fmt='%.8f')

# A normalized, symmetric, separated Gaussian mixture and Gaussian fits.
a, s = 2.0, 0.55
forward_mean, forward_std = 0.0, np.sqrt(a*a+s*s)
def logp(x):
    return logsumexp(np.stack([-0.5*((x+a)/s)**2,
                               -0.5*((x-a)/s)**2]), axis=0) - np.log(2*s*np.sqrt(2*np.pi))
def reverse_kl(params):
    mean, std = params[0], np.exp(params[1])
    return quad(lambda z: float(normal(z, 0, 1) *
        (-0.5*z*z - np.log(std*np.sqrt(2*np.pi)) - logp(mean+std*z))),
        -10, 10, epsabs=1e-10)[0]
solutions = [minimize(reverse_kl, [m, np.log(sd)], method='Nelder-Mead',
                      options={'xatol': 1e-10, 'fatol': 1e-11, 'maxiter': 2000})
             for m in [-a, 0, a] for sd in [s, 1.0, forward_std]]
assert all(sol.success for sol in solutions)
best = min(solutions, key=lambda sol: sol.fun)
# Symmetry gives two equally good mode-centered solutions; draw the left one.
reverse_mean, reverse_std = -abs(float(best.x[0])), float(np.exp(best.x[1]))
x = np.linspace(-7, 7, 561)
save(KL/'target.dat', x, np.exp(logp(x)))
save(KL/'forward.dat', x, normal(x, forward_mean, forward_std))
save(KL/'reverse.dat', x, normal(x, reverse_mean, reverse_std))
for f in [lambda x: np.exp(logp(x)),
          lambda x: normal(x, forward_mean, forward_std),
          lambda x: normal(x, reverse_mean, reverse_std)]:
    assert abs(quad(f, -30, 30)[0]-1) < 1e-8
(KL/'fit-parameters.tex').write_text(
    f'\\def\\forwardstd{{{forward_std:.3f}}}\n'
    f'\\def\\reversemean{{{reverse_mean:.3f}}}\n'
    f'\\def\\reversestd{{{reverse_std:.3f}}}\n')

# One common displacement example: rho_t = N(-1+2t, 0.6^2).
x = np.linspace(-3.3, 3.3, 265)
for t, filename in [(0, 'start'), (0.5, 'middle'), (1, 'end')]:
    save(OT/(filename+'.dat'), x, normal(x, -1+2*t, 0.6))
starts = np.array([-1.9, -1.45, -1, -0.55, -0.1])
for i, start in enumerate(starts):
    save(OT/f'characteristic-{i}.dat', [start, start+2], [0, 1])
assert np.allclose((starts+2)-starts, 2)

# Gaussian Schrodinger bridge for Brownian diffusivity epsilon.
# Endpoint covariance solves C^2 + epsilon*C = s0^2*s1^2.
# Conditional on endpoints, its paths are Brownian bridges.
rng = np.random.default_rng(20261108)
epsilon, s0, s1, m0, m1 = 0.35, 0.45, 0.45, 0.0, 2.5
cov = (np.sqrt(epsilon**2+4*s0*s0*s1*s1)-epsilon)/2
assert abs(cov*cov+epsilon*cov-s0*s0*s1*s1) < 1e-12
t = np.linspace(0, 1, 101)
for i in range(9):
    x0 = rng.normal(m0, s0)
    x1 = m1 + cov/(s0*s0)*(x0-m0) + np.sqrt(s1*s1-cov*cov/(s0*s0))*rng.normal()
    bm = np.r_[0, np.cumsum(rng.normal(0, np.sqrt(t[1]), len(t)-1))]
    reference = x0 + np.sqrt(epsilon)*bm
    bridge = (1-t)*x0 + t*x1 + np.sqrt(epsilon)*(bm-t*bm[-1])
    save(SB/f'reference-{i}.dat', reference, t)
    save(SB/f'bridge-{i}.dat', bridge, t)
    assert abs(bridge[0]-x0) < 1e-12 and abs(bridge[-1]-x1) < 1e-12
x = np.linspace(-2.0, 4.0, 361)
for filename, mean, std in [('initial', m0, s0), ('target', m1, s1),
                            ('reference-terminal', m0, np.sqrt(s0*s0+epsilon))]:
    save(SB/(filename+'.dat'), x, normal(x, mean, std))
summary = {'kl': {'target': '0.5 N(-2, 0.55^2) + 0.5 N(2, 0.55^2)',
                   'forward': {'mean': forward_mean, 'std': float(forward_std)},
                   'reverse': {'mean': reverse_mean, 'std': reverse_std, 'kl': float(best.fun)},
                   'method': 'moment-matched forward fit; multistart reverse-KL minimization with adaptive quadrature'},
           'displacement': {'mean': '-1 + 2t', 'std': 0.6, 'squared_wasserstein': 4.0},
           'bridge': {'seed': 20261108, 'epsilon': epsilon,
                      'initial_mean': m0, 'terminal_mean': m1,
                      'initial_std': s0, 'terminal_std': s1,
                      'endpoint_covariance': float(cov)}}
(ROOT/'assets/diagrams/numerical-examples.json').write_text(json.dumps(summary, indent=2)+'\n')

# A total-mass-one 2x2 example: one residual characterizes each marginal.
mu, nu = np.array([0.55, 0.45]), np.array([0.35, 0.65])
coupling = np.array([[0.32, 0.08], [0.12, 0.48]])
residuals = []
for k in range(13):
    r = coupling.sum(axis=1)[0]-mu[0]
    c = coupling.sum(axis=0)[0]-nu[0]
    residuals.append([float(r), float(c)])
    assert abs(coupling.sum()-1) < 1e-12
    if k:
        assert abs(r if k % 2 else c) < 1e-12
    if k % 2 == 0:
        coupling *= (mu/coupling.sum(axis=1))[:, None]
    else:
        coupling *= (nu/coupling.sum(axis=0))[None, :]
assert np.linalg.norm(residuals[-1]) < 0.001
(SB/'sinkhorn-coordinates.tex').write_text(''.join(
    f'\\coordinate (g{k}) at ({r:.8f},{c:.8f});\n'
    for k, (r,c) in enumerate(residuals)))
summary['sinkhorn'] = {'initial': [[0.32,0.08],[0.12,0.48]],
                        'source_marginal': mu.tolist(), 'target_marginal': nu.tolist(),
                        'residuals': residuals}
(ROOT/'assets/diagrams/numerical-examples.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
