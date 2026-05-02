import random
from datetime import datetime, timedelta
from observatory.models.signal import SignalLog

class RFDataParser:
    """
    Service to parse incoming RF data or simulate live feeds.
    """
    
    MODULATIONS = ["FM", "AM", "QPSK", "LoRa", "OFDM", "DSSS"]
    STATIONS = ["GBS-Alpha", "TCOM-7", "SDR-Local-01", "SatNet-9", "Public-Node-B"]

    @classmethod
    def generate_mock_signal(cls, base_freq: float = 433.0) -> dict:
        """
        Generates a realistic mock signal record.
        """
        # Add some randomness to frequency
        freq = base_freq + random.uniform(-5.0, 5.0)
        strength = random.uniform(-110.0, -40.0)
        
        # Simple anomaly logic: very high strength or unusual frequency
        anomaly_conf = 0.0
        if strength > -50.0:
            anomaly_conf = random.uniform(0.7, 0.95)
        elif random.random() > 0.98:
            anomaly_conf = random.uniform(0.5, 0.8)

        data = {
            "timestamp": datetime.utcnow(),
            "frequency": round(freq, 4),
            "signal_strength": round(strength, 2),
            "bandwidth": random.choice([12.5, 25.0, 50.0, 200.0]),
            "modulation_type": random.choice(cls.MODULATIONS),
            "source_station": random.choice(cls.STATIONS),
            "occupancy_level": round(random.uniform(0.1, 0.9), 2),
            "anomaly_confidence": round(anomaly_conf, 2)
        }
        return SignalLog.to_mongo(data)

    @classmethod
    def parse_sigmf_metadata(cls, metadata: dict) -> dict:
        """
        Placeholder for SigMF metadata parsing logic.
        """
        # Logic to extract frequency, strength, etc from SigMF
        pass
