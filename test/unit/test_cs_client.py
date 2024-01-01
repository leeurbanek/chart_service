import logging
import unittest
from unittest.mock import MagicMock

from test.data import ctx
from src import config_dict
from src.data_service import client


debug = config_dict['default']['debug'] == 'True'
logger = logging.getLogger(__name__)


class UseTiingoReaderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.ctx = MagicMock()
        self.ctx.obj.return_value = ctx
        self.download = MagicMock()
        # self.download.return_value = get_data

    def tearDown(self) -> None:
        # logging.disable(logging.CRITICAL)
        del self

    @unittest.skip
    def test_reader_returns_generator(self):
        if debug: logger.debug(f"test_reader_returns_generator()")
        print(f"\nself.ctx.obj: {self.ctx.obj}")
        print(f"self.ctx.obj.return_value: {self.ctx.obj.return_value}")
        print(f"\nself.dowlnload: {self.download}")
        print(f"self.dowlnload.return_value: {self.download.return_value}")
        data = client.get_data(self.ctx)
        for i in range(len(self.download.return_value)):
            print(f"\nnext(data)={data}")
            print(f"\nself.download.return_value[{i}]={self.download.return_value[i]}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
