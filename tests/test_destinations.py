import pytest
from services.destination_service import DestinationService
from config.database import init_db


def test_destination_lookup_and_details():
    init_db()
    # Search for Araku Valley
    araku = DestinationService.get_by_name_or_discover("Araku Valley")
    assert araku is not None
    assert "araku" in araku["name"].lower()

    # Check details
    details = DestinationService.get_details(araku["id"])
    assert "attractions" in details
    assert "hotels" in details
    assert len(details["attractions"]) > 0


def test_custom_destination_fallback():
    # Searching for an arbitrary unknown village should never return None or crash
    unknown = DestinationService.get_by_name_or_discover("SolitudeHamlet999")
    assert unknown is not None
    assert "solitudehamlet999" in unknown["name"].lower()
