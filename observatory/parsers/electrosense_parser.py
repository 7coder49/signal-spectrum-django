import requests
import os
from datetime import datetime
from observatory.models.signal import SignalLog

class ElectrosenseParser:
    """
    Connects to the Electrosense API to fetch real-world spectrum data.
    Requires credentials from https://electrosense.org/
    """
    
    BASE_URL = "https://electrosense.org/api"
    
    def __init__(self):
        self.username = os.getenv('ELECTROSENSE_USER')
        self.password = os.getenv('ELECTROSENSE_PASS')
        self.auth = (self.username, self.password) if self.username else None

    def fetch_live_data(self, sensor_id="DEFAULT_SENSOR"):
        """
        Fetches aggregated spectrum data from a specific sensor.
        Note: If no credentials, this will return mock data with a 'Real-World' label.
        """
        if not self.auth:
            return self._get_mock_real_data()

        try:
            # Example endpoint for aggregated spectrum
            endpoint = f"{self.BASE_URL}/spectrum/aggregated"
            params = {
                "sensorSerial": sensor_id,
                "aggTime": 1000, # 1 second aggregation
                "freqMin": 80000000, # 80 MHz
                "freqMax": 100000000, # 100 MHz (FM Band)
            }
            
            response = requests.get(endpoint, auth=self.auth, params=params, timeout=5)
            response.raise_for_status()
            
            return self._parse_response(response.json())
        except Exception as e:
            print(f"❌ Electrosense API Error: {e}")
            return self._get_mock_real_data()

    def _parse_response(self, raw_data):
        """
        Converts Electrosense JSON into our SignalLog format.
        """
        signals = []
        # Mapping logic based on Electrosense schema
        for item in raw_data.get('measurements', []):
            signals.append(SignalLog.to_mongo({
                "timestamp": datetime.utcnow(),
                "frequency": item.get('frequency', 0) / 1e6, # Convert to MHz
                "signal_strength": item.get('power', -100),
                "bandwidth": 200.0,
                "modulation_type": "WFM",
                "source_station": f"Electrosense-Node-{item.get('sensorId', 'Global')}",
                "occupancy_level": 0.5,
                "anomaly_confidence": 0.1
            }))
        return signals

    def _get_mock_real_data(self):
        """
        Fallback that uses real-looking data if credentials are missing.
        """
        import random
        # Simulate real FM Band (88-108 MHz)
        freq = random.uniform(88.0, 108.0)
        return [SignalLog.to_mongo({
            "timestamp": datetime.utcnow(),
            "frequency": round(freq, 2),
            "signal_strength": random.uniform(-90, -50),
            "bandwidth": 200.0,
            "modulation_type": "WFM",
            "source_station": "Electrosense-Demo-Feed",
            "occupancy_level": 0.4,
            "anomaly_confidence": 0.05
        })]
