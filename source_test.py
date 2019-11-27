import pytest
from nvidia_fetcher import NVidiaFetcher
from topachat import TopAchat


@pytest.mark.parametrize("fetcher_class", [NVidiaFetcher])
@pytest.mark.parametrize("source_class", [TopAchat])
def test_source(fetcher_class, source_class):
    fetcher = fetcher_class(':in_memory:')
    mapping = fetcher.get_source_product_urls()[source_class]

    source = source_class()
    deals = source.fetch_deals(mapping)
    assert len(deals)
