from observability import Observability, trace_function

obs = Observability("AI_API_Service")


@trace_function(obs)
def sample_tool(x, y):
    return x + y


# Simulate API flow
obs.log_request("/chat", "POST", user_id="123")
obs.log_query("123", "What is AI?")
obs.log_tool_call("search_tool", {"query": "AI agents"})
obs.log_agent_action("PlannerAgent", "created_plan")

result = sample_tool(10, 20)

print("Tool Result:", result)
print("Done. Check /logs folder.")