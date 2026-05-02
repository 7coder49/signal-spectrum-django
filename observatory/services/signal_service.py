from observatory.config.db import get_db
from observatory.models.signal import SignalLog, AnomalyEvent
from observatory.parsers.rf_parser import RFDataParser
from observatory.analyzers.engines import AnomalyEngine, OccupancyEngine
from datetime import datetime, timedelta

class SignalService:
    def __init__(self):
        self.db = get_db()
        self.use_mock = self.db is None
        
        # In-memory storage for mock mode
        if self.use_mock:
            self._mock_signals = []
            self._mock_anomalies = []
            print("⚠️ [WARNING] MongoDB not found. Operating in HIGH-FIDELITY MOCK MODE.")
        else:
            self.logs_col = self.db[SignalLog.COLLECTION_NAME]
            self.anomaly_col = self.db[AnomalyEvent.COLLECTION_NAME]

    def ingest_live_data(self, count=5):
        new_signals = [RFDataParser.generate_mock_signal() for _ in range(count)]
        
        if self.use_mock:
            self._mock_signals.extend(new_signals)
            # Keep only last 1000 signals to prevent memory issues
            self._mock_signals = self._mock_signals[-1000:]
            
            anomalies = AnomalyEngine.detect_spikes(new_signals)
            self._mock_anomalies.extend(anomalies)
            self._mock_anomalies = self._mock_anomalies[-100:]
        else:
            self.logs_col.insert_many(new_signals)
            anomalies = AnomalyEngine.detect_spikes(new_signals)
            if anomalies:
                self.anomaly_col.insert_many(anomalies)
        
        return new_signals

    def get_latest_signals(self, limit=50):
        if self.use_mock:
            return sorted(self._mock_signals, key=lambda x: x['timestamp'], reverse=True)[:limit]
        return list(self.logs_col.find().sort("timestamp", -1).limit(limit))

    def get_occupancy_stats(self):
        if self.use_mock:
            recent_signals = self._mock_signals[-50:]
        else:
            last_hour = datetime.utcnow() - timedelta(hours=1)
            recent_signals = list(self.logs_col.find({"timestamp": {"$gte": last_hour}}))
        
        return OccupancyEngine.calculate_band_utilization(recent_signals)

    def get_historical_logs(self, filters=None, limit=100, skip=0):
        if self.use_mock:
            return self.get_latest_signals(limit=limit) # Simplified for mock
        query = filters or {}
        return list(self.logs_col.find(query).sort("timestamp", -1).skip(skip).limit(limit))

    def get_anomalies(self, limit=20):
        if self.use_mock:
            return sorted(self._mock_anomalies, key=lambda x: x['timestamp'], reverse=True)[:limit]
        return list(self.anomaly_col.find().sort("timestamp", -1).limit(limit))
