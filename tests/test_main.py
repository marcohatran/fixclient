import unittest
from unittest.mock import patch
from io import StringIO
from main import FixClient  # Replace with the actual module name

class TestFixClient(unittest.TestCase):
    def setUp(self):
        # Mocking the socket to test without actual network communication
        self.socket_patcher = patch("socket.socket")
        self.mock_socket = self.socket_patcher.start()

    def tearDown(self):
        self.socket_patcher.stop()

    @patch('your_module_name.FixClient.host', new='mocked_test_host')
    def test_send_message(self):
        # Replace with your actual implementation if needed
        fix_client = FixClient("mocked_test_host", 1234, "sender", "target", "00:00 SGT")
        fix_client.connect()

        with patch("builtins.print") as mock_print:
            fix_client.send_message("Test Message")

        self.mock_socket.return_value.send.assert_called_once_with("Test Message".encode())
        mock_print.assert_called_once_with("Sent: Test Message")

    @patch('your_module_name.FixClient.host', new='mocked_test_host')
    def test_receive_message(self):
        # Replace with your actual implementation if needed
        fix_client = FixClient("mocked_test_host", 1234, "sender", "target", "00:00 SGT")
        self.mock_socket.return_value.recv.return_value = "Received Message"

        with patch("builtins.print") as mock_print:
            received_message = fix_client.receive_message()

        self.assertEqual(received_message, "Received Message")
        mock_print.assert_called_once_with("Received: Received Message")

    # Add more test cases for other methods

if __name__ == "__main__":
    unittest.main()
