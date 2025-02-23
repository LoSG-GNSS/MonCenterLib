import datetime
from logging import Logger
import logging
import subprocess
import tempfile
from unittest import TestCase, main
from unittest.mock import MagicMock, patch, call
from moncenterlib.stream2file import Stream2File
import typeguard


class TestStream2File(TestCase):
    def setUp(self) -> None:
        # self.str2file = Stream2File(False)
        return super().setUp()

    def test_init_raises(self):
        with self.assertRaises((typeguard.TypeCheckError)) as e:
            str2file = Stream2File("bla")

    def test_init_with_enable_logger(self):
        str2file = Stream2File()
        self.assertEqual(Logger, type(str2file.logger))
        self.assertEqual("Stream2File", str2file.logger.name)

    def test_init_with_disable_logger(self):
        str2file = Stream2File(False)
        self.assertEqual(Logger, type(str2file.logger))
        self.assertEqual("Stream2File", str2file.logger.name)

    def test_init_with_my_logger(self):
        logger = logging.getLogger()
        str2file = Stream2File(logger=logger)
        self.assertEqual(logger, str2file.logger)
        self.assertEqual("root", str2file.logger.name)

    def test_init_check_dublicate_handlers(self):
        str2file = Stream2File()
        str2file = Stream2File()
        self.assertEqual(1, len(str2file.logger.handlers))

    def test__check_name_in_connections(self):
        str2file = Stream2File(False)
        with self.assertRaises(Exception):
            str2file._check_name_in_connections(None)

        str2file.connections["test"] = None
        self.assertIsNone(str2file._check_name_in_connections("test"))

        str2file.connections.pop("test")

        with self.assertRaises(ValueError) as msg:
            str2file._check_name_in_connections("test")
        self.assertEqual(str(msg.exception), "Unknown name of connection 'test'.")

    def test__check_param_raises(self):
        str2file = Stream2File(False)
        param = {}
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Not found key \'type\' in param."')

        param = {"type": "some_type"}
        with self.assertRaises(ValueError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), "Unknown type \'some_type\' in param.")

        param = {"type": "serial",
                 #  "port": "",
                 "brate": "",
                 "bsize": "",
                 "parity": "",
                 "stopb": "",
                 "fctr": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'port\' in param."')

        param = {"type": "serial",
                 "port": "",
                 #  "brate": "",
                 "bsize": "",
                 "parity": "",
                 "stopb": "",
                 "fctr": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'brate\' in param."')

        param = {"type": "serial",
                 "port": "",
                 "brate": "",
                 #  "bsize": "",
                 "parity": "",
                 "stopb": "",
                 "fctr": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'bsize\' in param."')

        param = {"type": "serial",
                 "port": "",
                 "brate": "",
                 "bsize": "",
                 #  "parity": "",
                 "stopb": "",
                 "fctr": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'parity\' in param."')

        param = {"type": "serial",
                 "port": "",
                 "brate": "",
                 "bsize": "",
                 "parity": "",
                 #  "stopb": "",
                 "fctr": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'stopb\' in param."')

        param = {"type": "serial",
                 "port": "",
                 "brate": "",
                 "bsize": "",
                 "parity": "",
                 "stopb": "",
                 #  "fctr": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'fctr\' in param."')

        param = {"type": "tcpcli",
                 #  "addr": "",
                 "port": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'addr\' in param."')

        param = {"type": "tcpcli",
                 "addr": "",
                 #  "port": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'port\' in param."')

        param = {"type": "ntrip",
                 #  "user": "",
                 "passwd": "",
                 "addr": "",
                 "port": "",
                 "mntpnt": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'user\' in param."')

        param = {"type": "ntrip",
                 "user": "",
                 #  "passwd": "",
                 "addr": "",
                 "port": "",
                 "mntpnt": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'passwd\' in param."')

        param = {"type": "ntrip",
                 "user": "",
                 "passwd": "",
                 #  "addr": "",
                 "port": "",
                 "mntpnt": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'addr\' in param."')

        param = {"type": "ntrip",
                 "user": "",
                 "passwd": "",
                 "addr": "",
                 #  "port": "",
                 "mntpnt": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'port\' in param."')

        param = {"type": "ntrip",
                 "user": "",
                 "passwd": "",
                 "addr": "",
                 "port": "",
                 #  "mntpnt": ""
                 }
        with self.assertRaises(KeyError) as msg:
            str2file._check_param(param)
        self.assertEqual(str(msg.exception), '"Missing key \'mntpnt\' in param."')

    def test_add_connection(self):
        str2file = Stream2File(False)

        # raise
        param = {"type": "tcpcli",
                 "addr": "1.2.3.4",
                 "port": "123"
                 }

        with patch("moncenterlib.stream2file.os.path.isdir") as mock_isdir:
            mock_isdir.return_value = True
            str2file.add_connection("TEST", param)
            exp = {
                'TEST':
                {
                    'param': {'type': 'tcpcli', 'addr': '1.2.3.4', 'port': '123', 'on_start': ""},
                    'temp_file': None,
                    'temp_file_on_start': None,
                    'process': False
                }
            }
            self.assertEqual(str2file.connections, exp)

            str2file.add_connection("TEST2", param)
            exp = {
                'TEST': {
                    'param': {'type': 'tcpcli', 'addr': '1.2.3.4', 'port': '123', 'on_start': ""},
                    'temp_file': None,
                    'temp_file_on_start': None,
                    'process': False
                },
                'TEST2': {
                    'param': {'type': 'tcpcli', 'addr': '1.2.3.4', 'port': '123', 'on_start': ""},
                    'temp_file': None,
                    'temp_file_on_start': None,
                    'process': False
                }
            }
            self.assertEqual(str2file.connections, exp)

    def test_remove_connection(self):
        str2file = Stream2File(False)
        str2file._check_name_in_connections = MagicMock()
        str2file._stop_process = MagicMock()

        param = {"type": "tcpcli",
                 "addr": "1.2.3.4",
                 "port": "123"
                 }
        str2file.add_connection("TEST", param)
        self.assertEqual(str2file.connections, {"TEST": {
                         'param': {'type': 'tcpcli', 'addr': '1.2.3.4', 'port': '123', 'on_start': ''},
                         'temp_file': None,
                         'temp_file_on_start': None,
                         'process': False}
        })

        str2file.remove_connection("TEST")
        self.assertEqual(("TEST", ), str2file._check_name_in_connections.call_args_list[0].args)
        self.assertEqual(("TEST", ), str2file._stop_process.call_args_list[0].args)
        self.assertEqual(str2file.connections, {})

    def test_get_status(self):
        str2file = Stream2File(False)
        str2file._check_name_in_connections = MagicMock()
        temp_file = MagicMock()
        temp_file.name = "/some_file"

        str2file.connections = {"TEST": {
            'param': {'type': 'tcpcli', 'addr': '1.2.3.4', 'port': '123', 'output_dir': '/'},
            'temp_file': temp_file,
            'temp_file_on_start': temp_file,
            'process': None}
        }
        # check raise and method _check_name_in_connections
        with self.assertRaises(FileNotFoundError) as msg:
            str2file.get_status("TEST")
        self.assertEqual(str(msg.exception), "File to get status doesn't exist.")
        self.assertEqual(("TEST", ), str2file._check_name_in_connections.call_args_list[0].args)

        # check open file status
        with (patch("moncenterlib.stream2file.open") as mock_open,
              patch("moncenterlib.stream2file.os.path.isfile") as mock_isfile,
              tempfile.NamedTemporaryFile() as temp_file):
            mock_isfile.return_value = True
            str2file.connections["TEST"]["temp_file"] = temp_file

            result = str2file.get_status("TEST")

            self.assertEqual((temp_file.name, "r"), mock_open.call_args_list[0].args)
            self.assertEqual({"encoding": "utf-8"}, mock_open.call_args_list[0].kwargs)

        # check read file status
        with (patch("moncenterlib.stream2file.os.path.isfile") as mock_isfile,
              tempfile.NamedTemporaryFile(mode="w") as temp_file):
            mock_isfile.return_value = True
            with open(temp_file.name, "w", encoding="utf-8") as f:
                f.write("2020-01-01 00:00:00 123 456 connected")

            str2file.connections["TEST"]["temp_file"] = temp_file

            result = str2file.get_status("TEST")
            self.assertEqual(result, {"time": "2020-01-01 00:00:00", "byte": "123",
                             "bps": "456", "connect": ["connected"]})

        # check read file no data
        with (patch("moncenterlib.stream2file.os.path.isfile") as mock_isfile,
              tempfile.NamedTemporaryFile(mode="w") as temp_file):
            mock_isfile.return_value = True
            with open(temp_file.name, "w", encoding="utf-8") as f:
                f.write("")

            str2file.connections["TEST"]["temp_file"] = temp_file

            result = str2file.get_status("TEST")
            self.assertEqual(result, {"time": "", "byte": "", "bps": "", "connect": ""})

    def test_start(self):
        str2file = Stream2File(False)

        # raises
        str2file.connections = {"TEST": {
            'param': {"type": "serial", 'port': 'COM1', "brate": "115200", "bsize": "1024", "parity": "N", "stopb": "1", "fctr": "1", },
            'temp_file': None,
            'temp_file_on_start': None,
            'process': False,
        }
        }
        with self.assertRaises(Exception) as e:
            str2file.start("TEST", "bla bla")
        self.assertEqual(str(e.exception), "Path '' to dir is strange.")

        with self.assertRaises(Exception) as e:
            str2file.start("TEST", "/aa/ss.log")
        self.assertEqual(str(e.exception), "Path '/aa' to dir is strange.")

        str2file._check_name_in_connections = MagicMock()
        str2file._stop_process = MagicMock()
        str2file.connections = {"TEST": {
            'param': {'type': 'tcpcli', 'addr': '1.2.3.4', 'port': '123'},
            'temp_file': None,
            'temp_file_on_start': None,
            'process': None}
        }
        # check before condition
        with (patch("moncenterlib.tools.get_path2bin") as mock_tools,
              patch("moncenterlib.stream2file.subprocess.Popen") as mock_subprocess,
              patch("moncenterlib.stream2file.os.path.isdir") as mock_isdir):
            mock_isdir.return_value = True
            mock_subprocess.side_effect = Exception()

            with self.assertRaises(Exception):
                str2file.start("TEST", "")
            self.assertEqual(("TEST", ), str2file._check_name_in_connections.call_args_list[0].args)
            self.assertEqual(("TEST", ), str2file._stop_process.call_args_list[0].args)
            self.assertEqual(("str2str", ), mock_tools.call_args_list[0].args)

        # check serial condition
        with (patch("moncenterlib.tools.get_path2bin") as mock_get_path2bin,
              patch("moncenterlib.stream2file.subprocess.Popen") as mock_subprocess,
              patch("moncenterlib.stream2file.tempfile.NamedTemporaryFile") as mock_temp_file,
              patch("moncenterlib.stream2file.datetime") as mock_datetime,
              patch("moncenterlib.stream2file.os.path.isdir") as mock_isdir):
            mock_utcnow = mock_datetime.utcnow
            mock_utcnow.return_value = datetime.datetime(1970, 1, 1, 1, 2, 3)
            mock_get_path2bin.return_value = "/path2bin/str2str"
            mock_temp_file.return_value.name = "/some_file4stats"
            mock_isdir.return_value = True
            mock_subprocess.side_effect = Exception()

            str2file.connections = {"TEST": {
                'param': {"type": "serial", 'port': 'COM1', "brate": "115200", "bsize": "1024", "parity": "N", "stopb": "1", "fctr": "1", },
                'temp_file': None,
                'temp_file_on_start': None,
                'process': False,
            }
            }

            with self.assertRaises(Exception):
                str2file.start("TEST", "/output_dir/TEST_19700101_010203.log")
            self.assertEqual((['/path2bin/str2str',
                               '-outstat',
                               '/some_file4stats',
                               '-in',
                               'serial://COM1:115200:1024:N:1:1',
                               '-out',
                               'file:///output_dir/TEST_19700101_010203.log'], ), mock_subprocess.call_args_list[0].args)
            self.assertEqual({"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL},
                             mock_subprocess.call_args_list[0].kwargs)
            self.assertEqual(str2file.connections["TEST"]["temp_file"], mock_temp_file.return_value)
            self.assertEqual(str2file.connections["TEST"]["process"], True)

        # check tcpcli condition
        with (patch("moncenterlib.tools.get_path2bin") as mock_get_path2bin,
              patch("moncenterlib.stream2file.subprocess.Popen") as mock_subprocess,
              patch("moncenterlib.stream2file.tempfile.NamedTemporaryFile") as mock_temp_file,
              patch("moncenterlib.stream2file.datetime") as mock_datetime,
              patch("moncenterlib.stream2file.os.path.isdir") as mock_isdir):
            mock_utcnow = mock_datetime.utcnow
            mock_utcnow.return_value = datetime.datetime(1970, 1, 1, 1, 2, 3)
            mock_get_path2bin.return_value = "/path2bin/str2str"
            mock_temp_file.return_value.name = "/some_file4stats"

            mock_isdir.return_value = True
            mock_subprocess.side_effect = Exception()

            str2file.connections = {"TEST": {
                'param': {"type": "tcpcli", "output_dir": "/output_dir", "addr": "1.2.3.4", "port": "123"},
                'temp_file': None,
                'temp_file_on_start': None,
                'process': False,
            }
            }

            with self.assertRaises(Exception):
                str2file.start("TEST", "/output_dir/TEST_19700101_010203.log")
            self.assertEqual((['/path2bin/str2str',
                               '-outstat',
                               '/some_file4stats',
                               '-in',
                               'tcpcli://1.2.3.4:123',
                               '-out',
                               'file:///output_dir/TEST_19700101_010203.log'], ), mock_subprocess.call_args_list[0].args)
            self.assertEqual({"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL},
                             mock_subprocess.call_args_list[0].kwargs)
            self.assertEqual(str2file.connections["TEST"]["temp_file"], mock_temp_file.return_value)
            self.assertEqual(str2file.connections["TEST"]["process"], True)

        # check ntrip condition
        with (patch("moncenterlib.tools.get_path2bin") as mock_get_path2bin,
              patch("moncenterlib.stream2file.subprocess.Popen") as mock_subprocess,
              patch("moncenterlib.stream2file.tempfile.NamedTemporaryFile") as mock_temp_file,
              patch("moncenterlib.stream2file.datetime") as mock_datetime,
              patch("moncenterlib.stream2file.os.path.isdir") as mock_isdir):
            mock_utcnow = mock_datetime.utcnow
            mock_utcnow.return_value = datetime.datetime(1970, 1, 1, 1, 2, 3)
            mock_get_path2bin.return_value = "/path2bin/str2str"
            mock_temp_file.return_value.name = "/some_file4stats"
            mock_isdir.return_value = True
            mock_subprocess.side_effect = Exception()

            str2file.connections = {"TEST": {
                'param': {"type": "ntrip", "output_dir": "/output_dir", "user": "u", "passwd": "123", "addr": "1.2.3.4", "port": "123", "mntpnt": "QWER"},
                'temp_file': None,
                'temp_file_on_start': None,
                'process': False,
            }
            }

            with self.assertRaises(Exception):
                str2file.start("TEST", "/output_dir/TEST_19700101_010203.log")
            self.assertEqual((['/path2bin/str2str',
                               '-outstat',
                               '/some_file4stats',
                               '-in',
                               'ntrip://u:123@1.2.3.4:123/QWER',
                               '-out',
                               'file:///output_dir/TEST_19700101_010203.log'], ), mock_subprocess.call_args_list[0].args)
            self.assertEqual({"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL},
                             mock_subprocess.call_args_list[0].kwargs)
            self.assertEqual(str2file.connections["TEST"]["temp_file"], mock_temp_file.return_value)
            self.assertEqual(str2file.connections["TEST"]["process"], True)

    def test_stop(self):
        str2file = Stream2File(False)
        str2file._check_name_in_connections = MagicMock()
        str2file._stop_process = MagicMock()
        str2file.stop("TEST")
        self.assertEqual(("TEST", ), str2file._check_name_in_connections.call_args_list[0].args)
        self.assertEqual(("TEST", ), str2file._stop_process.call_args_list[0].args)

    def test__stop_process(self):
        str2file = Stream2File(False)
        str2file._check_name_in_connections = MagicMock()
        with (patch("moncenterlib.stream2file.subprocess.Popen") as mock_subprocess,
              patch("moncenterlib.stream2file.tempfile.NamedTemporaryFile") as mock_temp_file,
              patch("moncenterlib.stream2file.tempfile.NamedTemporaryFile") as mock_temp_file_on_start):

            # temo_file and process are not None
            str2file.connections = {"TEST": {
                'param': {},
                'temp_file': mock_temp_file,
                'temp_file_on_start': mock_temp_file_on_start,
                'process': mock_subprocess,

            }
            }

            str2file._stop_process("TEST")
            self.assertEqual(("TEST", ), str2file._check_name_in_connections.call_args_list[0].args)
            self.assertEqual(False, str2file.connections["TEST"]["process"])
            self.assertTrue(mock_temp_file.close.called)
            self.assertTrue(mock_temp_file_on_start.close.called)

            # temo_file and process are None
            mock_subprocess.reset_mock()
            mock_temp_file.reset_mock()
            mock_temp_file_on_start.reset_mock()
            str2file.connections = {"TEST": {
                'param': {},
                'temp_file': None,
                'temp_file_on_start': None,
                'process': False,
            }
            }

            str2file._stop_process("TEST")
            self.assertEqual(("TEST", ), str2file._check_name_in_connections.call_args_list[0].args)
            self.assertFalse(mock_temp_file.close.called)
            self.assertFalse(mock_temp_file_on_start.close.called)

    def test_add_connection_check_on_start(self):
        str2file = Stream2File(False)
        param = {"type": "tcpcli",
                 "addr": "1.2.3.4",
                 "port": "123"
                 }

        with (
            patch("moncenterlib.stream2file.os.path.isdir") as mock_isdir,
            patch("moncenterlib.stream2file.subprocess.Popen") as mock_subprocess,
            patch("moncenterlib.tools.get_path2bin") as mock_get_path,
            patch("moncenterlib.stream2file.tempfile.NamedTemporaryFile") as mock_temp_file,
            patch("moncenterlib.stream2file.datetime") as mock_datetime
        ):
            mock_utcnow = mock_datetime.utcnow
            mock_utcnow.return_value = datetime.datetime(1970, 1, 1, 1, 2, 3)

            mock_isdir.return_value = True

            mock_get_path.return_value = "/path2bin/str2str"
            mock_temp_file.return_value.name = "tempfile"

            mock_subprocess.side_effect = Exception()

            str2file.add_connection("TEST", param, "Some cmd")

            with self.assertRaises(Exception):
                str2file.start("TEST", "TEST_19700101_010203.log")

            self.assertEqual(['/path2bin/str2str',
                              '-outstat', 'tempfile',
                              '-in', 'tcpcli://1.2.3.4:123',
                              '-out', 'file://TEST_19700101_010203.log',
                              '-c', 'tempfile'], mock_subprocess.mock_calls[0].args[0])
            self.assertIsNotNone(str2file.connections['TEST']["temp_file_on_start"])
            self.assertEqual(str2file.connections['TEST']["temp_file_on_start"].name, "tempfile")
            self.assertEqual(str2file.connections['TEST']["temp_file_on_start"].mock_calls, [
                             call.write(b'Some cmd'), call.seek(0)])

    def test_get_connection_names(self):
        str2file = Stream2File(False)
        str2file.connections = {"TEST1": {}, "TEST2": {}}
        self.assertEqual(["TEST1", "TEST2"], str2file.get_connection_names())
        str2file.connections = {}
        self.assertEqual([], str2file.get_connection_names())

    def test_create_output_file_name(self):
        str2file = Stream2File(False)
        with (patch("moncenterlib.stream2file.datetime") as mock_datetime):
            mock_utcnow = mock_datetime.utcnow
            mock_utcnow.return_value = datetime.datetime(1970, 1, 1, 1, 2, 3)
            output_file = str2file.create_output_file_name("TEST", "/blabla")
            self.assertEqual("/blabla/TEST_19700101_010203.log", output_file)


if __name__ == "__main__":
    main()
