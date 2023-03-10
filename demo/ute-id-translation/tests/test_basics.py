from pprint import pprint

import pandas as pd

from ute import id_translation

DATA = pd.DataFrame({"category_id": [1, 2], "country_id": [1, 2], "customer_id": [1, 2]})
EXPECTED = pd.DataFrame({
    "category_id": ["1:Action", "2:Animation"],
    "country_id": ["1:Afghanistan", "2:Algeria"],
    "customer_id": ["1:MARY", "2:PATRICIA"],
})


def test_show_placeholders():
    fetcher = id_translation.create_translator().fetcher
    print(f"\nColumns available to {fetcher}:")
    for source, placeholders in fetcher.placeholders.items():
        print(f"Table {source}: [{(', '.join(sorted(placeholders)))}]")


def test_translate():
    pd.testing.assert_frame_equal(EXPECTED, id_translation.translate(DATA))


def test_create_translator():
    translator = id_translation.create_translator()
    pd.testing.assert_frame_equal(EXPECTED, translator.translate(DATA))


def test_load_cached_translator(tmp_path):
    id_translation.config.CACHE_DIR = tmp_path
    translator = id_translation.load_cached_translator()
    pd.testing.assert_frame_equal(EXPECTED, translator.translate(DATA))
