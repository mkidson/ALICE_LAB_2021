#!/usr/bin/env python3
"""
Takes a screeshot of the current oscilloscope screen and saves it to the folder under the name given by the user.
"""
import oscilloscope.scopeRead

scope = oscilloscope.scopeRead.reader('ttyACM2')

scope.takeScreenshot()

