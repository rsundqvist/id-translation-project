from pprint import pprint

from ute import id_translation


def test_fancy_format_string():
    translator = id_translation.create_translator().copy(fmt="{name} <{email!r}> {last_name}")
    print("\nSome more information about the first ten customers:")
    pprint(translator.translate(list(range(10)), names="customer_id"))


def test_untranslatable_ids():
    translator = id_translation.create_translator()
    print("\nSome untranslatable IDs:")
    pprint(translator.translate([0, -1, 10000], names="customer_id"))
