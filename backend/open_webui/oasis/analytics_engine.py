import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict

log = logging.getLogger(__name__)

class AnalyticsEngine:
    """Real-time analytics and metrics tracking"""
    
    def __init__(self):
        self.metrics = defaultdict(lambda: defaultdict(int))
        self.events = []
        
    def track_event(self, event_type: str, user_id: str, metadata: Dict = None):
        """Track user event"""
        event = {
            "type": event_type,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.events.append(event)
        self.metrics[event_type]["count"] += 1
        
    def track_model_usage(self, model: str, tokens: int, cost: float, user_id: str):
        """Track model usage and costs"""
        self.metrics["models"][model] += tokens
        self.metrics["costs"][user_id] += cost
        self.metrics["tokens"]["total"] += tokens
        
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        return {
            "total_events": len(self.events),
            "total_tokens": self.metrics["tokens"]["total"],
            "total_cost": sum(self.metrics["costs"].values()),
            "active_users": len(set(e["user_id"] for e in self.events)),
            "top_models": dict(sorted(self.metrics["models"].items(), key=lambda x: x[1], reverse=True)[:5]),
            "event_breakdown": dict(self.metrics)
        }
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user-specific statistics"""
        user_events = [e for e in self.events if e["user_id"] == user_id]
        return {
            "total_events": len(user_events),
            "total_cost": self.metrics["costs"][user_id],
            "recent_activity": user_events[-10:]
        }
    
    def export_report(self, format: str = "json") -> str:
        """Export analytics report"""
        stats = self.get_dashboard_stats()
        if format == "json":
            import json
            return json.dumps(stats, indent=2)
        return str(stats)

analytics_engine = AnalyticsEngine()
