from src.config import Config
from src.ebay_client import EbayClient
from src.discord_notifier import DiscordNotifier
from src.seen_items_manager import SeenItemsManager
from src.tracker import EbayTracker


def main():
    config = Config()

    ebay_client = EbayClient(
        credentials=config.ebay_credentials,
    )

    notifier = DiscordNotifier(
        macbook_webhook_url=config.discord_macbook_webhook_url,
        macbook_auction_webhook_url=config.discord_macbook_auction_webhook_url,
        ps5_webhook_url=config.discord_ps5_webhook_url,
        ps5_auction_webhook_url=config.discord_ps5_auction_webhook_url,
    )

    seen_items_manager = SeenItemsManager(
        file_path=config.seen_file,
    )

    tracker = EbayTracker(
        ebay_client=ebay_client,
        notifier=notifier,
        seen_items_manager=seen_items_manager,
        search_categories=config.search_categories,
        check_every_seconds=config.check_every_seconds,
    )

    tracker.run()


if __name__ == "__main__":
    main()