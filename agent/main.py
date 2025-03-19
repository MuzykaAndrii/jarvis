from livekit.agents import WorkerOptions, cli

from app.agent import entrypoint, prewarm


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
