import discord
from discord import SyncWebhook
from datetime import datetime, timezone
from constants import DISCORD_EMBED_COLOR, STARGAZE_ICON_URL, STARGAZE_NFT_URL, COLLECTION_ADDRESS, DISCORD_WEBHOOK


async def create_discord_embed(activity: dict):
    token = activity.get('token', {})
    price = activity.get('price', {})
    name = token.get('name')
    rarity = token.get('rarityOrder')
    traits = token.get('traits', {})
    amount_micro = int(price.get('amount', 0))
    amount = amount_micro * 1e-6
    amount_usd = price.get('amountUsd')
    token_id = token.get('tokenId')
    thumbnail = token.get('media', {}).get('visualAssets', {}).get('md', {}).get('url')
    currency = price.get('symbol')
    nft_url = await get_token_url(COLLECTION_ADDRESS, token_id)

    embed = discord.Embed(title=name,
                          url=nft_url,
                          color=DISCORD_EMBED_COLOR)

    embed.set_author(name="Sold on Stargaze", icon_url=STARGAZE_ICON_URL)
    if rarity:
        embed.add_field(name="Rarity", value="```" + str(rarity) + "```", inline=True)
    formatted_value = "{:,}".format(int(amount))
    embed.add_field(name="Price", value="```" + formatted_value + " " + currency + "```", inline=True)
    embed.add_field(name="USD Price", value=f"```${round(amount_usd)} USD```", inline=True)

    # Handle optional attributes data
    text = ""
    sorted_attributes = sorted(traits, key=lambda x: x["name"])
    for attribute in sorted_attributes:
        if 'name' in attribute and 'value' in attribute:
            text = text + f"**⦁ {attribute['name']}:** {attribute['value']}\n"
    if len(text) > 0:
        embed.add_field(name="Traits", value=text, inline=False)

    embed.set_image(url=thumbnail)
    embed.timestamp = datetime.now(timezone.utc)
    embed.set_footer(text="@LibreBots",
                     icon_url="https://pbs.twimg.com/profile_images/1841774136009297920/rNoWg-9A_400x400.jpg")
    return embed


async def get_token_url(collection_address: str, token_id: str):
    nft_url = STARGAZE_NFT_URL.replace('{collection_address}', collection_address)
    nft_url = nft_url.replace('{token_id}', token_id)
    return nft_url


class DiscordClient:

    def __init__(self):
        self.webhook = SyncWebhook.from_url(DISCORD_WEBHOOK)

    async def send_message(self, embed):
        self.webhook.send(embed=embed)
