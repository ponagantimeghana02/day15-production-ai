import time
import random
import json
from datetime import datetime

class AIOpsDashboard:
    def __init__(self):
        # System metrics
        self.requests = 0
        self.total_latency = 0
        self.errors = 0
        self.active_users = set()

        # Cost tracking (simple simulated model)
        self.total_cost = 0.0

        # AI metrics
        self.retrieval_scores = []
        self.hallucination_count = 0
        self.agent_success = 0
        self.agent_total = 0

    # -------------------------
    # System tracking
    # -------------------------
    def log_request(self, user_id, latency_ms, error=False, cost=0.0):
        self.requests += 1
        self.total_latency += latency_ms
        self.total_cost += cost

        if error:
            self.errors += 1

        self.active_users.add(user_id)

    # -------------------------
    # AI metrics tracking
    # -------------------------
    def log_retrieval(self, score):
        # score: 0 to 1
        self.retrieval_scores.append(score)

    def log_hallucination(self, is_hallucinated):
        if is_hallucinated:
            self.hallucination_count += 1

    def log_agent_run(self, success=True):
        self.agent_total += 1
        if success:
            self.agent_success += 1

    # -------------------------
    # Metrics calculation
    # -------------------------
    def generate_report(self):
        avg_latency = self.total_latency / self.requests if self.requests else 0
        error_rate = self.errors / self.requests if self.requests else 0

        retrieval_quality = (
            sum(self.retrieval_scores) / len(self.retrieval_scores)
            if self.retrieval_scores else 0
        )

        hallucination_rate = (
            self.hallucination_count / self.requests
            if self.requests else 0
        )

        agent_success_rate = (
            self.agent_success / self.agent_total
            if self.agent_total else 0
        )

        report = {
            "system_metrics": {
                "requests": self.requests,
                "avg_latency_ms": round(avg_latency, 2),
                "error_rate": round(error_rate, 4),
                "cost": round(self.total_cost, 4),
                "active_users": len(self.active_users)
            },
            "ai_metrics": {
                "retrieval_quality": round(retrieval_quality, 4),
                "hallucination_rate": round(hallucination_rate, 4),
                "agent_success_rate": round(agent_success_rate, 4)
            }
        }

        return report

    # -------------------------
    # Export report
    # -------------------------
    def export_report(self, filename="ops_dashboard_report.json"):
        report = self.generate_report()

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return filename


# =========================
# TESTING BLOCK
# =========================
if __name__ == "__main__":

    dashboard = AIOpsDashboard()

    # Simulated requests
    dashboard.log_request("user1", latency_ms=1200, cost=0.02)
    dashboard.log_request("user2", latency_ms=800, cost=0.015)
    dashboard.log_request("user1", latency_ms=1500, cost=0.03, error=True)

    # AI metrics
    dashboard.log_retrieval(0.8)
    dashboard.log_retrieval(0.6)
    dashboard.log_retrieval(0.9)

    dashboard.log_hallucination(False)
    dashboard.log_hallucination(True)

    dashboard.log_agent_run(True)
    dashboard.log_agent_run(True)
    dashboard.log_agent_run(False)

    # Final report
    report = dashboard.generate_report()

    print("\n📊 AI OPS DASHBOARD REPORT")
    print(json.dumps(report, indent=2))

    file = dashboard.export_report()
    print("\n📁 Report saved as:", file)