# Validation record

On 27 September 2026, all three tests passed locally and on GitHub Actions.

The synthetic demo generated a tilted page, applied perspective correction, and produced a binary scan. Input and output were visually inspected: text and horizontal rules remained legible and the page was straightened.

Run `python demo.py` to reproduce the input and outputs. This validates a controlled example; real photos with shadows, curled pages, and clutter need a separate benchmark. No OCR or real-world accuracy claim is made.
