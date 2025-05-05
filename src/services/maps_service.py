"""
Google Maps helper service used by ZipCodeAgent.

Functions:
  • geocode_zip(zip_code)          -> (city, state, lat, lng)
  • find_hospitals(lat, lng, ...)  -> list[str]
  • lookup_zip(zip_code)           -> (city, state, hospitals)
All I/O is executed in a background thread so callers can `await`.
"""

from __future__ import annotations

import asyncio
import os
from functools import lru_cache
from typing import Any, List, Tuple

import googlemaps


# ---------------------------------------------------------------------------
# Client initialisation
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _gmaps_client() -> googlemaps.Client:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_MAPS_API_KEY not set in environment!")
    return googlemaps.Client(key=api_key)


def _run_sync(func, *args, **kwargs):
    """
    Helper to off‑load blocking googlemaps call into thread executor.
    """
    loop = asyncio.get_running_loop()
    return loop.run_in_executor(None, lambda: func(*args, **kwargs))


# ---------------------------------------------------------------------------
# Core look‑ups
# ---------------------------------------------------------------------------

async def geocode_zip(zip_code: str) -> Tuple[str | None, str | None, float | None, float | None]:
    """Return (city, state, lat, lng) or (None, None, None, None) on failure."""
    client = _gmaps_client()
    try:
        results: List[dict[str, Any]] = await _run_sync(client.geocode, zip_code)
    except Exception:
        return (None, None, None, None)

    if not results:
        return (None, None, None, None)

    addr = results[0]["address_components"]
    city = state = None
    for comp in addr:
        types = comp["types"]
        if "locality" in types:
            city = comp["long_name"]
        if "administrative_area_level_1" in types:
            state = comp["short_name"]

    loc = results[0]["geometry"]["location"]
    return (city, state, loc["lat"], loc["lng"])


async def find_hospitals(
    lat: float,
    lng: float,
    *,
    radius_m: int = 16093,
    max_results: int = 3,
) -> List[str]:
    """Return a list of hospital names (+ vicinity) near the coordinates."""
    client = _gmaps_client()
    try:
        resp: dict[str, Any] = await _run_sync(
            client.places_nearby,
            location=(lat, lng),
            radius=radius_m,
            type="hospital",
        )
    except Exception:
        return []

    hospitals = []
    for result in resp.get("results", [])[:max_results]:
        name = result.get("name")
        vicinity = result.get("vicinity", "")
        hospitals.append(f"{name} ({vicinity})")
    return hospitals


# ---------------------------------------------------------------------------
# High‑level convenience
# ---------------------------------------------------------------------------

async def lookup_zip(zip_code: str) -> Tuple[str | None, str | None, List[str]]:
    """
    Full pipeline → (city, state, [hospital list]).
    Returns (None, None, []) if lookup fails.
    """
    city, state, lat, lng = await geocode_zip(zip_code)
    if city is None or lat is None:
        return (None, None, [])
    hospitals = await find_hospitals(lat, lng)
    return (city, state, hospitals)
