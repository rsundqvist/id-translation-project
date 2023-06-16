import pandas as pd
from id_translation.mapping.support import enable_verbose_debug_messages

from big_corporation_inc import id_translation


DATA = pd.DataFrame(
    {
        "category_id": [1, 2],
        "country_id": [1, 2],
        "customer_id": [1, 2],
        # Should not be translated!
        "session_id": [123113, 3213213],
        "date": [pd.Timestamp("2019-05-11"), pd.Timestamp("2019-05-11")],
    }
)

EXPECTED = pd.DataFrame(
    {
        "category_id": ["1:Action", "2:Animation"],
        "country_id": ["1:Afghanistan", "2:Algeria"],
        "customer_id": ["1:MARY", "2:PATRICIA"],
        # Should not be translated!
        "session_id": [123113, 3213213],
        "date": [pd.Timestamp("2019-05-11"), pd.Timestamp("2019-05-11")],
    }
)


def test_show_placeholders():
    fetcher = id_translation.create_translator().fetcher
    print(f"\nColumns available to {fetcher}:")
    for source, placeholders in fetcher.placeholders.items():
        print(f"Table {source}: [{(', '.join(sorted(placeholders)))}]")


def test_translate():
    with enable_verbose_debug_messages():
        # Use verbose logging here, to make debugging mapping issues easier.
        actual = id_translation.translate(DATA)
    pd.testing.assert_frame_equal(EXPECTED, actual)


def test_create_translator():
    translator = id_translation.create_translator()
    actual = translator.translate(DATA)
    pd.testing.assert_frame_equal(EXPECTED, actual)


def test_load_cached_translator(tmp_path):
    id_translation.config.CACHE_DIR = tmp_path
    translator = id_translation.load_cached_translator()
    actual = translator.translate(DATA)
    pd.testing.assert_frame_equal(EXPECTED, actual)


def test_override_only(monkeypatch):
    """Contains all configuration which is not specific to a single fetcher."""
    from big_corporation_inc.id_translation import config

    onverride_only = config._config_root / "fetching/inactive/override-only.toml"
    monkeypatch.setattr(config, "FETCHING_CONFIGURATION_PATHS", [onverride_only])
    translator = id_translation.create_translator()
    assert translator.fetcher.mapper._score.__name__ == "disabled"
    actual = translator.translate(DATA)
    pd.testing.assert_frame_equal(EXPECTED, actual)
