import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from audio_processing import AudioAnalyzer
from osint_scanner import OSINTScanner
from geo_tracker import GeoTracker
from results_manager import ResultsManager

console = Console()

class ShadowIntelCLI:
    def __init__(self):
        self.audio_analyzer = AudioAnalyzer()
        self.osint_scanner = OSINTScanner()
        self.geo_tracker = GeoTracker()
        self.results_manager = ResultsManager()
        
    def display_menu(self):
        console.print(Panel.fit(
            "[green]SHADOW INTEL SYSTEM v1.0[/green]\n\n"
            "1. Audio Analysis\n"
            "2. OSINT Scanning\n"
            "3. Geolocation Tracking\n"
            "4. View Previous Results\n"
            "5. Exit\n",
            title="Main Menu",
            border_style="green"
        ))
        
    def run_audio_analysis(self):
        console.print("\n[green]== Audio Analysis ==[/green]")
        console.print("1. Start Recording")
        console.print("2. Stop Recording")
        console.print("3. Back to Main Menu")
        
        choice = input("\nEnter choice (1-3): ")
        
        if choice == "1":
            with Progress() as progress:
                task = progress.add_task("[green]Recording...", total=100)
                result = self.audio_analyzer.start_recording()
                for i in range(100):
                    time.sleep(0.1)
                    progress.update(task, advance=1)
                
                # Save results
                result_path = self.results_manager.save_audio_result(result)
                console.print(f"\n[green]Result:[/green] {result}")
                console.print(f"\n[blue]Results saved to:[/blue] {result_path}")
                
        elif choice == "2":
            console.print("\n[yellow]Stopping recording...[/yellow]")
            time.sleep(1)
            console.print("[green]Recording stopped[/green]")
            
    def run_osint_scan(self):
        console.print("\n[green]== OSINT Scanner ==[/green]")
        target = input("\nEnter target information (phone, email, username, etc): ")
        
        if target:
            with Progress() as progress:
                task = progress.add_task("[green]Scanning...", total=100)
                result = self.osint_scanner.scan_target(target)
                for i in range(100):
                    time.sleep(0.1)
                    progress.update(task, advance=1)
                
                # Save results
                result_path = self.results_manager.save_osint_result(target, result)
                console.print(f"\n[green]Results:[/green]")
                console.print(result)
                console.print(f"\n[blue]Results saved to:[/blue] {result_path}")
        else:
            console.print("[red]No target specified[/red]")
            
    def run_geo_tracking(self):
        console.print("\n[green]== Geolocation Tracking ==[/green]")
        target = input("\nEnter target IP or device identifier: ")
        
        if target:
            with Progress() as progress:
                task = progress.add_task("[green]Tracking...", total=100)
                result = self.geo_tracker.track_target(target)
                for i in range(100):
                    time.sleep(0.1)
                    progress.update(task, advance=1)
                
                # Save results
                result_path = self.results_manager.save_geo_result(target, result)
                console.print(f"\n[green]Results:[/green]")
                console.print(result)
                console.print(f"\n[blue]Results saved to:[/blue] {result_path}")
        else:
            console.print("[red]No target specified[/red]")
            
    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter choice (1-4): ")
            
            if choice == "1":
                self.run_audio_analysis()
            elif choice == "2":
                self.run_osint_scan()
            elif choice == "3":
                self.run_geo_tracking()
            elif choice == "4":
                self.view_results()
            elif choice == "5":
                console.print("\n[yellow]Exiting Shadow Intel System...[/yellow]")
                break
            else:
                console.print("\n[red]Invalid choice. Please try again.[/red]")
                
            input("\nPress Enter to continue...")
            
    def view_results(self):
        console.print("\n[green]== Previous Results ==[/green]")
        console.print("1. Audio Analysis Results")
        console.print("2. OSINT Scan Results")
        console.print("3. Geolocation Results")
        console.print("4. Back to Main Menu")
        
        choice = input("\nEnter choice (1-4): ")
        
        result_type = None
        if choice == "1":
            result_type = "audio"
        elif choice == "2":
            result_type = "osint"
        elif choice == "3":
            result_type = "geo"
        elif choice == "4":
            return
            
        if result_type:
            results = self.results_manager.get_latest_results(result_type)
            if results:
                console.print(f"\n[green]Latest {result_type.upper()} Results:[/green]")
                for type_, filepath in results[:5]:  # Show last 5 results
                    result = self.results_manager.read_result(filepath)
                    console.print(f"\n[blue]File:[/blue] {filepath}")
                    console.print(result)
            else:
                console.print(f"\n[yellow]No {result_type} results found[/yellow]")

if __name__ == "__main__":
    try:
        app = ShadowIntelCLI()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
