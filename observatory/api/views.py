from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from observatory.services.signal_service import SignalService
from observatory.serializers.signal_serializer import (
    SignalLogSerializer, AnomalyEventSerializer, OccupancyStatsSerializer
)

service = SignalService()

class LiveSpectrumView(APIView):
    def get(self, request):
        # Trigger ingestion to simulate live data
        service.ingest_live_data()
        signals = service.get_latest_signals(limit=20)
        serializer = SignalLogSerializer(signals, many=True)
        return Response(serializer.data)

class OccupancyAnalyticsView(APIView):
    def get(self, request):
        stats = service.get_occupancy_stats()
        serializer = OccupancyStatsSerializer(stats)
        return Response(serializer.data)

class AnomalyFeedView(APIView):
    def get(self, request):
        anomalies = service.get_anomalies()
        serializer = AnomalyEventSerializer(anomalies, many=True)
        return Response(serializer.data)

class SignalLogExplorerView(APIView):
    def get(self, request):
        limit = int(request.query_params.get('limit', 100))
        skip = int(request.query_params.get('skip', 0))
        logs = service.get_historical_logs(limit=limit, skip=skip)
        serializer = SignalLogSerializer(logs, many=True)
        return Response(serializer.data)

class AIInsightView(APIView):
    def get(self, request):
        # Simulate AI Insight Generation
        stats = service.get_occupancy_stats()
        anomalies = service.get_anomalies(limit=1)
        
        insights = []
        if stats['status'] == "CONGESTED":
            insights.append("High spectrum congestion detected in the monitored bands.")
        
        if anomalies:
            insights.append(f"Recent anomaly at {anomalies[0]['frequency']} MHz requires investigation.")
        
        insights.append("FM broadcast channels remain consistently occupied.")
        
        return Response({"insights": insights})

class ManualTriggerView(APIView):
    def post(self, request):
        data = service.trigger_burst()
        return Response({"status": "BURST_TRIGGERED", "data": data})
