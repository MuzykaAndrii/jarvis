import logging

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import cartesia, deepgram, silero, google

from app.loggers import log_collected_metrics
from app.validator import services
from app import prompts


logger = logging.getLogger("voice-agent")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=google.LLM(model="gemini-2.0-pro-exp-02-05"),
        tts=cartesia.TTS(),
        min_endpointing_delay=1.5,
        max_endpointing_delay=5.0,
        before_tts_cb=services.validate_llm_output_length,
        chat_ctx=llm.ChatContext().append(
            role="system",
            text=prompts.INITIAL_CONTEXT,
        ),
    )

    agent.on("metrics_collected", log_collected_metrics)
    agent.start(ctx.room, participant)
    await agent.say(prompts.GREET_MSG, allow_interruptions=True)
