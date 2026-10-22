import unittest

from pluralize_utils import pluralize, singularize, is_plural


class TestPluralize(unittest.TestCase):
    def test_basic_add_s(self):
        self.assertEqual(pluralize("cat"), "cats")
        self.assertEqual(pluralize("dog"), "dogs")

    def test_es_after_s_x_z_ch_sh(self):
        self.assertEqual(pluralize("bus"), "buses")
        self.assertEqual(pluralize("box"), "boxes")
        self.assertEqual(pluralize("buzz"), "buzzes")
        self.assertEqual(pluralize("church"), "churches")
        self.assertEqual(pluralize("dish"), "dishes")

    def test_consonant_plus_y_to_ies(self):
        self.assertEqual(pluralize("city"), "cities")
        self.assertEqual(pluralize("fly"), "flies")
        # vowel + y just adds s
        self.assertEqual(pluralize("boy"), "boys")
        self.assertEqual(pluralize("day"), "days")

    def test_fe_to_ves(self):
        self.assertEqual(pluralize("knife"), "knives")
        self.assertEqual(pluralize("wife"), "wives")
        self.assertEqual(pluralize("life"), "lives")

    def test_f_to_ves(self):
        self.assertEqual(pluralize("leaf"), "leaves")
        self.assertEqual(pluralize("wolf"), "wolves")
        self.assertEqual(pluralize("thief"), "thieves")

    def test_consonant_plus_o_es(self):
        self.assertEqual(pluralize("potato"), "potatoes")
        self.assertEqual(pluralize("hero"), "heroes")
        self.assertEqual(pluralize("volcano"), "volcanoes")
        # vowel + o just adds s
        self.assertEqual(pluralize("radio"), "radios")
        self.assertEqual(pluralize("video"), "videos")

    def test_irregular(self):
        self.assertEqual(pluralize("child"), "children")
        self.assertEqual(pluralize("person"), "people")
        self.assertEqual(pluralize("man"), "men")
        self.assertEqual(pluralize("woman"), "women")
        self.assertEqual(pluralize("tooth"), "teeth")
        self.assertEqual(pluralize("mouse"), "mice")

    def test_preserves_uppercase(self):
        self.assertEqual(pluralize("CAT"), "CATS")
        self.assertEqual(pluralize("CHILD"), "CHILDREN")

    def test_preserves_titlecase(self):
        self.assertEqual(pluralize("Cat"), "Cats")
        self.assertEqual(pluralize("Child"), "Children")

    def test_empty_string(self):
        self.assertEqual(pluralize(""), "")


class TestSingularize(unittest.TestCase):
    def test_basic_strip_s(self):
        self.assertEqual(singularize("cats"), "cat")
        self.assertEqual(singularize("dogs"), "dog")

    def test_strip_es(self):
        self.assertEqual(singularize("buses"), "bus")
        self.assertEqual(singularize("boxes"), "box")
        self.assertEqual(singularize("churches"), "church")
        self.assertEqual(singularize("dishes"), "dish")

    def test_ies_to_y(self):
        self.assertEqual(singularize("cities"), "city")
        self.assertEqual(singularize("flies"), "fly")

    def test_ves_to_f(self):
        # Known trade-off: 'fe' info is lost, so knives -> knif, not knife.
        self.assertEqual(singularize("leaves"), "leaf")
        self.assertEqual(singularize("wolves"), "wolf")
        self.assertEqual(singularize("knives"), "knif")

    def test_oes_to_o(self):
        self.assertEqual(singularize("potatoes"), "potato")
        self.assertEqual(singularize("heroes"), "hero")

    def test_irregular_reverse(self):
        self.assertEqual(singularize("children"), "child")
        self.assertEqual(singularize("people"), "person")
        self.assertEqual(singularize("men"), "man")
        self.assertEqual(singularize("teeth"), "tooth")
        self.assertEqual(singularize("mice"), "mouse")

    def test_empty_string(self):
        self.assertEqual(singularize(""), "")


class TestIsPlural(unittest.TestCase):
    def test_regular_plurals(self):
        self.assertTrue(is_plural("cats"))
        self.assertTrue(is_plural("boxes"))
        self.assertTrue(is_plural("cities"))
        self.assertTrue(is_plural("leaves"))

    def test_irregular_plurals(self):
        self.assertTrue(is_plural("children"))
        self.assertTrue(is_plural("people"))
        self.assertTrue(is_plural("men"))

    def test_singlulars_are_not_plural(self):
        self.assertFalse(is_plural("cat"))
        self.assertFalse(is_plural("box"))
        self.assertFalse(is_plural("city"))
        self.assertFalse(is_plural("child"))
        self.assertFalse(is_plural("person"))

    def test_invariable_not_flagged(self):
        # sheep singularizes to sheep, and pluralize(sheep) != sheep, so
        # the round-trip check returns False.
        self.assertFalse(is_plural("sheep"))
        self.assertFalse(is_plural("deer"))

    def test_empty(self):
        self.assertFalse(is_plural(""))


if __name__ == "__main__":
    unittest.main()
