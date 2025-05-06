import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QTextEdit, QProgressBar,
                           QTabWidget, QFrame, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from audio_processing import AudioAnalyzer
from osint_scanner import OSINTScanner
from geo_tracker import GeoTracker
from results_manager import ResultsManager

class AnalysisThread(QThread):
    progress_update = pyqtSignal(int)
    result_ready = pyqtSignal(dict)
    
    def __init__(self, analyzer_type, data):
        super().__init__()
        self.analyzer_type = analyzer_type
        self.data = data
        
    def run(self):
        try:
            if self.analyzer_type == "audio":
                analyzer = AudioAnalyzer()
                for i in range(0, 101, 10):
                    self.progress_update.emit(i)
                    time.sleep(0.1)
                result = analyzer.analyze_audio(self.data)
                
            elif self.analyzer_type == "osint":
                scanner = OSINTScanner()
                for i in range(0, 101, 10):
                    self.progress_update.emit(i)
                    time.sleep(0.1)
                result = scanner.scan_target(self.data)
                
            elif self.analyzer_type == "geo":
                tracker = GeoTracker()
                for i in range(0, 101, 10):
                    self.progress_update.emit(i)
                    time.sleep(0.1)
                result = tracker.track_target(self.data)
                
            self.result_ready.emit(result)
        except Exception as e:
            self.result_ready.emit({"error": str(e)})

