import requests


class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_listing(self, listing, category):
        specs = listing.specs

        embed = {
            "title": listing.title[:256],
            "url": listing.url,
            "description": (
                f"**Category:** {category.name}\n"
                f"**Price:** £{listing.price}\n"
                f"**Max Price:** £{category.max_price}\n\n"
                f"**CPU:** {specs['cpu']}\n"
                f"**RAM:** {specs['ram']}\n"
                f"**Storage:** {specs['storage']}\n"
                f"**Year:** {specs['year']}\n"
                f"**Size:** {specs['screen_size']}"
            ),
            "color": 5814783,
            "footer": {
                "text": "eBay MacBook Tracker"
            },
        }

        if listing.image_url:
            embed["thumbnail"] = {
                "url": listing.image_url
            }

        payload = {
            "content": f"🚨 New {category.name} listing found!",
            "embeds": [embed],
        }

        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()