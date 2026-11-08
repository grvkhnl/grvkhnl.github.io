# Geometry diagrams

The eight canonical drawings live in `posts/*/figures/source/*.tex` and share
`diagram-style.tex`. Each produces four SVGs: desktop light, desktop dark,
stacked mobile light, and stacked mobile dark. The post's `<picture>` elements
select the mobile drawing at 600 px; CSS follows Quarto's manual theme toggle.
Alt text and numbered captions remain in the post. SVGs embed glyph outlines
and explicit backgrounds, so they also work as standalone assets. Text uses
Iowan Old Style; equations use the bundled XCharter Math font. Iowan must be
installed on the machine rebuilding the figures (it is available on this Mac).
Readers do not need either font installed because the SVGs contain outlines.

## Rebuild

From the repository root, with XeLaTeX and Poppler's `pdftocairo` installed:

```sh
python3 scripts/build-diagrams.py
# Or rebuild a single figure:
python3 scripts/build-diagrams.py --figure fim-pullback-origin
python3 scripts/export-diagram-social-previews.py
quarto render
```

PDFs and LaTeX logs are ignored under each figure's `build/` directory. The
chapter overview `.tex` files include these current PDFs instead of maintaining
separate copies of the drawings. Generated SVGs and numerical plot data are
tracked; normal site publication requires only Quarto.

## Numerical examples

`numerical-examples.json` records all parameters. To change or regenerate the
examples, run `scripts/generate-diagram-data.py` with NumPy and SciPy installed,
then rebuild the figures. The existing Manim environment can run it:

```sh
manim-scenes/.venv/bin/python scripts/generate-diagram-data.py
python3 scripts/build-diagrams.py
```

- **KL:** a symmetric mixture of two normalized Gaussians; the forward fit
  matches moments. The reverse fit is optimized from multiple initial means
  and variances using adaptive quadrature. The left and right optima are
  equivalent by symmetry. The generator checks unit integrals.
- **Displacement:** a Gaussian translated by two units. Both the snapshots and
  characteristics use the same map, with squared Wasserstein distance four.
- **Bridge:** Brownian reference and the Gaussian Schrödinger bridge have the
  same diffusivity. The bridge endpoint covariance solves
  `C² + epsilon C = s0² s1²`; conditional paths are Brownian bridges. The seed
  and endpoint laws are fixed. Nine paths illustrate each law; their empirical
  histograms are not claimed to equal the exact marginal density curves.
- **Sinkhorn:** row and column scaling of a positive, normalized 2×2 matrix.
  The figure plots the first row and column residuals. With total mass one,
  each residual vanishes exactly when the respective marginal is correct.
  The generator checks the corresponding zero residual after each update.

The two social-preview PNGs are rendered from the desktop light SVGs, fitted
inside a 1200×630 canvas with the light diagram background (`#fff1dc`).
