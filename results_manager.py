import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd
from dataclasses import dataclass
import sqlite3
import hashlib
from pathlib import Path

@dataclass
class ScanResult:
    id: str
    timestamp: datetime
    target: str
    scan_type: str
    results: Dict[str, Any]
    risk_score: float
    status: str

class ResultsManager:
    def __init__(self, data_dir: str = "findings"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "scans.db")
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for scan results"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                target TEXT,
                scan_type TEXT,
                risk_score REAL,
                status TEXT,
                results_path TEXT
            )
        ''')
        
        # Create tips table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tips (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                reporter_type TEXT,
                scam_type TEXT,
                location TEXT,
                urgency TEXT,
                status TEXT,
                details_path TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_scan(self, scan_result: ScanResult) -> str:
        """Save scan results to database and filesystem"""
        try:
            # Generate unique ID if not provided
            if not scan_result.id:
                scan_result.id = self._generate_scan_id(scan_result.target)

            # Save detailed results to JSON file
            results_path = os.path.join(
                self.data_dir,
                f"scans/{scan_result.scan_type}",
                f"{scan_result.id}.json"
            )
            
            os.makedirs(os.path.dirname(results_path), exist_ok=True)
            
            with open(results_path, 'w') as f:
                json.dump({
                    "id": scan_result.id,
                    "timestamp": scan_result.timestamp.isoformat(),
                    "target": scan_result.target,
                    "scan_type": scan_result.scan_type,
                    "results": scan_result.results,
                    "risk_score": scan_result.risk_score,
                    "status": scan_result.status
                }, f, indent=2)

            # Save metadata to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO scans
                (id, timestamp, target, scan_type, risk_score, status, results_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                scan_result.id,
                scan_result.timestamp.isoformat(),
                scan_result.target,
                scan_result.scan_type,
                scan_result.risk_score,
                scan_result.status,
                results_path
            ))
            
            conn.commit()
            conn.close()

            return scan_result.id

        except Exception as e:
            print(f"Error saving scan results: {e}")
            raise

    def get_scan(self, scan_id: str) -> Optional[ScanResult]:
        """Retrieve scan results by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
                
            # Load detailed results from JSON file
            with open(row[6], 'r') as f:
                detailed_results = json.load(f)
                
            return ScanResult(
                id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                target=row[2],
                scan_type=row[3],
                risk_score=row[4],
                status=row[5],
                results=detailed_results["results"]
            )

        except Exception as e:
            print(f"Error retrieving scan results: {e}")
            return None
        finally:
            conn.close()

    def save_tip(self, tip_data: Dict[str, Any]) -> str:
        """Save submitted tip information"""
        try:
            tip_id = self._generate_tip_id()
            timestamp = datetime.now()
            
            # Save detailed tip data to JSON file
            details_path = os.path.join(
                self.data_dir,
                "tips",
                f"{tip_id}.json"
            )
            
            os.makedirs(os.path.dirname(details_path), exist_ok=True)
            
            with open(details_path, 'w') as f:
                json.dump({
                    "id": tip_id,
                    "timestamp": timestamp.isoformat(),
                    **tip_data
                }, f, indent=2)

            # Save metadata to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO tips
                (id, timestamp, reporter_type, scam_type, location, urgency, status, details_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tip_id,
                timestamp.isoformat(),
                tip_data.get('reporter_type'),
                tip_data.get('scam_type'),
                tip_data.get('location'),
                tip_data.get('urgency'),
                'new',
                details_path
            ))
            
            conn.commit()
            conn.close()

            return tip_id

        except Exception as e:
            print(f"Error saving tip: {e}")
            raise

    def get_recent_scans(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent scan results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp, target, scan_type, risk_score, status
                FROM scans
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "timestamp": row[1],
                    "target": row[2],
                    "scan_type": row[3],
                    "risk_score": row[4],
                    "status": row[5]
                })
            
            return results

        except Exception as e:
            print(f"Error retrieving recent scans: {e}")
            return []
        finally:
            conn.close()

    def get_high_risk_scans(self, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Get high-risk scan results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp, target, scan_type, risk_score, status
                FROM scans
                WHERE risk_score >= ?
                ORDER BY risk_score DESC
            ''', (threshold,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "timestamp": row[1],
                    "target": row[2],
                    "scan_type": row[3],
                    "risk_score": row[4],
                    "status": row[5]
                })
            
            return results

        except Exception as e:
            print(f"Error retrieving high-risk scans: {e}")
            return []
        finally:
            conn.close()

    def get_urgent_tips(self) -> List[Dict[str, Any]]:
        """Get urgent tips that need attention"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp, reporter_type, scam_type, location, urgency, status
                FROM tips
                WHERE urgency = 'high' AND status = 'new'
                ORDER BY timestamp DESC
            ''')
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "timestamp": row[1],
                    "reporter_type": row[2],
                    "scam_type": row[3],
                    "location": row[4],
                    "urgency": row[5],
                    "status": row[6]
                })
            
            return results

        except Exception as e:
            print(f"Error retrieving urgent tips: {e}")
            return []
        finally:
            conn.close()

    def update_tip_status(self, tip_id: str, new_status: str) -> bool:
        """Update the status of a tip"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE tips
                SET status = ?
                WHERE id = ?
            ''', (new_status, tip_id))
            
            conn.commit()
            return True

        except Exception as e:
            print(f"Error updating tip status: {e}")
            return False
        finally:
            conn.close()

    def generate_report(self, scan_ids: List[str]) -> Dict[str, Any]:
        """Generate a comprehensive report from multiple scans"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "scans": [],
            "summary": {
                "total_scans": len(scan_ids),
                "high_risk_count": 0,
                "average_risk_score": 0.0,
                "risk_factors": []
            }
        }

        try:
            risk_scores = []
            all_risk_factors = []

            for scan_id in scan_ids:
                scan_result = self.get_scan(scan_id)
                if scan_result:
                    report["scans"].append({
                        "id": scan_id,
                        "timestamp": scan_result.timestamp.isoformat(),
                        "target": scan_result.target,
                        "risk_score": scan_result.risk_score,
                        "key_findings": scan_result.results.get("risk_factors", [])
                    })
                    
                    risk_scores.append(scan_result.risk_score)
                    all_risk_factors.extend(scan_result.results.get("risk_factors", []))

            # Calculate summary statistics
            if risk_scores:
                report["summary"]["average_risk_score"] = sum(risk_scores) / len(risk_scores)
                report["summary"]["high_risk_count"] = len([s for s in risk_scores if s >= 0.7])

            # Aggregate common risk factors
            from collections import Counter
            risk_factor_counts = Counter(all_risk_factors)
            report["summary"]["risk_factors"] = [
                {"factor": factor, "count": count}
                for factor, count in risk_factor_counts.most_common(5)
            ]

        except Exception as e:
            report["error"] = str(e)

        return report

    def _generate_scan_id(self, target: str) -> str:
        """Generate unique scan ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_input = f"{target}{timestamp}{os.urandom(8).hex()}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def _generate_tip_id(self) -> str:
        """Generate unique tip ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = os.urandom(4).hex()
        return f"TIP_{timestamp}_{random_suffix}"
