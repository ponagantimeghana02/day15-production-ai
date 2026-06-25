import time
import json
from datetime import datetime

class AlertingSystem:
    def __init__(self):
        self.incidents = []

        # Thresholds
        self.error_threshold = 0.3
        self.cost_threshold = 1.0
        self.latency_threshold = 2000  # ms
        self.retrieval_threshold = 0.5

        # Metrics store
        self.metrics = {
            "requests": 0,
            "errors": 0,
            "cost": 0.0,
            "latency_sum": 0,
            "retrieval_failures": 0
        }

    # -------------------------
    # Metric ingestion
    # -------------------------
    def log_request(self, latency_ms, error=False, cost=0.0):
        self.metrics["requests"] += 1
        self.metrics["cost"] += cost
        self.metrics["latency_sum"] += latency_ms

        if error:
            self.metrics["errors"] += 1

        self._evaluate_alerts(latency_ms, cost, error)

    def log_retrieval(self, score):
        if score < self.retrieval_threshold:
            self.metrics["retrieval_failures"] += 1
            self._send_alert(
                "Failed Retrieval",
                f"Low retrieval score detected: {score}"
            )

    # -------------------------
    # Alert evaluation
    # -------------------------
    def _evaluate_alerts(self, latency_ms, cost, error):
        error_rate = (
            self.metrics["errors"] / self.metrics["requests"]
            if self.metrics["requests"] else 0
        )

        avg_latency = (
            self.metrics["latency_sum"] / self.metrics["requests"]
            if self.metrics["requests"] else 0
        )

        # High error rate
        if error_rate > self.error_threshold:
            self._send_alert(
                "High Error Rate",
                f"Error rate is {error_rate:.2f}"
            )

        # High cost
        if self.metrics["cost"] > self.cost_threshold:
            self._send_alert(
                "High Cost",
                f"Total cost exceeded: {self.metrics['cost']:.2f}"
            )

        # Slow response
        if latency_ms > self.latency_threshold:
            self._send_alert(
                "Slow Response Time",
                f"Latency too high: {latency_ms} ms"
            )

        # Service downtime (simple simulation)
        if error:
            self._send_alert(
                "Service Downtime",
                "Request failed / service error detected"
            )

    # -------------------------
    # Alert sender (mock)
    # -------------------------
    def _send_alert(self, alert_type, message):
        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": alert_type,
            "message": message
        }

        self.incidents.append(alert)

        # Mock notifications
        self._send_email(alert)
        self._send_slack(alert)
        self._send_teams(alert)

    def _send_email(self, alert):
        print(f"[EMAIL ALERT] {alert['type']} -> {alert['message']}")

    def _send_slack(self, alert):
        print(f"[SLACK ALERT] {alert['type']} -> {alert['message']}")

    def _send_teams(self, alert):
        print(f"[TEAMS ALERT] {alert['type']} -> {alert['message']}")

    # -------------------------
    # Incident report
    # -------------------------
    def generate_report(self, filename="incident_report.md"):
        report = f"# 🚨 Incident Report\n\n"
        report += f"Generated: {datetime.utcnow().isoformat()}\n\n"

        if not self.incidents:
            report += "No incidents detected.\n"
        else:
            for i, inc in enumerate(self.incidents, 1):
                report += f"## Incident {i}\n"
                report += f"- Type: {inc['type']}\n"
                report += f"- Message: {inc['message']}\n"
                report += f"- Time: {inc['timestamp']}\n\n"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        return filename


# =========================
# TESTING BLOCK
# =========================
if __name__ == "__main__":

    system = AlertingSystem()

    # Normal request
    system.log_request(latency_ms=500, cost=0.2)

    # Slow request
    system.log_request(latency_ms=2500, cost=0.3)

    # Error request
    system.log_request(latency_ms=800, cost=0.4, error=True)

    # High cost trigger
    system.log_request(latency_ms=600, cost=1.2)

    # Retrieval failure
    system.log_retrieval(0.3)

    # Generate report
    file = system.generate_report()

    print("\n📁 Incident report saved:", file)