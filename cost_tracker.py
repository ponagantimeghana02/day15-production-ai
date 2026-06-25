import datetime

class CostTracker:
    def __init__(self):
        self.llm_cost = 0.0
        self.embedding_cost = 0.0
        self.vector_cost = 0.0
        self.agent_cost = 0.0

    # ------------------------
    # Cost methods
    # ------------------------
    def add_llm_cost(self, tokens, cost_per_1k=0.002):
        self.llm_cost += (tokens / 1000) * cost_per_1k

    def add_embedding_cost(self, tokens, cost_per_1k=0.0001):
        self.embedding_cost += (tokens / 1000) * cost_per_1k

    def add_vector_search_cost(self, queries=1, cost_per_query=0.001):
        self.vector_cost += queries * cost_per_query

    def add_agent_cost(self, actions=1, cost_per_action=0.01):
        self.agent_cost += actions * cost_per_action

    # ------------------------
    # Report
    # ------------------------
    def generate_report(self):
        total = self.llm_cost + self.embedding_cost + self.vector_cost + self.agent_cost

        return {
            "llm_cost": round(self.llm_cost, 4),
            "embedding_cost": round(self.embedding_cost, 4),
            "vector_search_cost": round(self.vector_cost, 4),
            "agent_execution_cost": round(self.agent_cost, 4),
            "total_cost": round(total, 4)
        }

    # ------------------------
    # Markdown report
    # ------------------------
    def save_report(self, filename="daily_cost_report.md"):
        report = self.generate_report()
        date = datetime.date.today()

        content = f"""# 📊 Daily Cost Report ({date})

## 💰 Cost Breakdown

- LLM Cost: ${report['llm_cost']}
- Embedding Cost: ${report['embedding_cost']}
- Vector Search Cost: ${report['vector_search_cost']}
- Agent Execution Cost: ${report['agent_execution_cost']}

---

## 🧾 Total Cost

**${report['total_cost']}**

---

## 📈 Optimization Suggestions

- Reduce prompt length to save LLM cost
- Cache embeddings to avoid recomputation
- Batch vector DB queries
- Reduce unnecessary agent calls
- Use cheaper models for simple tasks
"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        return filename


# =========================
# TESTING BLOCK (IMPORTANT)
# =========================
if __name__ == "__main__":

    tracker = CostTracker()

    # Simulated usage
    tracker.add_llm_cost(tokens=5000)
    tracker.add_llm_cost(tokens=3000)

    tracker.add_embedding_cost(tokens=20000)

    tracker.add_vector_search_cost(queries=40)

    tracker.add_agent_cost(actions=15)

    # Print report
    report = tracker.generate_report()
    print("\n📊 COST REPORT:")
    print(report)

    # Save markdown file
    file = tracker.save_report()
    print("\n📁 Report saved as:", file)