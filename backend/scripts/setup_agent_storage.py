"""Create LangGraph checkpoint tables as an explicit deployment step."""

import asyncio

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.core.config import settings


async def main() -> None:
    async with AsyncPostgresSaver.from_conn_string(
        settings.checkpoint_database_url
    ) as checkpointer:
        await checkpointer.setup()


if __name__ == "__main__":
    asyncio.run(main())
