import io
import unittest
from task2 import searcher

generator = searcher("01/example.txt", ["роза", "условий", "и"])


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.output = ['а Роза упала на лапу Азора\n']
        self.output2 = [
            'Равным образом рамки и место обучения кадров играет важную\n',
            'и административных условий?\n'
        ]

    def test_file(self) -> None:
        self.assertEqual(
            list(searcher("example.txt", ['роза'])),
            self.output
        )

    def test_file_2(self) -> None:
        self.assertEqual(
            list(searcher("example.txt", ['и'])),
            self.output2
        )

    def test_fileobject(self) -> None:
        fileobject = io.StringIO("""а Роза упала на лапу Азора\n
        С другой стороны постоянное информационно-техническое""")

        self.assertEqual(
            list(searcher(fileobject, ['на'])),
            self.output
        )

    def test_empty_fileobject(self) -> None:
        fileobject = io.StringIO("""""")
        self.assertEqual(
            list(fileobject),
            []
        )
