import os
import logging
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from constants import STARGAZE_API_HOST


class StargazeClient:
    def __init__(self):
        api_url = os.getenv('STARGAZE_API_HOST', STARGAZE_API_HOST)
        self.transport = AIOHTTPTransport(url=api_url)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    async def execute_query(self, query: str, params: dict) -> dict:
        """Execute a GraphQL query and return the result."""
        try:
            result = await self.client.execute_async(gql(query), variable_values=params)
            return result
        except Exception as e:
            logging.error(f"An error occurred while running the query: {e}")
            return {}
