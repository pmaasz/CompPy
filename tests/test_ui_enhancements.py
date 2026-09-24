"""
Test new UI/UX enhancement modules
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from UndoRedo import UndoRedoManager
from Tooltips import get_tooltip, PARAMETER_TOOLTIPS
from Presets import get_preset_names, get_preset, get_preset_description


class TestUndoRedo(unittest.TestCase):
    def setUp(self):
        self.manager = UndoRedoManager()
    
    def test_initial_state(self):
        """Test initial state of undo/redo manager"""
        self.assertFalse(self.manager.can_undo())
        self.assertFalse(self.manager.can_redo())
    
    def test_push_and_undo(self):
        """Test pushing state and undoing"""
        state = {'stage_idx': 0, 'field_name': 'RPM', 'old_value': '100', 'new_value': '200'}
        self.manager.push_state(state)
        
        self.assertTrue(self.manager.can_undo())
        self.assertFalse(self.manager.can_redo())
        
        undone_state = self.manager.undo()
        self.assertEqual(undone_state, state)
        self.assertFalse(self.manager.can_undo())
        self.assertTrue(self.manager.can_redo())
    
    def test_redo(self):
        """Test redo functionality"""
        state = {'stage_idx': 0, 'field_name': 'RPM', 'old_value': '100', 'new_value': '200'}
        self.manager.push_state(state)
        self.manager.undo()
        
        redone_state = self.manager.redo()
        self.assertEqual(redone_state, state)
        self.assertTrue(self.manager.can_undo())
        self.assertFalse(self.manager.can_redo())
    
    def test_clear(self):
        """Test clearing undo/redo stacks"""
        state = {'stage_idx': 0, 'field_name': 'RPM', 'old_value': '100', 'new_value': '200'}
        self.manager.push_state(state)
        self.manager.clear()
        
        self.assertFalse(self.manager.can_undo())
        self.assertFalse(self.manager.can_redo())
    
    def test_max_stack_size(self):
        """Test that stack size is limited"""
        for i in range(100):
            state = {'stage_idx': 0, 'field_name': 'RPM', 'old_value': str(i), 'new_value': str(i+1)}
            self.manager.push_state(state)
        
        # Should only keep last 50
        self.assertEqual(len(self.manager.undo_stack), 50)


class TestTooltips(unittest.TestCase):
    def test_tooltip_exists_for_common_fields(self):
        """Test that tooltips exist for common fields"""
        common_fields = ['RPM', 'Loading (Psi)', 'Flow (Phi)', 'Reaction (R)', 'Mean Line Radius']
        for field in common_fields:
            tooltip = get_tooltip(field)
            self.assertIsNotNone(tooltip)
            self.assertGreater(len(tooltip), 0)
    
    def test_tooltip_exists_for_rotor_fields(self):
        """Test that tooltips exist for rotor fields"""
        rotor_fields = ['Rotor Diameter', 'Hub Diameter', 'Num of Blade (Rotor)']
        for field in rotor_fields:
            tooltip = get_tooltip(field)
            self.assertIsNotNone(tooltip)
            self.assertGreater(len(tooltip), 0)
    
    def test_tooltip_exists_for_stator_fields(self):
        """Test that tooltips exist for stator fields"""
        stator_fields = ['Duct ID', 'Duct Length', 'Num of Blade (Stator)']
        for field in stator_fields:
            tooltip = get_tooltip(field)
            self.assertIsNotNone(tooltip)
            self.assertGreater(len(tooltip), 0)
    
    def test_all_tooltips_are_strings(self):
        """Test that all tooltips are non-empty strings"""
        for field_name, tooltip in PARAMETER_TOOLTIPS.items():
            self.assertIsInstance(tooltip, str)
            self.assertGreater(len(tooltip), 0)


class TestPresets(unittest.TestCase):
    def test_preset_names_exist(self):
        """Test that preset names can be retrieved"""
        names = get_preset_names()
        self.assertIsInstance(names, list)
        self.assertGreater(len(names), 0)
    
    def test_get_preset_by_name(self):
        """Test retrieving preset by name"""
        names = get_preset_names()
        if names:
            preset = get_preset(names[0])
            self.assertIsNotNone(preset)
            self.assertIn('description', preset)
            self.assertIn('Stage', preset)
            self.assertIn('Rotor', preset)
            self.assertIn('Stator', preset)
    
    def test_preset_has_required_fields(self):
        """Test that presets have all required fields"""
        names = get_preset_names()
        for name in names:
            preset = get_preset(name)
            
            # Check Stage parameters
            self.assertIn('Reaction (R)', preset['Stage'])
            self.assertIn('Loading (Psi)', preset['Stage'])
            self.assertIn('Flow (Phi)', preset['Stage'])
            self.assertIn('RPM', preset['Stage'])
            self.assertIn('Mean Line Radius', preset['Stage'])
            
            # Check Rotor parameters
            self.assertIn('Rotor Diameter', preset['Rotor'])
            self.assertIn('Hub Diameter', preset['Rotor'])
            self.assertIn('Num of Blade (Rotor)', preset['Rotor'])
            
            # Check Stator parameters
            self.assertIn('Duct ID', preset['Stator'])
            self.assertIn('Duct Length', preset['Stator'])
            self.assertIn('Num of Blade (Stator)', preset['Stator'])
    
    def test_preset_description(self):
        """Test that preset descriptions exist"""
        names = get_preset_names()
        for name in names:
            description = get_preset_description(name)
            self.assertIsInstance(description, str)
            self.assertGreater(len(description), 0)
    
    def test_known_presets_exist(self):
        """Test that expected presets exist"""
        names = get_preset_names()
        expected_presets = [
            "Micro Turbine - Single Stage",
            "RC Ducted Fan - High Speed",
            "Industrial Compressor - Low Speed"
        ]
        for expected in expected_presets:
            self.assertIn(expected, names)


if __name__ == '__main__':
    unittest.main()
