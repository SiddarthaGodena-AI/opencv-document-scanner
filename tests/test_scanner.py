import cv2
import numpy as np
import pytest
from scanner import scan, order_corners

def test_synthetic_document():
    image = np.zeros((500,600,3),np.uint8)
    cv2.fillConvexPoly(image,np.int32([[90,70],[510,110],[490,440],[70,410]]),(255,255,255))
    color, bw = scan(image)
    assert color.shape[0] > 250 and color.shape[1] > 350
    assert set(np.unique(bw)).issubset({0,255})

def test_no_document():
    with pytest.raises(ValueError,match="quadrilateral"):
        scan(np.zeros((100,100,3),np.uint8))

def test_corner_order():
    np.testing.assert_array_equal(order_corners([[10,10],[0,10],[10,0],[0,0]]),
                                  [[0,0],[10,0],[10,10],[0,10]])

