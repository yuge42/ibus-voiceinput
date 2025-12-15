#!/usr/bin/env python3

import sys
import gi
gi.require_version("IBus", "1.0")
from gi.repository import IBus, GLib

import logging

logging.basicConfig(
    filename="/tmp/ibus-sample.log",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

logging.debug("SampleEngine initialized")


class SampleEngine(IBus.Engine):
    def __init__(self):
        super().__init__()
        logging.debug("SampleEngine initialized")

    def do_process_key_event(self, keyval, keycode, state):
        logging.debug(f"keyval={keyval}")

        if keyval == IBus.KEY_Return:
            self.commit_text(IBus.Text.new_from_string("HELLO"))
            return True

        return True


def main():
    IBus.init()
    loop = GLib.MainLoop()

    bus = IBus.Bus()
    factory = IBus.Factory.new(bus.get_connection())

    factory.add_engine("sample", SampleEngine)

    bus.request_name("org.freedesktop.IBus.Sample", 0)
    loop.run()


if __name__ == "__main__":
    main()
