"""
Extracts MacBook specs from eBay listing titles.

The eBay API does not always provide clean structured specs,
so this parser uses the listing title as the main source.
"""

import re


class SpecParser:
    """
    Parses useful MacBook details from a listing title.
    """

    @staticmethod
    def parse(title):
        """
        Returns a dictionary of extracted specs.
        """

        title_lower = title.lower()

        return {
            "screen_size": SpecParser.extract_screen_size(title_lower),
            "cpu": SpecParser.extract_cpu(title_lower),
            "ram": SpecParser.extract_ram(title_lower),
            "storage": SpecParser.extract_storage(title_lower),
            "year": SpecParser.extract_year(title_lower),
        }

    @staticmethod
    def extract_screen_size(title):
        match = re.search(r"(13|13\.3|14|14\.2|15|16|16\.2)[\s-]?(inch|in|\"|'')?", title)

        if match:
            return match.group(1) + '"'

        return "Unknown"

    @staticmethod
    def extract_cpu(title):
        cpu_patterns = [
            "m3 max",
            "m3 pro",
            "m3",
            "m2 max",
            "m2 pro",
            "m2",
            "m1 max",
            "m1 pro",
            "m1",
            "intel i9",
            "intel i7",
            "intel i5",
            "i9",
            "i7",
            "i5",
        ]

        for cpu in cpu_patterns:
            if cpu in title:
                return cpu.upper()

        return "Unknown"

    @staticmethod
    def extract_ram(title):
        match = re.search(r"(\d+)\s?(gb)\s?(ram|memory)?", title)

        if match:
            return match.group(1) + "GB"

        return "Unknown"

    @staticmethod
    def extract_storage(title):
        match = re.search(r"(\d+)\s?(tb|gb)\s?(ssd|storage)?", title)

        if match:
            size = match.group(1)
            unit = match.group(2).upper()

            # Avoid confusing RAM as storage
            if "ram" not in match.group(0):
                return size + unit

        return "Unknown"

    @staticmethod
    def extract_year(title):
        """
        Extract year from title.
        If no year is present, infer it from CPU.
        """

        # Explicit year in title
        match = re.search(
            r"(2016|2017|2018|2019|2020|2021|2022|2023|2024|2025)",
            title
        )

        if match:
            return match.group(1)

        # CPU-based inference
        if "m1 pro" in title:
            return "2021"

        if "m1 max" in title:
            return "2021"

        if "m1" in title:
            return "2020"

        if "m2 pro" in title:
            return "2023"

        if "m2 max" in title:
            return "2023"

        if "m2" in title:
            return "2022"

        if "m3 pro" in title:
            return "2023"

        if "m3 max" in title:
            return "2023"

        if "m3" in title:
            return "2023"

        # Intel generation estimates
        if "i9" in title:
            return "2019-2020"

        if "i7" in title:
            return "2016-2020"

        if "i5" in title:
            return "2013-2020"

        return "Unknown"