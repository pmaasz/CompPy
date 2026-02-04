import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from FileOps import StageOpen, StageSave


class TestFileOps(unittest.TestCase):
    """Test file operations"""
    
    def setUp(self):
        """Create temporary file for testing"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_filename = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up temporary file"""
        if os.path.exists(self.temp_filename):
            os.unlink(self.temp_filename)
    
    def test_stage_save_and_open(self):
        """Test saving and loading stage data"""
        # Create test data
        common = [
            {"RPM": "30000", "Loading (Psi)": "0.482", "Flow (Phi)": "0.691", 
             "Reaction (R)": "0.4", "Mean Line Radius": "47.455"}
        ]
        rotor = [
            {"Hub Diameter": "30.0", "X Twist (Rotor)": "50.0", 
             "Blade Thickness (Rotor)": "16", "Rotor Diameter": "60", 
             "Hub Length": "17", "Blade Clearance": "0", 
             "Y Twist (Rotor)": "0.0", "Root Chord (Rotor)": "20", 
             "Num of Blade (Rotor)": "24", "Tip Chord (Rotor)": "10.88"}
        ]
        stator = [
            {"Duct ID": "60", "Duct Length": "14.3", "Duct Thickness": "2", 
             "Num of Blade (Stator)": "13", "Mount Can Length": "14.3", 
             "Mount Can Dia": "30", "Mount Can Loc": "0", 
             "Blade Thickness (Stator)": "16", "Root Chord (Stator)": "15", 
             "Tip Chord (Stator)": "9.405", "X Twist (Stator)": "50", 
             "Y Twist (Stator)": "0"}
        ]
        
        # Save the data
        StageSave(self.temp_filename, common, rotor, stator)
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.temp_filename))
        
        # Load the data back
        loaded_data = list(StageOpen(self.temp_filename))
        
        # Verify we got the right number of stages
        self.assertEqual(len(loaded_data), 1)
        
        # Verify the data matches
        loaded_common, loaded_rotor, loaded_stator = loaded_data[0]
        
        self.assertEqual(loaded_common["RPM"], "30000")
        self.assertEqual(loaded_rotor["Hub Diameter"], "30.0")
        self.assertEqual(loaded_stator["Duct ID"], "60")
    
    def test_stage_save_multiple_stages(self):
        """Test saving and loading multiple stages"""
        common = [
            {"RPM": "30000", "Loading (Psi)": "0.482", "Flow (Phi)": "0.691", 
             "Reaction (R)": "0.4", "Mean Line Radius": "47.455"},
            {"RPM": "35000", "Loading (Psi)": "0.5", "Flow (Phi)": "0.7", 
             "Reaction (R)": "0.45", "Mean Line Radius": "50.0"}
        ]
        rotor = [
            {"Hub Diameter": "30.0", "Rotor Diameter": "60"},
            {"Hub Diameter": "32.0", "Rotor Diameter": "62"}
        ]
        stator = [
            {"Duct ID": "60", "Duct Length": "14.3"},
            {"Duct ID": "62", "Duct Length": "15.0"}
        ]
        
        StageSave(self.temp_filename, common, rotor, stator)
        loaded_data = list(StageOpen(self.temp_filename))
        
        self.assertEqual(len(loaded_data), 2)
        
        # Check first stage
        self.assertEqual(loaded_data[0][0]["RPM"], "30000")
        self.assertEqual(loaded_data[0][1]["Hub Diameter"], "30.0")
        
        # Check second stage
        self.assertEqual(loaded_data[1][0]["RPM"], "35000")
        self.assertEqual(loaded_data[1][1]["Hub Diameter"], "32.0")
    
    def test_stage_save_with_json_extension(self):
        """Test that .json extension is not duplicated"""
        filename = self.temp_filename
        
        common = [{"RPM": "30000"}]
        rotor = [{"Hub Diameter": "30.0"}]
        stator = [{"Duct ID": "60"}]
        
        StageSave(filename, common, rotor, stator)
        
        # Verify file exists and has proper extension
        self.assertTrue(os.path.exists(filename))
        self.assertTrue(filename.endswith('.json'))


if __name__ == '__main__':
    unittest.main()
