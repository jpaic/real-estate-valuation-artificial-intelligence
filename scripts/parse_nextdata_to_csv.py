"""
Parser that converts SAVED search pages from nekretnine.rs into clean CSV data.

WHY THIS APPROACH (and not live scraping with the requests library)
--------------------------------------------------------------------
Nekretnine.rs uses Next.js server-side rendering OR DataDome anti-bot protection.
Two separate problems:

1. DataDome (window.ddjskey, datadome.co script on the page) blocks "bare" HTTP
   requests (requests/curl) with 403 before you even get HTML. This is NOT
   an IP/domain restriction — even from a real computer `requests.get(...)` gets
   a 403 from DataDome.
2. The page is server-side rendered (SSR) — the complete structured JSON for all
   listings on the page is already embedded in HTML in:

       <script id="__NEXT_DATA__" type="application/json"> ... </script>

   This is a BETTER data source than CSS classes (which are hashed, e.g.
   "Price_price__kHY5L", and change on every site build) — JSON has
   stable field names (price, rooms, surface, location.macrozone, etc.)

STRATEGY
--------
   This script ONLY parses already-saved .html files — it makes no network
   requests. It works completely offline on files in the input directory.

Usage
-----
    python parse_nextdata_to_csv.py --input-dir ../data/raw/nekretnine --out ../data/processed/nekretnine_listings.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("parse_nextdata_to_csv")

NEXT_DATA_PATTERN = re.compile(
    r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL
)

CSV_COLUMNS = [
    "listing_id",
    "url",
    "title",
    "contract",
    "is_new",
    "price_eur",
    "price_raw",
    "price_visible",
    "typology",
    "category",
    "area_sqm",
    "rooms",
    "bedrooms",
    "bathrooms",
    "floor",
    "elevator",
    "balcony",
    "terrace",
    "basement",
    "furnished",
    "heating",
    "municipality",
    "neighborhood",
    "city",
    "address",
    "latitude",
    "longitude",
    "agency",
    "description",
    "source_file",
]


@dataclass
class Listing:
    listing_id: str = ""
    url: str = ""
    title: str = ""
    contract: str = ""
    is_new: Optional[bool] = None
    price_eur: Optional[float] = None
    price_raw: str = ""
    price_visible: Optional[bool] = None
    typology: str = ""
    category: str = ""
    area_sqm: Optional[float] = None
    rooms: str = ""
    bedrooms: str = ""
    bathrooms: str = ""
    floor: str = ""
    elevator: Optional[bool] = None
    balcony: Optional[bool] = None
    terrace: Optional[bool] = None
    basement: Optional[bool] = None
    furnished: Optional[bool] = None
    heating: str = ""
    municipality: str = ""
    neighborhood: str = ""
    city: str = ""
    address: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    agency: str = ""
    description: str = ""
    source_file: str = ""


def _surface_to_float(surface: str) -> Optional[float]:
    """'268 m²' -> 268.0"""
    if not surface:
        return None
    m = re.search(r"([\d.,]+)", surface)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", "."))
    except ValueError:
        return None


def _feature_present(feature_list: list, feature_type: str) -> Optional[bool]:
    """Returns True if feature_type is present in featureList, otherwise None
    (not False, because absence from this list does not guarantee that the
    property DOESN'T have that feature — only that the site didn't highlight it)."""
    if not feature_list:
        return None
    present = any(f.get("type") == feature_type for f in feature_list)
    return True if present else None


def extract_next_data(html: str) -> Optional[dict]:
    match = NEXT_DATA_PATTERN.search(html)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        log.warning("Cannot parse __NEXT_DATA__ JSON: %s", exc)
        return None


def find_results_list(next_data: dict) -> list:
    """Next.js dehydrates react-query caches into queries[]; we look for the one
    containing search results (has 'results' key in state.data)."""
    try:
        queries = next_data["props"]["pageProps"]["dehydratedState"]["queries"]
    except (KeyError, TypeError):
        return []

    for query in queries:
        try:
            data = query["state"]["data"]
        except (KeyError, TypeError):
            continue
        if isinstance(data, dict) and "results" in data:
            return data["results"]
    return []


def parse_result_item(item: dict, source_file: str) -> Optional[Listing]:
    real_estate = item.get("realEstate", {})
    seo = item.get("seo", {})
    properties = real_estate.get("properties") or [{}]
    prop = properties[0]

    price = real_estate.get("price", {})
    location = prop.get("location", {})
    feature_list = prop.get("featureList", [])
    agency = (
        real_estate.get("advertiser", {}).get("agency", {}).get("displayName", "")
    )

    listing = Listing(
        listing_id=str(real_estate.get("id", "")),
        url=seo.get("url", ""),
        title=seo.get("anchor") or real_estate.get("title", ""),
        contract=real_estate.get("contract", ""),
        is_new=real_estate.get("isNew"),
        price_eur=price.get("value"),
        price_raw=price.get("formattedValue", ""),
        price_visible=price.get("visible"),
        typology=(prop.get("typology") or {}).get("name", ""),
        category=(prop.get("category") or {}).get("name", ""),
        area_sqm=_surface_to_float(prop.get("surface", "")),
        rooms=prop.get("rooms", ""),
        bedrooms=prop.get("bedRoomsNumber", ""),
        bathrooms=prop.get("bathrooms", ""),
        floor=(prop.get("floor") or {}).get("floorOnlyValue", ""),
        elevator=prop.get("elevator") or _feature_present(feature_list, "elevator"),
        balcony=_feature_present(feature_list, "balcony"),
        terrace=_feature_present(feature_list, "terrace"),
        basement=_feature_present(feature_list, "basement"),
        furnished=_feature_present(feature_list, "furniture"),
        heating=prop.get("ga4Heating", ""),
        municipality=location.get("macrozone", ""),
        neighborhood=location.get("microzone", ""),
        city=location.get("city", ""),
        address=location.get("address", ""),
        latitude=location.get("latitude"),
        longitude=location.get("longitude"),
        agency=agency,
        description=(prop.get("description", "") or "")[:500],
        source_file=source_file,
    )

    if not listing.listing_id:
        return None
    return listing


def parse_html_file(path: Path) -> list[Listing]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    next_data = extract_next_data(html)
    if next_data is None:
        log.warning("No __NEXT_DATA__ in %s — skipping.", path.name)
        return []

    results = find_results_list(next_data)
    if not results:
        log.warning("No 'results' list in __NEXT_DATA__ for %s.", path.name)
        return []

    listings = []
    for item in results:
        listing = parse_result_item(item, source_file=path.name)
        if listing:
            listings.append(listing)
    log.info("%s: %s listings parsed.", path.name, len(listings))
    return listings


def run(input_dir: str, out_path: str) -> Path:
    in_dir = Path(input_dir)
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    html_files = sorted(in_dir.glob("*.html")) + sorted(in_dir.glob("*.htm"))
    if not html_files:
        raise FileNotFoundError(
            f"No .html files in {in_dir}. Save search pages there first "
            "(see instructions at the top of this file)."
        )

    log.info("Found %s HTML files to process.", len(html_files))

    all_listings: list[Listing] = []
    seen_ids = set()
    for html_file in html_files:
        for listing in parse_html_file(html_file):
            if listing.listing_id in seen_ids:
                continue  # dedupe - the same property may appear on multiple pages
            seen_ids.add(listing.listing_id)
            all_listings.append(listing)

    with out_file.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for listing in all_listings:
            writer.writerow(asdict(listing))

    log.info("Done. %s unique listings saved to %s", len(all_listings), out_file.resolve())
    return out_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Parses saved nekretnine.rs HTML pages into CSV")
    parser.add_argument("--input-dir", default="../data/raw/nekretnine", help="Directory with saved .html pages")
    parser.add_argument("--out", default="../data/processed/nekretnine_listings.csv", help="Output CSV path")
    args = parser.parse_args()
    run(args.input_dir, args.out)


if __name__ == "__main__":
    main()
