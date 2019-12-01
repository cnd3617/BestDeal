# coding: utf-8

import pytest
from nvidia_fetcher import NVidiaFetcher
from topachat import TopAchat


@pytest.mark.parametrize("fetcher_class", [NVidiaFetcher])
@pytest.mark.parametrize("source_class", [TopAchat])
def test_source(fetcher_class, source_class):
    """
    Smoke test
    """
    fetcher = fetcher_class(database=None)
    fetcher._scrap_and_store()
