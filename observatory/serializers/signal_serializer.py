from rest_framework import serializers

class SignalLogSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    frequency = serializers.FloatField()
    signal_strength = serializers.FloatField()
    bandwidth = serializers.FloatField()
    modulation_type = serializers.CharField()
    source_station = serializers.CharField()
    occupancy_level = serializers.FloatField()
    anomaly_confidence = serializers.FloatField()

class AnomalyEventSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    frequency = serializers.FloatField()
    description = serializers.CharField()
    confidence = serializers.FloatField()
    severity = serializers.CharField()

class OccupancyStatsSerializer(serializers.Serializer):
    average_occupancy = serializers.FloatField()
    peak_frequency = serializers.FloatField()
    signal_count = serializers.IntegerField()
    status = serializers.CharField()
