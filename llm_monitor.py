import time

class LLMMonitor:
    def __init__(self):
        self.requests = 0
        self.total_latency = 0
        self.token_usage = 0

    def _estimate_tokens(self, text):
        if not text:
            return 0
        return len(text.split())

    def start_request(self):
        self.start_time = time.time()
        self.requests += 1

    def end_request(self, prompt="", completion=""):
        latency = int((time.time() - self.start_time) * 1000)
        self.total_latency += latency

        self.token_usage += (
            self._estimate_tokens(prompt) +
            self._estimate_tokens(completion)
        )

    def generate_metrics(self):
        avg_latency = self.total_latency / self.requests if self.requests else 0

        return {
            "requests": self.requests,
            "avg_latency": int(avg_latency),
            "token_usage": self.token_usage
        }


# -------------------------
# RUN ONLY WHEN EXECUTED
# -------------------------
if __name__ == "__main__":

    monitor = LLMMonitor()

    # Request 1
    monitor.start_request()
    time.sleep(1)
    monitor.end_request(
        prompt="What is AI?",
        completion="AI is Artificial Intelligence"
    )

    # Request 2
    monitor.start_request()
    time.sleep(0.5)
    monitor.end_request(
        prompt="Explain ML",
        completion="ML is a subset of AI"
    )

    # FINAL OUTPUT
    result = monitor.generate_metrics()
    print(result)