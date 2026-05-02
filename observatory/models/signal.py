from datetime import datetime
from typing import Dict, Any

class SignalLog:
    """
    Schema representation for RF Signal Logs in MongoDB.
    
    Fields:
    - timestamp: datetime (UTC)
    - frequency: float (MHz)
    - signal_strength: float (dBm)
    - bandwidth: float (kHz)
    - modulation_type: str (e.g., AM, FM, QPSK, LoRa)
    - source_station: str (Identification if known)
    - occupancy_level: float (0.0 to 1.0)
    - anomaly_confidence: float (0.0 to 1.0)
    """
    
    COLLECTION_NAME = 'signal_logs'

    @staticmethod
    def to_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "timestamp": data.get("timestamp", datetime.utcnow()),
            "frequency": float(data.get("frequency", 0.0)),
            "signal_strength": float(data.get("signal_strength", -100.0)),
            "bandwidth": float(data.get("bandwidth", 0.0)),
            "modulation_type": data.get("modulation_type", "Unknown"),
            "source_station": data.get("source_station", "Unknown"),
            "occupancy_level": float(data.get("occupancy_level", 0.0)),
            "anomaly_confidence": float(data.get("anomaly_confidence", 0.0))
        }

class AnomalyEvent:
    """
    Schema for detected RF anomalies.
    """
    COLLECTION_NAME = 'anomaly_events'

    @staticmethod
    def to_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "timestamp": data.get("timestamp", datetime.utcnow()),
            "frequency": float(data.get("frequency")),
            "description": data.get("description", "Sudden spike detected"),
            "confidence": float(data.get("confidence", 0.0)),
            "severity": data.get("severity", "LOW") # LOW, MEDIUM, HIGH, CRITICAL
        }
