import logging

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    llm,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent

# from livekit.plugins import cartesia, deepgram, silero, turn_detector, google
from livekit.plugins import cartesia, deepgram, silero, google

from agent.app.validator import services
from app import prompts


logger = logging.getLogger("voice-agent")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=prompts.INITIAL_CONTEXT,
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=google.LLM(model="gemini-2.0-pro-exp-02-05"),
        tts=cartesia.TTS(),
        # turn_detector=turn_detector.EOUModel(),
        min_endpointing_delay=1.5,
        max_endpointing_delay=5.0,
        chat_ctx=initial_ctx,
        before_tts_cb=services.validate_llm_output_length,
    )

    usage_collector = metrics.UsageCollector()

    @agent.on("metrics_collected")
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
        metrics.log_metrics(agent_metrics)
        usage_collector.collect(agent_metrics)

    agent.start(ctx.room, participant)

    await agent.say(prompts.GREET_MSG, allow_interruptions=True)
