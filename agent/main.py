from livekit.agents import WorkerOptions, cli
from dotenv import load_dotenv

from app.agent import entrypoint, prewarm


load_dotenv(dotenv_path=".env.local")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
