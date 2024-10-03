import logging
import asyncio
import os
from datetime import datetime, timezone
from stargaze_client import StargazeClient
from discord_client import DiscordClient, create_discord_embed
from constants import TIMESTAMP_FILE, PAGINATION_LIMIT, CHECK_FREQUENCY_SECONDS, COLLECTION_ADDRESS

async def load_query_file(file_path: str) -> str:
    """Load the content of a GraphQL file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"GraphQL file not found: {file_path}")
        return ""


async def main():
    await asyncio.create_task(process_event_loop())

async def process_event_loop():
    stargaze_client = StargazeClient()
    discord_client = DiscordClient()
    activity_query_content = await load_query_file('graphql/token_sales_query.graphql')
    stargaze_query = f"""{activity_query_content}"""

    while True:
        try:
            if not os.path.isfile(TIMESTAMP_FILE):
                # If it doesn't exist, create a new one with the current UTC timestamp
                last_time_stamp = datetime.now(timezone.utc)
                with open(TIMESTAMP_FILE, 'w') as file:
                    file.write(str(last_time_stamp))
            else:
                with open(TIMESTAMP_FILE, 'r') as file:
                    timestamp_str = file.read()
                    last_time_stamp = datetime.fromisoformat(timestamp_str)
            logging.info(f"Searching for new sales.  Last sale was on: {timestamp_str}")

            # Define the query parameters and prepare the query
            if not COLLECTION_ADDRESS:
                logging.error(f"Please specify a collection address by using the environment variable: COLLECTION_ADDRESS")
                return

            pagination_limit = PAGINATION_LIMIT
            if pagination_limit < 1 or pagination_limit > 50:
                pagination_limit = 25

            params = {
                "filterByCollectionAddrs": [COLLECTION_ADDRESS],
                "sortBy": "SALE_TIME_ASC",
                "limit": pagination_limit,
                "filterByDateRange": {
                    "startDate": last_time_stamp.strftime("%Y-%m-%dT%H:%M:%S")
                },
            }

            # Run the query and process the results
            result = await stargaze_client.execute_query(stargaze_query, params)

            if result:
                activities = result.get('tokenSales', {}).get('tokenSales', {})
                for activity in activities:
                    activity_date = activity.get('date', 0)
                    activity_timestamp = datetime.strptime(activity_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                    activity_timestamp = activity_timestamp.replace(tzinfo=timezone.utc)
                    if activity_timestamp > last_time_stamp:
                        with open(TIMESTAMP_FILE, 'w') as file:
                            last_time_stamp = activity_timestamp
                            file.write(str(last_time_stamp))

                        # Send a discord notification for each activity
                        activity_embed = await create_discord_embed(activity)
                        await discord_client.send_message(activity_embed)
        except Exception as e:
            logging.error(f"Error checking activities: {e}")
            pass

        # Sleep before checking again for sales
        await asyncio.sleep(CHECK_FREQUENCY_SECONDS)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
