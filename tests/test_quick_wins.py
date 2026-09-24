"""
Test quick win features
"""
import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from RecentFiles import RecentFilesManager
from ErrorLogger import logger
from DefaultParameters import get_default_parameters, validate_design_rules, RECOMMENDED_RANGES


class TestRecentFiles(unittest.TestCase):
    def setUp(self):
        """Create temporary config for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = RecentFilesManager()
        # Override config path for testing
        self.manager.config_file = Path(self.temp_dir) / 'test_recent.json'
    
    def tearDown(self):
        """Clean up temp files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_add_file(self):
        """Test adding files to recent list"""
        # Create a temp file
        test_file = Path(self.temp_dir) / 'test.json'
        test_file.touch()
        
        self.manager.add_file(str(test_file))
        recent = self.manager.get_recent_files()
        
        self.assertIn(str(test_file.absolute()), recent)
    
    def test_max_files(self):
        """Test that only max files are kept"""
        self.manager.max_files = 3
        
        # Add more than max
        for i in range(5):
            test_file = Path(self.temp_dir) / f'test{i}.json'
            test_file.touch()
            self.manager.add_file(str(test_file))
        
        recent = self.manager.get_recent_files()
        self.assertEqual(len(recent), 3)
    
    def test_remove_nonexistent(self):
        """Test that non-existent files are removed"""
        # Add real file
        test_file = Path(self.temp_dir) / 'test.json'
        test_file.touch()
        self.manager.add_file(str(test_file))
        
        # Add fake file
        self.manager.recent_files.append('/nonexistent/file.json')
        self.manager.save()
        
        # Get recent files filters non-existent
        recent = self.manager.get_recent_files()
        self.assertEqual(len(recent), 1)
    
    def test_clear(self):
        """Test clearing recent files"""
        test_file = Path(self.temp_dir) / 'test.json'
        test_file.touch()
        self.manager.add_file(str(test_file))
        
        self.manager.clear()
        recent = self.manager.get_recent_files()
        self.assertEqual(len(recent), 0)


class TestErrorLogger(unittest.TestCase):
    def test_logger_singleton(self):
        """Test that logger is a singleton"""
        from ErrorLogger import ErrorLogger
        logger1 = ErrorLogger()
        logger2 = ErrorLogger()
        self.assertIs(logger1, logger2)
    
    def test_log_file_exists(self):
        """Test that log file is created"""
        log_path = Path(logger.get_log_file_path())
        self.assertTrue(log_path.exists())
    
    def test_logging_methods(self):
        """Test various logging methods"""
        # These should not raise exceptions
        logger.debug("Test debug message")
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")


class TestDefaultParameters(unittest.TestCase):
    def test_get_defaults(self):
        """Test getting default parameters"""
        defaults = get_default_parameters()
        
        self.assertIn('Stage', defaults)
        self.assertIn('Rotor', defaults)
        self.assertIn('Stator', defaults)
        
        # Check stage has required fields
        self.assertIn('Reaction (R)', defaults['Stage'])
        self.assertIn('RPM', defaults['Stage'])
        
        # Check rotor has required fields
        self.assertIn('Rotor Diameter', defaults['Rotor'])
        self.assertIn('Num of Blade (Rotor)', defaults['Rotor'])
        
        # Check stator has required fields
        self.assertIn('Duct ID', defaults['Stator'])
        self.assertIn('Num of Blade (Stator)', defaults['Stator'])
    
    def test_defaults_are_valid(self):
        """Test that default values are within valid ranges"""
        defaults = get_default_parameters()
        
        # Test a few key parameters
        reaction = float(defaults['Stage']['Reaction (R)'])
        self.assertGreaterEqual(reaction, 0.0)
        self.assertLessEqual(reaction, 1.0)
        
        rpm = float(defaults['Stage']['RPM'])
        self.assertGreater(rpm, 0)
        
        rotor_dia = float(defaults['Rotor']['Rotor Diameter'])
        hub_dia = float(defaults['Rotor']['Hub Diameter'])
        self.assertGreater(rotor_dia, hub_dia)
    
    def test_validate_design_rules_good(self):
        """Test validation with good parameters"""
        defaults = get_default_parameters()
        warnings = validate_design_rules(
            defaults['Stage'],
            defaults['Rotor'],
            defaults['Stator']
        )
        
        # Defaults should have no warnings (or very few)
        self.assertIsInstance(warnings, list)
    
    def test_validate_design_rules_bad_hub_ratio(self):
        """Test validation catches bad hub/rotor ratio"""
        stage = {'Reaction (R)': '0.5'}
        rotor = {
            'Rotor Diameter': '100.0',
            'Hub Diameter': '90.0',  # Too large relative to rotor
            'Blade Clearance': '0.5',
            'Num of Blade (Rotor)': '12'
        }
        stator = {
            'Duct ID': '110.0',
            'Num of Blade (Stator)': '18'
        }
        
        warnings = validate_design_rules(stage, rotor, stator)
        self.assertGreater(len(warnings), 0)
    
    def test_validate_design_rules_bad_blade_ratio(self):
        """Test validation catches bad blade count ratio"""
        stage = {'Reaction (R)': '0.5'}
        rotor = {
            'Rotor Diameter': '100.0',
            'Hub Diameter': '50.0',
            'Blade Clearance': '0.5',
            'Num of Blade (Rotor)': '12'
        }
        stator = {
            'Duct ID': '110.0',
            'Num of Blade (Stator)': '6'  # Too few relative to rotor
        }
        
        warnings = validate_design_rules(stage, rotor, stator)
        self.assertGreater(len(warnings), 0)
    
    def test_recommended_ranges_exist(self):
        """Test that recommended ranges are defined"""
        self.assertGreater(len(RECOMMENDED_RANGES), 0)
        
        # Check a few key parameters have ranges
        self.assertIn('RPM', RECOMMENDED_RANGES)
        self.assertIn('Reaction (R)', RECOMMENDED_RANGES)
        self.assertIn('Rotor Diameter', RECOMMENDED_RANGES)
        
        # Check ranges are tuples of two numbers
        for param, range_tuple in RECOMMENDED_RANGES.items():
            self.assertIsInstance(range_tuple, tuple)
            self.assertEqual(len(range_tuple), 2)
            self.assertLess(range_tuple[0], range_tuple[1])


if __name__ == '__main__':
    unittest.main()
