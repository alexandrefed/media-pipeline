"""Check existing quality scores in database."""

import asyncio

from src.database.connection import get_database


async def check_quality_scores():
    db = get_database()
    await db.initialize()

    try:
        async with db.get_connection() as conn:
            # Check existing quality scores in sources
            result = await conn.fetch(
                "SELECT DISTINCT quality_score FROM sources ORDER BY quality_score"
            )
            print("Existing quality scores in sources:", [r["quality_score"] for r in result])

            # Check constraint definition
            constraint = await conn.fetch(
                """
                SELECT conname, pg_get_constraintdef(oid) as definition
                FROM pg_constraint
                WHERE conname LIKE '%quality_score%'
            """
            )

            for c in constraint:
                print(f"Constraint {c['conname']}: {c['definition']}")

    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(check_quality_scores())
