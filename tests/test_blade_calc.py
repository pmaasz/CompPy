import unittest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from BladeCalc import StageCalc, CalcStageBladeAngles, NACA4Blade, FindBounds
from stl import mesh


class TestBladeCalc(unittest.TestCase):
    """Test blade calculation functions"""
    
    def test_calc_stage_blade_angles(self):
        """Test stage blade angle calculations"""
        stageProps = CalcStageBladeAngles(
            r=0.4,
            phi=0.691,
            psi=0.482,
            rpm=30000,
            radius=25.0
        )
        
        self.assertIsNotNone(stageProps.beta1)
        self.assertIsNotNone(stageProps.beta2)
        self.assertIsNotNone(stageProps.alpha1)
        self.assertIsNotNone(stageProps.alpha2)
        self.assertIsNotNone(stageProps.cx)
        self.assertEqual(stageProps.rpm, 30000)
        self.assertEqual(stageProps.radius, 25.0)
    
    def test_stage_calc(self):
        """Test full stage calculation"""
        stageProps = StageCalc(
            r=0.4,
            phi=0.691,
            psi=0.482,
            rpm=30000,
            rootRadius=15.0,
            tipRadius=30.0
        )
        
        self.assertEqual(stageProps.rootRadius, 15.0)
        self.assertEqual(stageProps.tipRadius, 30.0)
        self.assertIsNotNone(stageProps.rootProps)
        self.assertIsNotNone(stageProps.meanProps)
        self.assertIsNotNone(stageProps.tipProps)
        
        # Check that axial velocity is consistent
        self.assertAlmostEqual(
            stageProps.rootProps.cx,
            stageProps.meanProps.cx,
            places=2
        )
        self.assertAlmostEqual(
            stageProps.tipProps.cx,
            stageProps.meanProps.cx,
            places=2
        )
    
    def test_naca4_blade(self):
        """Test NACA4 blade generation"""
        faces, verts = NACA4Blade(
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
        
        self.assertIsInstance(faces, list)
        self.assertIsInstance(verts, list)
        self.assertGreater(len(faces), 0)
        self.assertGreater(len(verts), 0)
        
        # Check that all faces reference valid vertices
        for face in faces:
            self.assertEqual(len(face), 3)
            for idx in face:
                self.assertLess(idx, len(verts))
    
    def test_find_bounds(self):
        """Test bounding box calculation with a real cylinder"""
        from StlUtils import drawCylinder
        
        # Create a cylinder with known dimensions
        cylinder = drawCylinder(dia=10.0, height=20.0, res=25)
        
        minx, maxx, miny, maxy, minz, maxz = FindBounds(cylinder)
        
        # Check that bounds are reasonable for a 10mm diameter, 20mm tall cylinder
        # Diameter ~10, so radius ~5
        self.assertAlmostEqual(float(maxx - minx), 10.0, places=0)
        self.assertAlmostEqual(float(maxy - miny), 10.0, places=0)
        self.assertAlmostEqual(float(maxz - minz), 20.0, places=1)


if __name__ == '__main__':
    unittest.main()
