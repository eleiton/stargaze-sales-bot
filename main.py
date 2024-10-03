import logging
import asyncio
from collections import deque
from stargaze_client import StargazeClient
from discord_client import DiscordClient, create_discord_embed
from constants import PAGINATION_LIMIT, COLLECTION_ACTIVITY, COLLECTION_ADDRESS


async def load_query_file(file_path: str) -> str:
    """Load the content of a GraphQL file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"GraphQL file not found: {file_path}")
        return ""


async def main():
    stargaze_client = StargazeClient()
    discord_client = DiscordClient()
    activity_query_content = await load_query_file('graphql/activity_query.graphql')
    stargaze_query = f"""{activity_query_content}"""

    # Define the query parameters and prepare the query
    if not COLLECTION_ADDRESS:
        logging.error(f"Please specify a collection address by using the environment variable: COLLECTION_ADDRESS")
        return

    pagination_limit = PAGINATION_LIMIT
    if pagination_limit < 1 or pagination_limit > 50:
        pagination_limit = 25
    pagination = {
        "limit": pagination_limit
    }

    params = {
        "address": COLLECTION_ADDRESS,
        "filterByActivity": COLLECTION_ACTIVITY,
        "pagination": pagination
    }

    # Run the query and process the results
    result = await stargaze_client.execute_query(stargaze_query, params)

    if result:
        activities = result.get('collectionActivity', {}).get('collectionActivity', {})

        # Add all activities in a queue, to then show them in the right order
        activity_queue = deque()
        for activity in activities:
            activity_queue.append(await create_discord_embed(activity))

        # Send a discord notification for each activity
        while activity_queue:
            await discord_client.send_message(activity_queue.pop())


if __name__ == "__main__":
    asyncio.run(main())
