import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import json
from datetime import datetime
from audio_processing import AudioAnalyzer
from osint_scanner import OSINTScanner
from geo_tracker import GeoTracker
from results_manager import ResultsManager

class ShadowIntelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shadow Intel System")
        self.root.configure(bg='black')
        self.root.geometry("1000x600")
        
        # Configure style
        style = ttk.Style()
        style.configure("TNotebook", background='black')
        style.configure("TFrame", background='black')
        style.configure("TButton", 
                       background='#2b2b2b',
                       foreground='#00ff00',
                       borderwidth=1)
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.audio_tab = ttk.Frame(self.notebook)
        self.osint_tab = ttk.Frame(self.notebook)
        self.geo_tab = ttk.Frame(self.notebook)
        
        # Results Tab
        self.results_tab = ttk.Frame(self.notebook)
        self.setup_results_tab()
        
        self.notebook.add(self.audio_tab, text='Audio Analysis')
        self.notebook.add(self.osint_tab, text='OSINT Scanner')
        self.notebook.add(self.geo_tab, text='Geolocation')
        self.notebook.add(self.results_tab, text='Previous Results')
        
        # Initialize components
        self.setup_audio_tab()
        self.setup_osint_tab()
        self.setup_geo_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="System Status: READY")
        self.status_bar = tk.Label(root, 
                                 textvariable=self.status_var,
                                 fg='#00ff00',
                                 bg='black')
        self.status_bar.pack(side='bottom', fill='x', padx=5, pady=5)
        
        # Initialize components
        self.audio_analyzer = AudioAnalyzer()
        self.osint_scanner = OSINTScanner()
        self.geo_tracker = GeoTracker()
        self.results_manager = ResultsManager()
        
    def setup_audio_tab(self):
        # Controls frame
        controls = tk.Frame(self.audio_tab, bg='black')
        controls.pack(fill='x', padx=5, pady=5)
        
        self.record_btn = tk.Button(controls,
                                  text="Start Recording",
                                  command=self.start_recording,
                                  bg='#2b2b2b',
                                  fg='#00ff00')
        self.record_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(controls,
                                text="Stop Recording",
                                command=self.stop_recording,
                                bg='#2b2b2b',
                                fg='#00ff00')
        self.stop_btn.pack(side='left', padx=5)
        
        # Output area
        self.audio_output = scrolledtext.ScrolledText(self.audio_tab,
                                                    bg='black',
                                                    fg='#00ff00',
                                                    height=20)
        self.audio_output.pack(fill='both', expand=True, padx=5, pady=5)
        
    def setup_osint_tab(self):
        # Input frame
        input_frame = tk.Frame(self.osint_tab, bg='black')
        input_frame.pack(fill='x', padx=5, pady=5)
        
        self.osint_input = scrolledtext.ScrolledText(input_frame,
                                                   bg='black',
                                                   fg='#00ff00',
                                                   height=4)
        self.osint_input.pack(side='left', fill='both', expand=True, padx=5)
        
        self.scan_btn = tk.Button(input_frame,
                                text="Start OSINT Scan",
                                command=self.start_osint_scan,
                                bg='#2b2b2b',
                                fg='#00ff00')
        self.scan_btn.pack(side='right', padx=5)
        
        # Output area
        self.osint_output = scrolledtext.ScrolledText(self.osint_tab,
                                                    bg='black',
                                                    fg='#00ff00',
                                                    height=20)
        self.osint_output.pack(fill='both', expand=True, padx=5, pady=5)
        
    def setup_geo_tab(self):
        # Input frame
        input_frame = tk.Frame(self.geo_tab, bg='black')
        input_frame.pack(fill='x', padx=5, pady=5)
        
        self.geo_input = scrolledtext.ScrolledText(input_frame,
                                                bg='black',
                                                fg='#00ff00',
                                                height=4)
        self.geo_input.pack(side='left', fill='both', expand=True, padx=5)
        
        self.track_btn = tk.Button(input_frame,
                                 text="Track Location",
                                 command=self.start_tracking,
                                 bg='#2b2b2b',
                                 fg='#00ff00')
        self.track_btn.pack(side='right', padx=5)
        
        # Output area
        self.geo_output = scrolledtext.ScrolledText(self.geo_tab,
                                                 bg='black',
                                                 fg='#00ff00',
                                                 height=20)
        self.geo_output.pack(fill='both', expand=True, padx=5, pady=5)
        
    def update_status(self, message):
        self.status_var.set(f"System Status: {message}")
        
    def start_recording(self):
        self.update_status("Recording audio...")
        self.record_btn.config(state='disabled')
        threading.Thread(target=self._record_audio).start()
        
    def stop_recording(self):
        self.update_status("Processing audio...")
        self.record_btn.config(state='normal')
        
    def start_osint_scan(self):
        target = self.osint_input.get('1.0', 'end-1c')
        if not target:
            self.update_status("Error: No target specified")
            return
            
        self.update_status("Starting OSINT scan...")
        self.scan_btn.config(state='disabled')
        threading.Thread(target=self._run_osint_scan, args=(target,)).start()
        
    def start_tracking(self):
        target = self.geo_input.get('1.0', 'end-1c')
        if not target:
            self.update_status("Error: No target specified")
            return
            
        self.update_status("Starting geolocation tracking...")
        self.track_btn.config(state='disabled')
        threading.Thread(target=self._run_tracking, args=(target,)).start()
        
    def format_result(self, result):
        """Format result dictionary for display"""
        if isinstance(result, dict):
            output = ""
            for key, value in result.items():
                output += f"\n{key.replace('_', ' ').title()}: "
                if isinstance(value, dict):
                    output += "\n"
                    for k, v in value.items():
                        output += f"  - {k}: {v}\n"
                else:
                    output += f"{value}\n"
            return output
        return str(result)

    def _record_audio(self):
        try:
            result = self.audio_analyzer.start_recording()
            result_path = self.results_manager.save_audio_result(result)
            
            # Display formatted results
            output = "=== Audio Analysis Results ===\n"
            output += self.format_result(result)
            output += f"\nResults saved to: {result_path}"
            
            self.audio_output.delete('1.0', 'end')
            self.audio_output.insert('end', output)
        except Exception as e:
            self.audio_output.insert('end', f"\nError: {str(e)}")
        finally:
            self.record_btn.config(state='normal')
            self.update_status("Ready")
            
    def _run_osint_scan(self, target):
        try:
            result = self.osint_scanner.scan_target(target)
            result_path = self.results_manager.save_osint_result(target, result)
            
            # Display formatted results
            output = f"=== OSINT Scan Results for {target} ===\n"
            output += self.format_result(result)
            output += f"\nResults saved to: {result_path}"
            
            self.osint_output.delete('1.0', 'end')
            self.osint_output.insert('end', output)
        except Exception as e:
            self.osint_output.insert('end', f"\nError: {str(e)}")
        finally:
            self.scan_btn.config(state='normal')
            self.update_status("Ready")
            
    def setup_results_tab(self):
        # Results type selection
        controls = tk.Frame(self.results_tab, bg='black')
        controls.pack(fill='x', padx=5, pady=5)
        
        self.results_var = tk.StringVar(value="Audio Analysis")
        results_types = ["Audio Analysis", "OSINT Scans", "Geolocation"]
        self.results_combo = ttk.Combobox(controls, 
                                        values=results_types,
                                        textvariable=self.results_var,
                                        state='readonly')
        self.results_combo.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(controls,
                              text="Refresh Results",
                              command=self.refresh_results,
                              bg='#2b2b2b',
                              fg='#00ff00')
        refresh_btn.pack(side='left', padx=5)
        
        # Results display
        self.results_output = scrolledtext.ScrolledText(self.results_tab,
                                                      bg='black',
                                                      fg='#00ff00',
                                                      height=20)
        self.results_output.pack(fill='both', expand=True, padx=5, pady=5)
        
    def refresh_results(self):
        result_type = self.results_var.get().lower().split()[0]
        results = self.results_manager.get_latest_results(result_type)
        
        self.results_output.delete('1.0', 'end')
        if results:
            output = f"=== Latest {result_type.title()} Results ===\n"
            for type_, filepath in results[:5]:  # Show last 5 results
                result = self.results_manager.read_result(filepath)
                output += "\n" + "="*50 + "\n"
                output += f"Timestamp: {filepath.split('_')[-1].split('.')[0]}\n"
                output += self.format_result(result)
                output += "\n"
            self.results_output.insert('end', output)
        else:
            self.results_output.insert('end', f"No {result_type} results found")
            
    def _run_tracking(self, target):
        try:
            result = self.geo_tracker.track_target(target)
            result_path = self.results_manager.save_geo_result(target, result)
            
            # Display formatted results
            output = f"=== Geolocation Results for {target} ===\n"
            output += self.format_result(result)
            output += f"\nResults saved to: {result_path}"
            
            self.geo_output.delete('1.0', 'end')
            self.geo_output.insert('end', output)
        except Exception as e:
            self.geo_output.insert('end', f"\nError: {str(e)}")
        finally:
            self.track_btn.config(state='normal')
            self.update_status("Ready")

def main():
    root = tk.Tk()
    app = ShadowIntelGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
