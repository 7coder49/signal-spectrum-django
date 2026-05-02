from typing import List, Dict
from observatory.models.signal import AnomalyEvent

class AnomalyEngine:
    """
    Analyzes signal logs to detect RF anomalies.
    """

    @staticmethod
    def detect_spikes(recent_signals: List[Dict]) -> List[Dict]:
        anomalies = []
        for signal in recent_signals:
            if signal.get('anomaly_confidence', 0) > 0.7:
                event = {
                    "timestamp": signal['timestamp'],
                    "frequency": signal['frequency'],
                    "description": f"High intensity burst detected: {signal['signal_strength']} dBm",
                    "confidence": signal['anomaly_confidence'],
                    "severity": "HIGH" if signal['signal_strength'] > -50 else "MEDIUM"
                }
                anomalies.append(AnomalyEvent.to_mongo(event))
        return anomalies

class OccupancyEngine:
    """
    Calculates spectrum utilization metrics.
    """

    @staticmethod
    def calculate_band_utilization(signals: List[Dict]) -> Dict:
        if not signals:
            return {}
        
        avg_occupancy = sum(s.get('occupancy_level', 0) for s in signals) / len(signals)
        peak_freq = max(signals, key=lambda x: x.get('signal_strength', -100))['frequency']
        
        return {
            "average_occupancy": round(avg_occupancy, 2),
            "peak_frequency": peak_freq,
            "signal_count": len(signals),
            "status": "CONGESTED" if avg_occupancy > 0.7 else "OPTIMAL" if avg_occupancy > 0.3 else "QUIET"
        }
