from osint_scanner import OSINTScanner
from rich.console import Console
import json

console = Console()

def test_scan():
    # Initialize scanner
    scanner = OSINTScanner()
    
    # Test data with multiple types of information
    test_target = """
    Contact: john.doe@example.com
    Phone: +1234567890
    Website: http://malware.com
    IP: 1.2.3.4
    """
    
    console.print("\n[green]Testing OSINT Scanner...[/green]")
    console.print(f"\n[blue]Test Target:[/blue]\n{test_target}")
    
    # Run scan
    results = scanner.scan_target(test_target)
    
    # Display results
    console.print("\n[green]Scan Results:[/green]")
    console.print(json.dumps(results, indent=2))
    
    # Verify each component
    console.print("\n[yellow]Verification:[/yellow]")
    
    if "emails" in results["findings"]:
        console.print("✓ Email analysis completed")
    if "phones" in results["findings"]:
        console.print("✓ Phone analysis completed")
    if "ips" in results["findings"]:
        console.print("✓ IP analysis completed")
    if "domains" in results["findings"]:
        console.print("✓ Domain analysis completed")
        
    console.print(f"\n[blue]Risk Level:[/blue] {results['analysis']['risk_level']}")
    console.print(f"[blue]Threats Found:[/blue] {results['analysis']['threats_found']}")
    
    console.print("\n[green]Recommendations:[/green]")
    for rec in results["analysis"]["recommendations"]:
        console.print(f"• {rec}")

if __name__ == "__main__":
    try:
        test_scan()
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