class ShadowIntel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shadow Intel - Advanced Analysis System")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 12px;
            }
            QPushButton {
                background-color: #2b2b2b;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px;
                font-family: 'Courier New';
            }
            QPushButton:hover {
                background-color: #3b3b3b;
            }
            QTextEdit {
                background-color: #000000;
                color: #00ff00;
                border: 1px solid #00ff00;
                font-family: 'Courier New';
            }
            QProgressBar {
                border: 1px solid #00ff00;
                background-color: #1a1a1a;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
            }
            QTabWidget::pane {
                border: 1px solid #00ff00;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background-color: #3b3b3b;
            }
        """)
        
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(1000, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("[ SHADOW INTEL SYSTEM v1.0 ]")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Status bar
        self.status_bar = QLabel("System Status: READY")
        self.status_bar.setStyleSheet("color: #00ff00; font-weight: bold;")
        layout.addWidget(self.status_bar)
        
        # Tab widget
        tab_widget = QTabWidget()
        
        # Audio Analysis Tab
        audio_tab = QWidget()
        audio_layout = QVBoxLayout()
        
        audio_controls = QHBoxLayout()
        self.record_btn = QPushButton("Start Recording")
        self.stop_btn = QPushButton("Stop Recording")
        self.record_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)
        audio_controls.addWidget(self.record_btn)
        audio_controls.addWidget(self.stop_btn)
        
        self.audio_output = QTextEdit()
        self.audio_output.setReadOnly(True)
        self.audio_output.setPlaceholderText("Audio analysis results will appear here...")
        
        audio_layout.addLayout(audio_controls)
        audio_layout.addWidget(self.audio_output)
        audio_tab.setLayout(audio_layout)
        
        # OSINT Tab
        osint_tab = QWidget()
        osint_layout = QVBoxLayout()
        
        input_layout = QHBoxLayout()
        self.osint_input = QTextEdit()
        self.osint_input.setPlaceholderText("Enter target information (phone, email, username, etc)...")
        self.osint_input.setMaximumHeight(100)
        self.scan_btn = QPushButton("Start OSINT Scan")
        self.scan_btn.clicked.connect(self.start_osint_scan)
        input_layout.addWidget(self.osint_input)
        input_layout.addWidget(self.scan_btn)
        
        self.osint_output = QTextEdit()
        self.osint_output.setReadOnly(True)
        self.osint_output.setPlaceholderText("OSINT scan results will appear here...")
        
        osint_layout.addLayout(input_layout)
        osint_layout.addWidget(self.osint_output)
        osint_tab.setLayout(osint_layout)
        
        # Geolocation Tab
        geo_tab = QWidget()
        geo_layout = QVBoxLayout()
        
        geo_input = QHBoxLayout()
        self.target_input = QTextEdit()
        self.target_input.setPlaceholderText("Enter target IP or device identifier...")
        self.target_input.setMaximumHeight(100)
        self.track_btn = QPushButton("Track Location")
        self.track_btn.clicked.connect(self.start_tracking)
        geo_input.addWidget(self.target_input)
        geo_input.addWidget(self.track_btn)
        
        self.geo_output = QTextEdit()
        self.geo_output.setReadOnly(True)
        self.geo_output.setPlaceholderText("Geolocation tracking results will appear here...")
        
        geo_layout.addLayout(geo_input)
        geo_layout.addWidget(self.geo_output)
        geo_tab.setLayout(geo_layout)
        
        # Results Tab
        results_tab = QWidget()
        results_layout = QVBoxLayout()
        
        results_type = QHBoxLayout()
        self.results_combo = QComboBox()
        self.results_combo.addItems(["Audio Analysis", "OSINT Scans", "Geolocation"])
        refresh_btn = QPushButton("Refresh Results")
        refresh_btn.clicked.connect(self.refresh_results)
        results_type.addWidget(self.results_combo)
        results_type.addWidget(refresh_btn)
        
        self.results_output = QTextEdit()
        self.results_output.setReadOnly(True)
        self.results_output.setPlaceholderText("Select result type and click refresh...")
        
        results_layout.addLayout(results_type)
        results_layout.addWidget(self.results_output)
        results_tab.setLayout(results_layout)
        
        # Add tabs to widget
        tab_widget.addTab(audio_tab, "Audio Analysis")
        tab_widget.addTab(osint_tab, "OSINT Scanner")
        tab_widget.addTab(geo_tab, "Geolocation")
        tab_widget.addTab(results_tab, "Previous Results")
        
        layout.addWidget(tab_widget)
        
        # Progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Initialize components
        self.audio_analyzer = AudioAnalyzer()
        self.osint_scanner = OSINTScanner()
        self.geo_tracker = GeoTracker()
        self.results_manager = ResultsManager()
        
    def start_recording(self):
        self.update_status("Recording audio...")
        self.record_btn.setEnabled(False)
        self.audio_thread = AnalysisThread("audio", None)
        self.audio_thread.progress_update.connect(self.update_progress)
        self.audio_thread.result_ready.connect(self.handle_audio_result)
        self.audio_thread.start()
        
    def stop_recording(self):
        self.update_status("Processing audio...")
        self.record_btn.setEnabled(True)
        
    def start_osint_scan(self):
        target = self.osint_input.toPlainText()
        if not target:
            self.update_status("Error: No target specified")
            return
            
        self.update_status("Starting OSINT scan...")
        self.scan_btn.setEnabled(False)
        self.osint_thread = AnalysisThread("osint", target)
        self.osint_thread.progress_update.connect(self.update_progress)
        self.osint_thread.result_ready.connect(self.handle_osint_result)
        self.osint_thread.start()
        
    def start_tracking(self):
        target = self.target_input.toPlainText()
        if not target:
            self.update_status("Error: No target specified")
            return
            
        self.update_status("Starting geolocation tracking...")
        self.track_btn.setEnabled(False)
        self.geo_thread = AnalysisThread("geo", target)
        self.geo_thread.progress_update.connect(self.update_progress)
        self.geo_thread.result_ready.connect(self.handle_geo_result)
        self.geo_thread.start()
        
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

    def handle_audio_result(self, result):
        result_path = self.results_manager.save_audio_result(result)
        
        # Display formatted results
        output = "=== Audio Analysis Results ===\n"
        output += self.format_result(result)
        output += f"\nResults saved to: {result_path}"
        
        self.audio_output.setText(output)
        self.update_status("Audio analysis complete")
        self.record_btn.setEnabled(True)
        
    def handle_osint_result(self, result):
        target = self.osint_input.toPlainText()
        result_path = self.results_manager.save_osint_result(target, result)
        
        # Display formatted results
        output = f"=== OSINT Scan Results for {target} ===\n"
        output += self.format_result(result)
        output += f"\nResults saved to: {result_path}"
        
        self.osint_output.setText(output)
        self.update_status("OSINT scan complete")
        self.scan_btn.setEnabled(True)
        
    def handle_geo_result(self, result):
        target = self.target_input.toPlainText()
        result_path = self.results_manager.save_geo_result(target, result)
        
        # Display formatted results
        output = f"=== Geolocation Results for {target} ===\n"
        output += self.format_result(result)
        output += f"\nResults saved to: {result_path}"
        
        self.geo_output.setText(output)
        self.update_status("Geolocation tracking complete")
        self.track_btn.setEnabled(True)
        
    def update_status(self, message):
        self.status_bar.setText(f"System Status: {message}")
        
    def update_progress(self, value):
        self.progress.setValue(value)
        
    def refresh_results(self):
        result_type = self.results_combo.currentText().lower().split()[0]
        results = self.results_manager.get_latest_results(result_type)
        
        if results:
            output = f"=== Latest {result_type.title()} Results ===\n"
            for type_, filepath in results[:5]:
                result = self.results_manager.read_result(filepath)
                output += "\n" + "="*50 + "\n"
                output += f"Timestamp: {filepath.split('_')[-1].split('.')[0]}\n"
                output += self.format_result(result)
                output += "\n"
            self.results_output.setText(output)
        else:
            self.results_output.setText(f"No {result_type} results found")

def main():
    app = QApplication(sys.argv)
    window = ShadowIntel()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
