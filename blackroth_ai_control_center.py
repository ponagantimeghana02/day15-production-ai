import time
import json
import random
from datetime import datetime


class BlackRothAIControlCenter:
    def __init__(self):
        # -----------------------
        # Monitoring Data
        # -----------------------
        self.ai_requests = 0
        self.rag_searches = 0
        self.agent_activity = 0
        self.total_cost = 0.0
        self.errors = 0

        # system health
        self.services = {
            "api_gateway": "healthy",
            "rag_service": "healthy",
            "agent_service": "healthy",
            "auth_service": "healthy"
        }

        # -----------------------
        # Admin Data
        # -----------------------
        self.users = {}
        self.roles = {}
        self.audit_logs = []

        # -----------------------
        # Ops Data
        # -----------------------
        self.deployments = {}
        self.incidents = []
        self.alerts = []

        # -----------------------
        # Analytics
        # -----------------------
        self.latencies = []
        self.cost_history = []

    # =========================================================
    # MONITORING
    # =========================================================

    def log_ai_request(self, latency_ms, cost=0.0, error=False):
        self.ai_requests += 1
        self.total_cost += cost
        self.latencies.append(latency_ms)

        if error:
            self.errors += 1

        self._check_alerts(latency_ms, cost, error)

    def log_rag_search(self, score):
        self.rag_searches += 1

    def log_agent_activity(self):
        self.agent_activity += 1

    # =========================================================
    # ADMIN MODULE
    # =========================================================

    def create_user(self, user_id, role):
        self.users[user_id] = role
        self._audit("USER_CREATED", f"{user_id} as {role}")

    def create_role(self, role_name, permissions):
        self.roles[role_name] = permissions
        self._audit("ROLE_CREATED", role_name)

    def _audit(self, action, details):
        self.audit_logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "details": details
        })

    # =========================================================
    # OPERATIONS
    # =========================================================

    def deploy_service(self, service_name, version):
        self.deployments[service_name] = {
            "version": version,
            "status": "deployed",
            "time": datetime.utcnow().isoformat()
        }

    def update_service_health(self, service_name, status):
        self.services[service_name] = status

    def _check_alerts(self, latency_ms, cost, error):
        if latency_ms > 2000:
            self._create_alert("HIGH_LATENCY", f"Latency: {latency_ms}ms")

        if cost > 1.0:
            self._create_alert("HIGH_COST", f"Cost spike: {cost}")

        if error:
            self._create_alert("ERROR_RATE", "Error detected in request")

    def _create_alert(self, alert_type, message):
        alert = {
            "type": alert_type,
            "message": message,
            "time": datetime.utcnow().isoformat()
        }
        self.alerts.append(alert)

    def create_incident(self, title, severity):
        self.incidents.append({
            "title": title,
            "severity": severity,
            "time": datetime.utcnow().isoformat()
        })

    # =========================================================
    # ANALYTICS
    # =========================================================

    def get_usage_analytics(self):
        return {
            "ai_requests": self.ai_requests,
            "rag_searches": self.rag_searches,
            "agent_activity": self.agent_activity
        }

    def get_cost_analytics(self):
        return {
            "total_cost": round(self.total_cost, 4),
            "avg_cost_per_request": round(
                self.total_cost / self.ai_requests if self.ai_requests else 0, 4
            )
        }

    def get_performance_analytics(self):
        avg_latency = (
            sum(self.latencies) / len(self.latencies)
            if self.latencies else 0
        )

        return {
            "avg_latency_ms": round(avg_latency, 2),
            "error_rate": round(
                self.errors / self.ai_requests if self.ai_requests else 0, 4
            )
        }

    # =========================================================
    # SYSTEM HEALTH
    # =========================================================

    def get_system_health(self):
        return {
            "services": self.services,
            "status": "degraded" if "unhealthy" in self.services.values() else "healthy"
        }

    # =========================================================
    # FULL DASHBOARD
    # =========================================================

    def get_dashboard(self):
        return {
            "monitoring": {
                "ai_requests": self.ai_requests,
                "rag_searches": self.rag_searches,
                "agent_activity": self.agent_activity,
                "total_cost": round(self.total_cost, 4)
            },
            "administration": {
                "users": len(self.users),
                "roles": len(self.roles),
                "audit_logs": len(self.audit_logs)
            },
            "operations": {
                "deployments": len(self.deployments),
                "alerts": len(self.alerts),
                "incidents": len(self.incidents)
            },
            "analytics": {
                "usage": self.get_usage_analytics(),
                "cost": self.get_cost_analytics(),
                "performance": self.get_performance_analytics()
            },
            "system_health": self.get_system_health()
        }

    # =========================================================
    # EXPORT
    # =========================================================

    def export_report(self, filename="blackroth_control_center_report.json"):
        data = self.get_dashboard()

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return filename


# =========================================================
# TESTING
# =========================================================
if __name__ == "__main__":

    center = BlackRothAIControlCenter()

    # ---------------- Monitoring
    center.log_ai_request(1200, cost=0.2)
    center.log_ai_request(2500, cost=1.5, error=True)
    center.log_rag_search(0.8)
    center.log_agent_activity()

    # ---------------- Admin
    center.create_user("user1", "admin")
    center.create_role("admin", ["all_access"])

    # ---------------- Ops
    center.deploy_service("rag_service", "v1.2")
    center.update_service_health("rag_service", "healthy")

    center.create_incident("RAG slowdown", "medium")

    # ---------------- Dashboard
    dashboard = center.get_dashboard()
    print("\n📊 BLACKROTH AI CONTROL CENTER DASHBOARD\n")
    print(json.dumps(dashboard, indent=2))

    # Export
    file = center.export_report()
    print("\n📁 Report saved:", file)