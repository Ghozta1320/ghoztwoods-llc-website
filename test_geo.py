from geo_tracker import GeoTracker
from rich.console import Console
from rich.table import Table
import json
import time

console = Console()

def test_tracking():
    # Initialize tracker
    tracker = GeoTracker()
    
    # Test cases with various scenarios
    test_cases = [
        {
            "type": "Valid IP",
            "target": "8.8.8.8",  # Google DNS
            "expected_success": True
        },
        {
            "type": "Invalid IP",
            "target": "999.999.999.999",
            "expected_success": False
        },
        {
            "type": "Phone Number",
            "target": "+1234567890",
            "expected_success": True  # Should return "not implemented" status
        },
        {
            "type": "Device ID",
            "target": "DEV_123456",
            "expected_success": True  # Should return "not implemented" status
        },
        {
            "type": "Empty Input",
            "target": "",
            "expected_success": False
        }
    ]
    
    # Create results table
    table = Table(title="Geo Tracker Test Results")
    table.add_column("Test Type", style="cyan")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")
    
    console.print("\n[bold blue]Starting Geo Tracker Tests...[/bold blue]")
    
    for case in test_cases:
        console.print(f"\n[cyan]Testing {case['type']}[/cyan]")
        console.print(f"Target: {case['target']}")
        
        try:
            # Run tracking
            start_time = time.time()
            results = tracker.track_target(case['target'])
            duration = time.time() - start_time
            
            # Analyze results
            success = True
            details = []
            
            if "error" in results:
                success = False
                details.append(f"Error: {results['error']}")
            
            if "locations" in results:
                for loc_type, loc_data in results["locations"].items():
                    if isinstance(loc_data, dict):
                        if "error" in loc_data:
                            details.append(f"{loc_type}: {loc_data['error']}")
                        elif "coordinates" in loc_data:
                            details.append(f"{loc_type}: Found coordinates")
                        elif "status" in loc_data:
                            details.append(f"{loc_type}: {loc_data['status']}")
            
            # Check if map was generated
            if "map_path" in results:
                details.append("Map generated successfully")
            elif "map_error" in results:
                details.append(f"Map error: {results['map_error']}")
                
            # Add result to table
            status = "[green]PASS[/green]" if success == case["expected_success"] else "[red]FAIL[/red]"
            table.add_row(
                case["type"],
                case["target"],
                status,
                "\n".join(details)
            )
            
            # Display detailed results for debugging
            console.print("\n[yellow]Detailed Results:[/yellow]")
            console.print(json.dumps(results, indent=2))
            console.print(f"Processing Time: {duration:.2f} seconds")
            
        except Exception as e:
            table.add_row(
                case["type"],
                case["target"],
                "[red]ERROR[/red]",
                f"Test failed: {str(e)}"
            )
            
        console.print("\n" + "="*50)
    
    # Display final results table
    console.print("\n[bold green]Test Summary[/bold green]")
    console.print(table)

if __name__ == "__main__":
    try:
        test_tracking()
    except Exception as e:
        console.print(f"\n[red]Critical Test Error: {str(e)}[/red]")
