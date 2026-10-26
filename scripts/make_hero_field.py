"""Generate the data for the animated hero banner on the homepage.

Computes the total field u = u_inc + u_sc of a plane wave e^{ikx} scattered
by a sound-soft disk of radius a (exact series solution) and stores Re(u) and
Im(u) in the R and G channels of a PNG. The browser then animates
Re(u e^{-i omega t}) = Re(u) cos(omega t) + Im(u) sin(omega t) on a <canvas>
(see assets/js/hero-waves.js).

Also writes a static poster frame (t = 0) used before the script runs, or when
the visitor prefers reduced motion.

Usage:  python3 scripts/make_hero_field.py
"""

from pathlib import Path

import numpy as np
from matplotlib import colormaps
from PIL import Image
from scipy.special import hankel1, jv

# --- parameters ---------------------------------------------------------------
K = 5.0                      # wavenumber
A = 1.0                      # disk radius
X_RANGE = (-7.5, 4.5)        # domain (disk centred at the origin)
Y_RANGE = (-2.0, 2.0)
WIDTH, HEIGHT = 960, 320     # pixels (same 3:1 aspect ratio as the domain)
N_TERMS = int(K * A) + 25    # series truncation
OBSTACLE_RGB = (24, 26, 33)  # keep in sync with assets/js/hero-waves.js

OUT_DIR = Path(__file__).resolve().parent.parent / "images" / "hero"


def total_field(x, y):
    r = np.hypot(x, y)
    theta = np.arctan2(y, x)
    u_sc = np.zeros_like(r, dtype=complex)
    for n in range(N_TERMS + 1):
        coeff = -(1j ** n) * jv(n, K * A) / hankel1(n, K * A)
        weight = 1.0 if n == 0 else 2.0
        u_sc += weight * coeff * hankel1(n, K * np.maximum(r, A)) * np.cos(n * theta)
    u = np.exp(1j * K * x) + u_sc
    u[r < A] = 0.0
    return u


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # pixel centres, y pointing up
    xs = np.linspace(*X_RANGE, WIDTH, endpoint=False) + (X_RANGE[1] - X_RANGE[0]) / (2 * WIDTH)
    ys = np.linspace(*Y_RANGE[::-1], HEIGHT, endpoint=False) - (Y_RANGE[1] - Y_RANGE[0]) / (2 * HEIGHT)
    X, Y = np.meshgrid(xs, ys)
    u = total_field(X, Y)

    # sanity check: Dirichlet condition on the boundary
    t = np.linspace(0, 2 * np.pi, 200)
    bnd = total_field(A * np.cos(t) * (1 + 1e-12), A * np.sin(t) * (1 + 1e-12))
    print(f"max |u| on boundary: {np.abs(bnd).max():.2e}")

    scale = np.abs(u).max()
    to_byte = lambda v: np.clip(np.round((v / scale + 1) * 127.5), 0, 255).astype(np.uint8)
    rgb = np.dstack([to_byte(u.real), to_byte(u.imag), np.full(u.shape, 255, np.uint8)])
    Image.fromarray(rgb, "RGB").save(OUT_DIR / "field.png", optimize=True)

    # static poster frame (t = 0), same colour mapping as the JS
    frame = colormaps["viridis"]((u.real / scale + 1) / 2)[..., :3]
    # obstacle: dark fill with a light outline, anti-aliased
    px = (X_RANGE[1] - X_RANGE[0]) / WIDTH
    d = (np.hypot(X, Y) - A) / px                       # signed distance in pixels
    outline = np.clip(1.5 - np.abs(d + 0.75), 0, 1)[..., None]
    inside = np.clip(0.5 - d, 0, 1)[..., None]
    frame = frame * (1 - inside) + np.array(OBSTACLE_RGB) / 255 * inside
    frame = frame * (1 - outline) + outline
    Image.fromarray((frame * 255).astype(np.uint8), "RGB").save(
        OUT_DIR / "poster.webp", quality=85, method=6
    )

    cx = (0 - X_RANGE[0]) / (X_RANGE[1] - X_RANGE[0])
    cy = (Y_RANGE[1] - 0) / (Y_RANGE[1] - Y_RANGE[0])
    r = A / (X_RANGE[1] - X_RANGE[0])
    print(f"field scale {scale:.3f}; disk at ({cx:.4f}, {cy:.4f}) radius {r:.4f} (fractions of width/height/width)")


if __name__ == "__main__":
    main()
