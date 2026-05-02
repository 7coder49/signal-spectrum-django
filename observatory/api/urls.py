from django.urls import path
from .views import (
    LiveSpectrumView, OccupancyAnalyticsView, 
    AnomalyFeedView, SignalLogExplorerView, AIInsightView
)

urlpatterns = [
    path('live/', LiveSpectrumView.as_view(), name='live-spectrum'),
    path('analytics/occupancy/', OccupancyAnalyticsView.as_view(), name='occupancy-analytics'),
    path('anomalies/', AnomalyFeedView.as_view(), name='anomaly-feed'),
    path('logs/', SignalLogExplorerView.as_view(), name='log-explorer'),
    path('insights/', AIInsightView.as_view(), name='ai-insights'),
]
