import subprocess
import time
import json
import pyperclip

MACBOOK_BARCODES = {
    ("13", 2020, "M1",     8): "i000000038431",
    ("13", 2020, "M1",    16): "i000000038434",
    ("14", 2021, "M1 Pro", 16): "i000000041694",
    ("13", 2022, "M2",     8): "i000000042410",
    ("13", 2022, "M2",    16): "i000000042415",
}


def get_musicmagpie_price(screen_size: str, year: int, chip: str, ram_gb: int) -> dict | None:
    """
    Get musicmagpie trade-in prices for a MacBook.
    Returns None if the model isn't in our list or the request fails,
    so callers can handle it gracefully without crashing.
    """
    # Normalise inputs to match our keys
    size = screen_size.replace('"', '').replace("'", "").strip()
    chip_clean = chip.upper().replace("APPLE ", "").strip()
    # Map chip strings to our key format
    chip_map = {
        "M1": "M1", "M1 PRO": "M1 Pro", "M1 MAX": "M1 Max",
        "M2": "M2", "M2 PRO": "M2 Pro", "M2 MAX": "M2 Max",
        "M3": "M3", "M3 PRO": "M3 Pro", "M3 MAX": "M3 Max",
    }
    chip_key = chip_map.get(chip_clean)
    if not chip_key:
        return None

    try:
        ram = int(str(ram_gb).replace("GB", "").replace("gb", "").strip())
        year = int(year)
    except (ValueError, TypeError):
        return None

    key = (size, year, chip_key, ram)
    barcode = MACBOOK_BARCODES.get(key)
    if not barcode:
        return None

    url = (
        "https://www.musicmagpie.co.uk/Umbraco/Surface/Products/GetProductPrices"
        f"?barcode={barcode}&networkId=-1&website=musicMagpie"
    )

    try:
        subprocess.run([
            "osascript",
            "-e", f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"',
        ], check=True)
        time.sleep(4)

        subprocess.run([
            "osascript",
            "-e", 'tell application "Google Chrome" to activate',
            "-e", 'tell application "System Events" to keystroke "a" using command down',
            "-e", 'tell application "System Events" to keystroke "c" using command down',
        ], check=True)
        time.sleep(0.5)

        data = json.loads(pyperclip.paste().strip())
        return {
            "good":   data.get("good"),
            "poor":   data.get("poor"),
            "faulty": data.get("faulty"),
        }
    except Exception as e:
        print(f"[MusicMagpie] Failed to fetch price: {e}")
        return None