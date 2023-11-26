from rics import configure_stuff

configure_stuff()


def demo_available_data():
    from big_corporation_inc.id_translation import get_singleton

    print(get_singleton().placeholders)


def demo_translate():
    import pandas as pd
    from big_corporation_inc.id_translation import translate

    df = pd.read_csv("transactions.csv")
    result = translate(df, fmt="{id}:[{title}][{name}]")
    print(result)


if __name__ == '__main__':
    demo_available_data()
    demo_translate()
