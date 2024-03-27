import unittest

from parse_vfdb import Organism


class TestOrganism(unittest.TestCase):

    def test_construct(self) -> None:
        name = 'Yersinia enterocolitica subsp. enterocolitica 8081'
        organism = Organism(name)
        self.assertEqual(organism.genus_name, 'Yersinia')
        self.assertEqual(organism.species_name, 'enterocolitica')
        self.assertEqual(organism.strain, 'subsp. enterocolitica 8081')

        name = 'Yersinia enterocolitica'
        organism = Organism(name)
        self.assertEqual(organism.genus_name, 'Yersinia')
        self.assertEqual(organism.species_name, 'enterocolitica')
        self.assertIsNone(organism.strain)
