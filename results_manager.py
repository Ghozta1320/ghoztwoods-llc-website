import os
import json
from datetime import datetime

class ResultsManager:
    def __init__(self):
        # Create results directory structure
        self.base_dir = "findings"
        self.audio_dir = os.path.join(self.base_dir, "audio_analysis")
        self.osint_dir = os.path.join(self.base_dir, "osint_scans")
        self.geo_dir = os.path.join(self.base_dir, "geo_tracking")
        
        # Create directories if they don't exist
        for directory in [self.audio_dir, self.osint_dir, self.geo_dir]:
            os.makedirs(directory, exist_ok=True)
            
    def save_audio_result(self, result):
        """Save audio analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_analysis_{timestamp}.json"
        filepath = os.path.join(self.audio_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=4)
            
        # Save any audio recordings
        if result.get('recording_path'):
            recording_dir = os.path.join(self.audio_dir, "recordings")
            os.makedirs(recording_dir, exist_ok=True)
            # Copy recording file to results directory
            
        return filepath
        
    def save_osint_result(self, target, result):
        """Save OSINT scan results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"osint_scan_{timestamp}.json"
        filepath = os.path.join(self.osint_dir, filename)
        
        data = {
            "target": target,
            "timestamp": timestamp,
            "findings": result
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
        return filepath
        
    def save_geo_result(self, target, result):
        """Save geolocation tracking results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"geo_track_{timestamp}.json"
        filepath = os.path.join(self.geo_dir, filename)
        
        data = {
            "target": target,
            "timestamp": timestamp,
            "locations": result
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
        # Save map if available
        if result.get('map_path'):
            maps_dir = os.path.join(self.geo_dir, "maps")
            os.makedirs(maps_dir, exist_ok=True)
            # Copy map file to results directory
            
        return filepath
        
    def get_latest_results(self, result_type=None):
        """Get list of latest results, optionally filtered by type"""
        results = []
        
        if result_type in ['audio', None]:
            audio_files = self._get_directory_files(self.audio_dir)
            results.extend([('audio', f) for f in audio_files])
            
        if result_type in ['osint', None]:
            osint_files = self._get_directory_files(self.osint_dir)
            results.extend([('osint', f) for f in osint_files])
            
        if result_type in ['geo', None]:
            geo_files = self._get_directory_files(self.geo_dir)
            results.extend([('geo', f) for f in geo_files])
            
        # Sort by modification time, newest first
        results.sort(key=lambda x: os.path.getmtime(x[1]), reverse=True)
        return results
        
    def _get_directory_files(self, directory):
        """Get list of JSON files in directory"""
        if not os.path.exists(directory):
            return []
            
        files = []
        for file in os.listdir(directory):
            if file.endswith('.json'):
                files.append(os.path.join(directory, file))
        return files
        
    def read_result(self, filepath):
        """Read and return result file contents"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to read result file: {str(e)}"}

# Example usage
if __name__ == "__main__":
    manager = ResultsManager()
    print("Results Manager initialized. Findings will be saved in the 'findings' directory.")
