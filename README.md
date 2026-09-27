# OpenCV Document Scanner

![Tests](https://github.com/SiddarthaGodena-AI/opencv-document-scanner/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A small command-line scanner for photos of rectangular pages. It finds the page boundary, straightens the image, and saves a high-contrast black-and-white scan. Everything runs locally; there is no upload service or OCR step.

## How the scan is made

The image is converted to grayscale and blurred before Canny edge detection. The scanner looks for a large convex quadrilateral among the contours, orders its corners, and applies a perspective transform. Adaptive thresholding turns the corrected page into the final scan.

## Run

Use Python 3.12. From the repository folder, create an environment with `python -m venv .venv`. Activate it with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on Linux/macOS, then:

```bash
pip install -r requirements-dev.txt
python scanner.py photo.jpg --output scan.png
python -m pytest -q
python demo.py
```

Try a photo with the whole page visible against a contrasting background. The command reports an error if it cannot find a sufficiently large, four-sided page boundary instead of quietly saving a bad crop.

If you don't have a photo handy, start with `python demo.py`. It creates a tilted page and writes three images into `outputs/`:

- `input.png`: the synthetic photo
- `corrected.png`: the page after perspective correction, still in color
- `scan.png`: the black-and-white result

Comparing those images is a quick way to see what each stage does. No personal documents are included, and generated files are excluded from Git.

You can also call the scanner from Python:

```python
import cv2
from scanner import scan

color_page, binary_page = scan(cv2.imread("photo.jpg"))
cv2.imwrite("corrected.png", color_page)
cv2.imwrite("scan.png", binary_page)
```

## Tests

Three synthetic tests check a skewed page, blank-image rejection, and corner ordering. CI runs them offline. They check the pipeline's behavior, not how well it handles every phone photo. Recorded checks are in [VALIDATION.md](VALIDATION.md).

## Limitations

The scanner depends on a clear page outline. Shadows, a busy background, curved pages, and extreme angles can cause boundary detection to fail. It does not recognize text.

Manual corner selection would be a useful next addition when automatic detection misses the page. OCR could come later as a separate, optional step.

MIT licensed. Main implementation: `scanner.py`; regression tests: `tests/`.
