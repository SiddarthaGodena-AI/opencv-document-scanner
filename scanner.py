"""Detect a document quadrilateral and produce a perspective-corrected scan."""
import argparse
import cv2
import numpy as np

def order_corners(points):
    points = np.asarray(points, dtype=np.float32).reshape(4, 2)
    center = points.mean(axis=0)
    angles = np.arctan2(points[:, 1]-center[1], points[:, 0]-center[0])
    ordered = points[np.argsort(angles)]
    ordered = np.roll(ordered, -int(np.argmin(ordered.sum(axis=1))), axis=0)
    return ordered

def scan(image):
    if image is None or image.size == 0:
        raise ValueError("Image is empty")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (5,5), 0), 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    quad = None
    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(contour) < image.shape[0]*image.shape[1]*0.1:
            continue
        candidate = cv2.approxPolyDP(contour, .02*cv2.arcLength(contour, True), True)
        if len(candidate) == 4 and cv2.isContourConvex(candidate):
            quad = candidate
            break
    if quad is None:
        raise ValueError("No sufficiently large document quadrilateral found")
    tl, tr, br, bl = order_corners(quad)
    width = int(max(np.linalg.norm(tr-tl), np.linalg.norm(br-bl)))
    height = int(max(np.linalg.norm(bl-tl), np.linalg.norm(br-tr)))
    if min(width, height) < 2:
        raise ValueError("Degenerate document")
    target = np.float32([[0,0],[width-1,0],[width-1,height-1],[0,height-1]])
    transform = cv2.getPerspectiveTransform(np.float32([tl,tr,br,bl]), target)
    warped = cv2.warpPerspective(image, transform, (width,height))
    bw = cv2.adaptiveThreshold(cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY),255,
                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,10)
    return warped, bw

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--output", default="scan.png")
    args = parser.parse_args()
    try:
        _, bw = scan(cv2.imread(args.input))
    except ValueError as error:
        parser.error(str(error))
    if not cv2.imwrite(args.output, bw):
        parser.error("Could not write output")
    print(args.output)

if __name__ == "__main__":
    main()

