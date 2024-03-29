from unittest import TestCase

from src.core.arguments import DefaultArgumentsSchema
from src.utils import argutil
from src.core.services import GraphicMode


class ArgumentsTests(TestCase):

    def setUp(self) -> None:
        self.parser = argutil.SchemedArgumentParser(scheme=DefaultArgumentsSchema)

    def test_parse_graphic_mode(self):
        args = self.parser.parse_typed_args(['-g', str(GraphicMode.GUI.value)])
        self.assertEqual(args.graphic_mode, GraphicMode.GUI)

        args = self.parser.parse_typed_args(['--graphic_mode', str(GraphicMode.GUI.value)])
        self.assertEqual(args.graphic_mode, GraphicMode.GUI)

    def test_parse_settings_file(self):
        args = self.parser.parse_typed_args(['-s', 'test.toml'])
        self.assertEqual(args.settings_file, 'test.toml')

        args = self.parser.parse_typed_args(['--settings_file', 'test.toml'])
        self.assertEqual(args.settings_file, 'test.toml')
