from livekit.agents import metrics


def log_collected_metrics(agent_metrics: metrics.AgentMetrics):
    usage_collector = metrics.UsageCollector()
    metrics.log_metrics(agent_metrics)
    usage_collector.collect(agent_metrics)
