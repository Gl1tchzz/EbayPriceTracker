import requests
from src.musicmagpie_macbook import get_musicmagpie_price


class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_listing(self, listing, category):
        specs = listing.specs

        description = (
            f"**Category:** {category.name}\n"
            f"**eBay Price:** £{listing.price}\n"
            f"**Max Price:** £{category.max_price}\n\n"
            f"**CPU:** {specs['cpu']}\n"
            f"**RAM:** {specs['ram']}\n"
            f"**Storage:** {specs['storage']}\n"
            f"**Year:** {specs['year']}\n"
            f"**Size:** {specs['screen_size']}"
        )

        mm_prices = None
        poor_is_profitable = False

        try:
            ram_int = int(specs['ram'].replace("GB", "").strip())
            year_int = int(specs['year'])
            size_str = specs['screen_size'].replace('"', '').strip()
            chip_str = specs['cpu']

            mm_prices = get_musicmagpie_price(size_str, year_int, chip_str, ram_int)
        except Exception as e:
            print(f"[DiscordNotifier] Could not get resell price: {e}")

        if mm_prices:
            good   = mm_prices.get("good")
            poor   = mm_prices.get("poor")
            faulty = mm_prices.get("faulty")

            profit_good   = round(good   - listing.price, 2) if good   else None
            profit_poor   = round(poor   - listing.price, 2) if poor   else None
            profit_faulty = round(faulty - listing.price, 2) if faulty else None

            # Check if poor condition trade-in is profitable
            if profit_poor is not None and profit_poor > 0:
                poor_is_profitable = True

            def fmt(val, profit):
                if val is None:
                    return "N/A"
                sign = "+" if profit >= 0 else ""
                return f"£{val} ({sign}£{profit})"

            description += (
                f"\n\n**💰 MusicMagpie Resell Prices:**\n"
                f"Good:   {fmt(good,   profit_good)}\n"
                f"Poor:   {fmt(poor,   profit_poor)}\n"
                f"Faulty: {fmt(faulty, profit_faulty)}"
            )
        else:
            description += "\n\n_Resell price unavailable for this model_"

        embed = {
            "title": listing.title[:256],
            "url": listing.url,
            "description": description,
            "color": 16711680 if poor_is_profitable else 5814783,  # red if profitable, blue otherwise
            "footer": {"text": "eBay MacBook Tracker"},
        }

        if listing.image_url:
            embed["thumbnail"] = {"url": listing.image_url}

        # Ping @everyone if poor condition trade-in is in profit
        content = f"🚨 New {category.name} listing found!"
        if poor_is_profitable:
            content = f"@everyone 🔥 PROFITABLE FLIP — Poor condition is in profit! | {category.name}"

        payload = {
            "content": content,
            "embeds": [embed],
        }

        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()