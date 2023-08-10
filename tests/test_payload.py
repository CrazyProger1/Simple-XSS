import unittest
import os
import shutil

from settings import (
    PAYLOADS_DIR,
    PAYLOAD_MAIN_FILE,
    PAYLOAD_INIT_FILE,
    PAYLOAD_PACKAGE_FILE
)
from app.payload import DefaultPayload
from app.environment import Environment
from app.exceptions import PayloadLoadingError, InitFileImportError


class TestPayload(unittest.TestCase):
    PD_DIR = os.path.join(PAYLOADS_DIR, 'test_payload')
    PD_MAIN_FILE = os.path.join(PD_DIR, PAYLOAD_MAIN_FILE)
    PD_INIT_FILE = os.path.join(PD_DIR, PAYLOAD_INIT_FILE)
    PD_PACKAGE_FILE = os.path.join(PD_DIR, PAYLOAD_PACKAGE_FILE)

    @classmethod
    def setUpClass(cls) -> None:
        os.makedirs(cls.PD_DIR)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.PD_DIR)

    def test_loading_without_main_file(self):
        self.assertRaises(PayloadLoadingError, DefaultPayload.load, self.PD_DIR, Environment('test'))

    def test_loading(self):
        with open(self.PD_MAIN_FILE, 'w') as f:
            f.write('test{{environment.public_url}}')
        payload = DefaultPayload.load(self.PD_DIR, Environment(public_url='test'))
        self.assertIsInstance(payload, DefaultPayload)
        self.assertEqual(str(payload), 'testtest')
        os.remove(self.PD_MAIN_FILE)

    def test_init_file(self):
        open(self.PD_MAIN_FILE, 'w').close()

        with open(self.PD_INIT_FILE, 'w') as f:
            f.write('1 / 0')

        self.assertRaises(InitFileImportError, DefaultPayload.load, self.PD_DIR, Environment('test'))
        os.remove(self.PD_INIT_FILE)
        os.remove(self.PD_MAIN_FILE)

    def test_package_file(self):
        open(self.PD_MAIN_FILE, 'w').close()

        with open(self.PD_PACKAGE_FILE, 'w') as f:
            f.write('author="crazyproger1"\nversion="1.1"')
        payload = DefaultPayload.load(self.PD_DIR, Environment(public_url='test'))
        self.assertIsInstance(payload, DefaultPayload)

        self.assertIsNone(payload.metadata.name)
        self.assertIsNone(payload.metadata.description)
        self.assertEqual(payload.metadata.author, 'crazyproger1')
        self.assertEqual(payload.metadata.version, '1.1')

        os.remove(self.PD_PACKAGE_FILE)


if __name__ == '__main__':
    unittest.main()
