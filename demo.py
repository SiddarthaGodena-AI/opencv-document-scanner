"""Generate a synthetic tilted document and its corrected scan."""
from pathlib import Path
import cv2
import numpy as np
from scanner import scan

def main():
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    page = np.full((350, 450, 3), 245, np.uint8)
    cv2.putText(page, "OpenCV Document Demo", (25, 65), cv2.FONT_HERSHEY_SIMPLEX, .8, (20,20,20), 2)
    for y in range(110, 300, 30):
        cv2.line(page, (25,y), (390,y), (70,70,70), 2)
    src = np.float32([[0,0],[449,0],[449,349],[0,349]])
    dst = np.float32([[90,70],[510,110],[490,440],[70,410]])
    image = cv2.warpPerspective(page, cv2.getPerspectiveTransform(src,dst), (600,500))
    color, bw = scan(image)
    cv2.imwrite(str(out/"input.png"), image)
    cv2.imwrite(str(out/"corrected.png"), color)
    cv2.imwrite(str(out/"scan.png"), bw)
    print("Synthetic input and scans written to outputs/")

if __name__ == "__main__":
    main()
