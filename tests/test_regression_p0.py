"""Regression tests for 10x code-review P0/P1 fixes."""
import json
import os
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from BladeCalc import (
    CalcStageBladeAngles,
    LinearStageProp,
    NACA4Blade,
    StageCalc,
    camber_from_turning,
)
from StlUtils import _unique_faces, drawCylinder, drawDuct, rotationMatrix
from FileOps import StageSave, StageOpen
from DefaultParameters import get_default_parameters
from Presets import get_preset, get_preset_names


class TestStagePropsIsolation(unittest.TestCase):
    def test_instances_do_not_share_props(self):
        a = LinearStageProp()
        b = LinearStageProp()
        a.rootProps.beta1 = 123.0
        self.assertNotEqual(b.rootProps.beta1, 123.0)
        a.meanProps.cx = 999.0
        self.assertNotEqual(b.meanProps.cx, 999.0)


class TestStageCalc(unittest.TestCase):
    def test_mean_phi_preserved(self):
        sp = StageCalc(r=0.4, phi=0.691, psi=0.482, rpm=30000,
                       rootRadius=15.0, tipRadius=30.0)
        self.assertAlmostEqual(sp.meanProps.phi, 0.691, places=9)
        self.assertAlmostEqual(sp.meanProps.r, 0.4)
        # free-vortex: root/tip cx must match mean cx
        self.assertAlmostEqual(sp.rootProps.cx, sp.meanProps.cx, places=2)
        self.assertAlmostEqual(sp.tipProps.cx, sp.meanProps.cx, places=2)

    def test_invalid_radii_raise(self):
        with self.assertRaises(ValueError):
            StageCalc(r=0.5, phi=0.6, psi=0.5, rpm=10000,
                      rootRadius=30.0, tipRadius=30.0)
        with self.assertRaises(ValueError):
            StageCalc(r=0.5, phi=0.6, psi=0.5, rpm=10000,
                      rootRadius=-1.0, tipRadius=30.0)

    def test_zero_phi_raises_not_hangs(self):
        with self.assertRaises(ValueError):
            CalcStageBladeAngles(r=0.5, phi=0.0, psi=0.5,
                                 rpm=10000, radius=25.0)


class TestCamber(unittest.TestCase):
    def test_zero_turning_returns_zero(self):
        self.assertEqual(camber_from_turning(20.0, 0.0), 0.0)

    def test_known_value_sign(self):
        c = camber_from_turning(20.0, 0.3)
        self.assertTrue(np.isfinite(c))
        self.assertLess(c, 0)  # convention: negative camber value

    def test_bad_chord_raises(self):
        with self.assertRaises(ValueError):
            camber_from_turning(0.0, 0.3)


class TestNACA4Blade(unittest.TestCase):
    def test_includes_trailing_edge(self):
        faces, verts = NACA4Blade(0.04, 0.02, 0.35, 0.12, 15.0, 10.0,
                                  20.0, 10.0, [50.0, 0.0])
        # npts=25 per surface incl TE, 2 surfaces, 2 span stations
        self.assertEqual(len(verts), 2 * 25 * 2)
        for f in faces:
            self.assertEqual(len(f), 3)
            for idx in f:
                self.assertLess(idx, len(verts))

    def test_bad_inputs_raise(self):
        with self.assertRaises(ValueError):
            NACA4Blade(0.04, 0.02, 0.35, 0.12, 0.0, 10.0, 20.0, 10.0,
                       [50.0, 0.0])
        with self.assertRaises(ValueError):
            NACA4Blade(0.04, 0.02, 1.5, 0.12, 15.0, 10.0, 20.0, 10.0,
                       [50.0, 0.0])


class TestStlUtilsFixes(unittest.TestCase):
    def test_unique_faces_deterministic(self):
        faces = [[0, 1, 2], [2, 1, 0], [0, 1, 2], [3, 4, 5]]
        once = _unique_faces(faces).tolist()
        twice = _unique_faces(faces).tolist()
        self.assertEqual(once, twice)
        self.assertEqual(once, [[0, 1, 2], [2, 1, 0], [3, 4, 5]])

    def test_cylinder_validation(self):
        with self.assertRaises(ValueError):
            drawCylinder(0, 10)
        with self.assertRaises(ValueError):
            drawDuct(10, 0, 10)

    def test_cylinder_deterministic_order(self):
        a = drawCylinder(10.0, 20.0).vectors.copy()
        b = drawCylinder(10.0, 20.0).vectors.copy()
        self.assertTrue(np.allclose(a, b))


class TestFileOpsValidation(unittest.TestCase):
    def test_mismatched_lengths_raise(self):
        with self.assertRaises(ValueError):
            StageSave('/tmp/x.json', [{'a': 1}], [], [])

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            StageSave('/tmp/x.json', [], [], [])

    def test_corrupt_json_raises_valueerror(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json',
                                         delete=False) as f:
            f.write('{not json')
            name = f.name
        try:
            with self.assertRaises(ValueError):
                list(StageOpen(name))
        finally:
            os.unlink(name)

    def test_missing_keys_raise(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json',
                                         delete=False) as f:
            json.dump({"Stage 1": {"Stage": {}, "Rotor": {}}}, f)
            name = f.name
        try:
            with self.assertRaises(ValueError):
                list(StageOpen(name))
        finally:
            os.unlink(name)


class TestDeepcopyContracts(unittest.TestCase):
    def test_defaults_isolated(self):
        a = get_default_parameters()
        a['Rotor']['Rotor Diameter'] = 'MUTATED'
        b = get_default_parameters()
        self.assertNotEqual(b['Rotor']['Rotor Diameter'], 'MUTATED')

    def test_presets_isolated(self):
        names = get_preset_names()
        self.assertTrue(names)
        a = get_preset(names[0])
        a['Rotor']['Rotor Diameter'] = 'MUTATED'
        b = get_preset(names[0])
        self.assertNotEqual(b['Rotor']['Rotor Diameter'], 'MUTATED')


if __name__ == '__main__':
    unittest.main()
