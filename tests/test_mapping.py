from taas.mapping import Literal, Map, Concat, make_map
import unittest


class TestMapping(unittest.TestCase):

    row = {
        "id": "3",
        "foo": "bar",
        "baz": "bazza"
    }

    def test_literal(self):

        mystr = "foo"

        lit = Literal({"value": mystr})

        value = lit.emit(self.row)

        self.assertEqual(value, mystr)

    def test_map(self):
        mymap = Map({"field": "foo"})

        self.assertEqual(
            mymap.emit(self.row),
            "bar"
        )

        self.assertEqual(
            mymap.emit({"foo": "baz"}),
            "baz"
        )

    # TODO: Test *optional* maps.

    def test_concat(self):
        concat = Concat({
            "field": "id",
            "prefix": "https://example.com/",
            "postfix": "/self"
        })

        self.assertEqual(
            concat.emit(self.row),
            "https://example.com/3/self"
        )

    def test_make_map(self):

        # TODO: This should be a reusable chunk of data we can put somewhere.
        mapping = {
            "foo": "bar",
            "baz": {
                "type": "map",
                "field": "bar"
            },
            "lit": {
                "type": "literal",
                "value": "MyLiteralString"
            },
            "con": {
                "type": "concat",
                "field": "somefield",
                "prefix": "lol"
            }
        }

        made_map = make_map(mapping)

        assert(isinstance(made_map["foo"], Map))
        assert(isinstance(made_map["baz"], Map))
        assert(isinstance(made_map["lit"], Literal))
        assert(isinstance(made_map["con"], Concat))
