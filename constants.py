import os

# Required parameters
COLLECTION_ADDRESS = os.getenv('COLLECTION_ADDRESS')
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

# Optional parameters
STARGAZE_API_HOST = os.getenv('STARGAZE_API_HOST', 'https://graphql.mainnet.stargaze-apis.com/graphql')
STARGAZE_ICON_URL = os.getenv('STARGAZE_ICON_URL',
                              'https://pbs.twimg.com/profile_images/1507391623914737669/U3fR7nxh_400x400.jpg')
STARGAZE_NFT_URL = os.getenv('STARGAZE_NFT_URL', 'https://www.stargaze.zone/m/{collection_address}/{token_id}')
PAGINATION_LIMIT = int(os.getenv('PAGINATION_LIMIT', 25))
DISCORD_EMBED_COLOR = int(os.getenv('DISCORD_EMBED_COLOR', 0xe170a4))
COLLECTION_ACTIVITY = os.getenv('COLLECTION_ACTIVITY', 'SALE')
