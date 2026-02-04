import unittest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from StlUtils import drawCylinder, drawDuct, drawBlade, rotationMatrix
from BladeCalc import FindBounds


class TestStlUtils(unittest.TestCase):
    """Test STL utility functions"""
    
    def test_draw_cylinder(self):
        """Test cylinder generation"""
        cylinder = drawCylinder(dia=10.0, height=20.0, res=25)
        
        self.assertIsNotNone(cylinder)
        self.assertGreater(len(cylinder.vectors), 0)
        
        # Check bounds
        minx, maxx, miny, maxy, minz, maxz = FindBounds(cylinder)
        
        # Diameter should be approximately 10
        self.assertAlmostEqual(maxx - minx, 10.0, places=0)
        self.assertAlmostEqual(maxy - miny, 10.0, places=0)
        # Height should be 20
        self.assertAlmostEqual(maxz - minz, 20.0, places=1)
    
    def test_draw_duct(self):
        """Test duct (hollow cylinder) generation"""
        duct = drawDuct(innerDia=10.0, thickness=2.0, height=20.0, res=25)
        
        self.assertIsNotNone(duct)
        self.assertGreater(len(duct.vectors), 0)
        
        # Check bounds - outer diameter should be innerDia + 2*thickness
        minx, maxx, miny, maxy, minz, maxz = FindBounds(duct)
        
        outer_dia = 10.0 + 2 * 2.0  # 14.0
        self.assertAlmostEqual(maxx - minx, outer_dia, places=0)
        self.assertAlmostEqual(maxy - miny, outer_dia, places=0)
        self.assertAlmostEqual(maxz - minz, 20.0, places=1)
    
    def test_draw_blade(self):
        """Test blade generation"""
        blade = drawBlade(
            camberRoot=0.04,
            camberTip=0.02,
            camberPos=0.35,
            thickness=0.12,
            bladeHeight=15.0,
            twistAngle=10.0,
            rootChord=20.0,
            tipChord=10.0,
            cot=[50.0, 0.0]
        )
        
        self.assertIsNotNone(blade)
        self.assertGreater(len(blade.vectors), 0)
        
        # Check that blade has reasonable bounds
        minx, maxx, miny, maxy, minz, maxz = FindBounds(blade)
        
        # Height should be approximately 15
        self.assertAlmostEqual(maxz - minz, 15.0, places=0)
    
    def test_rotation_matrix(self):
        """Test rotation matrix generation"""
        # Test rotation around z-axis by 90 degrees
        R = rotationMatrix([0, 0, 1], np.pi / 2)
        
        self.assertEqual(R.shape, (3, 3))
        
        # Rotating [1, 0, 0] by 90 degrees around z should give approximately [0, 1, 0]
        vec = np.array([1, 0, 0])
        rotated = R.dot(vec)
        
        self.assertAlmostEqual(rotated[0], 0.0, places=5)
        self.assertAlmostEqual(rotated[1], 1.0, places=5)
        self.assertAlmostEqual(rotated[2], 0.0, places=5)
    
    def test_rotation_matrix_no_rotation(self):
        """Test rotation matrix with zero axis"""
        R = rotationMatrix([0, 0, 0], 0)
        
        # Should return zero matrix
        self.assertTrue(np.allclose(R, np.zeros((3, 3))))


if __name__ == '__main__':
    unittest.main()
