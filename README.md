# OpenCV Document Scanner

![Tests](https://github.com/SiddarthaGodena-AI/opencv-document-scanner/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Turn a photograph of a rectangular page into a perspective-corrected, high-contrast scan without a cloud API.

## Pipeline

Grayscale -> Gaussian blur -> Canny edges -> contour detection -> convex quadrilateral -> perspective transform -> adaptive threshold.

## Run

Requires Python 3.12. Create and activate a virtual environment, then:

```bash
pip install -r requirements-dev.txt
python scanner.py photo.jpg --output scan.png
python -m pytest -q
python demo.py
```

The CLI reports a useful error when no large page boundary is found. No private documents or photos are bundled.

`python demo.py` creates a synthetic tilted page, corrected color output, and binary scan in `outputs/`. The generated page can be recreated on any machine without downloading an image.

## Tests

Synthetic tests check a skewed white page, blank-image rejection, and corner ordering. CI runs these offline. This tests behavior, not OCR accuracy.

## Limitations

Works best with one convex rectangular document contrasting with its background. Shadows, curved pages, clutter, and extreme perspective can defeat contour detection. Does not perform OCR. A future extension could add manual corner selection and OCR as optional modules.

## Resume-ready description

“Built a local OpenCV scanner using contour detection, perspective correction, adaptive thresholding, and deterministic synthetic tests.”

MIT licensed. Main implementation: `scanner.py`; regression tests: `tests/`.
