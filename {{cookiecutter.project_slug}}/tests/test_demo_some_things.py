from pprint import pprint

from {{cookiecutter.namespace}} import id_translation


def test_fancy_format_string():
    print("\nSome more information about the first three:")
    pprint(id_translation.translate(
        [1, 2, 3],
        names="customer_id",
        fmt="{name} <{email!r}> {last_name}",

    ))


def test_untranslatable_ids():
    print("\nSome untranslatable IDs:")
    pprint(
        id_translation.translate(
            [0, -1, 10000],
            names="customer_id",
            maximal_untranslated_fraction=1,
        )
    )
