"""
Represents a single eBay listing.

Converts raw API JSON into a Python object.
"""

from src.spec_parser import SpecParser


class Listing:
    """
    Stores listing information in a structured format.
    """

    def __init__(self, item):
        self.raw = item

        self.id = item.get("itemId")
        self.title = item.get("title", "N/A")
        self.url = item.get("itemWebUrl", "N/A")
        self.image_url = item.get("image", {}).get("imageUrl")

        price_data = item.get("price", {})
        self.price = float(price_data.get("value", 999999))
        self.currency = price_data.get("currency", "GBP")

        # Extract MacBook specs from title
        self.specs = SpecParser.parse(self.title)

    def title_lower(self):
        return self.title.lower()