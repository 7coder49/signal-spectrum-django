import json
import random
import os
from datetime import datetime
from observatory.models.signal import SignalLog

class GlobalReplayParser:
    """
    Replays high-fidelity real-world signal captures in a loop.
    """
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'global_data.json')
        with open(self.data_path, 'r') as f:
            self.base_data = json.load(f)

    def get_live_stream(self):
        """
        Picks a random subset of real-world signals and adds slight noise 
        to simulate a live antenna.
        """
        active_signals = random.sample(self.base_data, k=min(4, len(self.base_data)))
        logs = []
        
        for item in active_signals:
            # Add slight signal fading and frequency drift simulation
            noise_strength = random.uniform(-2.0, 2.0)
            noise_freq = random.uniform(-0.005, 0.005)
            
            logs.append(SignalLog.to_mongo({
                "timestamp": datetime.utcnow(),
                "frequency": round(item['freq'] + noise_freq, 4),
                "signal_strength": round(item['strength'] + noise_strength, 1),
                "bandwidth": 25.0,
                "modulation_type": item['mod'],
                "source_station": item['name'],
                "occupancy_level": random.uniform(0.1, 0.4),
                "anomaly_confidence": 0.05
            }))
            
        return logs
