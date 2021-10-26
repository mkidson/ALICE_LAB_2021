# ALICE_LAB_2021
Contains the files modified and created by Miles Kidson for the ALICE TRD lab for UCT 3rd year physics, in 2021.

The basis of these programs comes from [OpenWave-1KB](https://github.com/tdietel/OpenWave-1KB), but many of the modules taken from that have been modified heavily, both for fixing as some didn't work, and for new purposes. The main goal of this section was to get the interface between TRD computer and oscilloscope working nicely. This has, for the most part, been achieved but there are still a few kinks in the process (namely the fact that the oscilloscope occasionally spits out data in the wrong format, which messes everything up. See line 297 of `dso1kb.py`). 

## Installation
The package `oscilloscopeRead` is where the magic happens. Make sure to run `pip install -r requirements.txt`, and to be safe I would recommend doing this in a virtual environment. To create the virtual environment run
```bash
python3 -m venv {venv name}
. {venv name}/bin/activate
pip install --upgrade pip
pip install -e oscilloscopeRead
```
The environment can then be accessed by running `. {venv name}/bin/activate` in the directory the previous commands were run in.

## Extra notes
There are some strange quirks when it comes to interfacing with the oscilloscope. I hope that for the most part this will not need to be done in the future, but in the event that you do need to change settings remotely, here are some tips:
- We found the ethernet interface much slower and more buggy than the USB interface, so we strongly recommending USB.
- The USB device name, which needs to be fed to either `scopeRead.reader()` or `dso1kb.Dso()`, can be found by running `dmesg` in the linux commandline after plugging the oscilloscope in and looking for something that looks like `ttyACM1` in the line `cdc_acm 3-8:2.0: {name}: USB ACM device`.
- The commands for the oscilloscope and what they do can be found in the Programming Manual in the Downloads section of [https://www.gwinstek.com/en-global/products/detail/GDS-1000B].
- I found it easiest to pass commands to the oscilloscope by running a python environment in the package directory, then doing 
    ```python
    import oscilloscopeRead.dso1kb
    dso = oscilloscopeRead.dso1kb.Dso('/dev/{device name}')
    dso.write('{command}\n')
    ```
    and if running a command that has an output, which should end with a "?", just run `dso.read()`. 
- When running in USB interface mode, `dso.read()` will read up until the next newline character ("\\n"). To get the next section, just run the command again. I have also created the `dso.readlines()` command, which will just read everything in the buffer.
- In order to completely clear the buffer, the command `dso.clearBuf()` exists.
- Very importantly, notice the "\\n" at the end of the command above. I found that when I didn't include the newline at the end of the command, things started to break when it came to the order of executed commands. I think it has something to do with how the oscilloscope actually executed the commands given to it, but nevertheless **ALWAYS INCLUDE A NEWLINE CHARACTER**.
- As mentioned before, I ran into an issue where the oscilloscope would, seemingly randomly, output data that was not in the form required; it had line breaks in the middle of it, which would mess with the `dso.read()` method. To get around this, when it happens I just set all the data to 0 and run `dso.clearBuf()`. I'm certain this can be improved, maybe by looking at how to reconstruct the data from the separate pieces, but I ran out of time to do that.
- I spent a while trying to work out what the time is between data points in the waveforms output by the oscilloscope and I'm fairly sure the number can be found in the header of the data output. Currently that number isn't being captured but in order to see it try running these commands in a python environment in the directory containing the `oscilloscopeRead` directory:
    ```python
    import oscilloscopeRead.dso1kb
    dso = oscilloscopeRead.dso1kb.Dso('/dev/{device name}')
    dso.write(':ACQ1:MEM?\n')
    dso.read()
    ```
    and the number following "Sampling Period" near the end of the output *should* be the spacing.

## Final housekeeping
The programs in the `not vital` folder are the programs I created while trying to understanding what was needed in this process. Some might be useful, such as `timeResolution.py`, but I am fairly sure most of them will not need to be used again. The sub-folder `old` has programs from previous years that were used for debugging and inspiration, but are all pretty much useless now.
The `screenshot.py` program is being kept here simply to show you how to take a screenshot. If you really want to use this, you could write something that just calls the appropriate function in `scopeRead.py`. 
