from tm.time_management import *

def test_categories():
    assert len(cat_en) == len(cat_ru)

def test_valid_time():
        assert valid_time('01.55 - 02.10 - Б -') == ('Б', 15)

def test_valid_time_english_category():
    assert valid_time('00.55 - 02.10 - B -') == ('Б', 75)

def test_valid_time_empty():
    assert valid_time('01.55 - 02.10 -') == ()
    assert valid_time('some random text') == ()

def test_valid_secondary_category():
    assert valid_secondary_category('17.30 - 17.35 - Б - python: committed changes to github.') == (('Б','python'), 5)

# if __name__ == "__main__":
#     pytest
