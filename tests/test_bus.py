#!/usr/bin/env python3

import localbus
import signal
import sys
import time
import unittest

class TestBus(unittest.TestCase):

    def setUp(self):
        self.bus1 = localbus.Bus(self.receive_callback_bus1, unique_identifier=1)
        self.bus2 = localbus.Bus(self.receive_callback_bus2, unique_identifier=2)
        self.bus3 = localbus.Bus(self.receive_callback_bus3, unique_identifier=3)
        self.buf1 = None
        self.buf2 = None
        self.buf3 = None

    def tearDown(self):
        self.bus1.stop()
        self.bus2.stop()
        self.bus3.stop()

    def receive_callback_bus1(self, message):
        self.buf1 = message

    def receive_callback_bus2(self, message):
        self.buf2 = message
    
    def receive_callback_bus3(self, message):
        self.buf3 = message

    def test_send_receive(self):
        self.bus1.send('test')
        time.sleep(0.1)
        self.assertEqual(self.buf2, 'test')
        self.assertEqual(self.buf3, 'test')
        self.bus2.send('test')
        time.sleep(0.1)
        self.assertEqual(self.buf1, 'test')
        self.assertEqual(self.buf3, 'test')

    def test_dont_loopback(self):
        self.bus1.send('test')
        time.sleep(0.1)
        self.assertIsNone(self.buf1)

    def test_long_payload(self):
        payload = ""
        for i in range(2048):
            payload += '@'
        # we don't want half messages, overlength send should just return
        # false and send nothing
        self.assertFalse(self.bus1.send(payload))
        self.assertIsNone(self.buf1)
        self.assertIsNone(self.buf2)
        self.assertIsNone(self.buf3)
        
if __name__ == '__main__':
    unittest.main()

