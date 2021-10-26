# ALICE_LAB_2021
Contains the files modified and created by Miles Kidson for the ALICE TRD lab for UCT 3rd year physics, in 2021.

The basis of these programs comes from [OpenWave-1KB](https://github.com/tdietel/OpenWave-1KB), but many of the modules taken from that have been modified heavily, both for fixing as some didn't work, and for new purposes. The main goal of this section was to get the interface between TRD computer and oscilloscope smooth. This has, for the most part, been achieved but there are still a few kinks in the process (namely the fact that the oscilloscope occasionally spits out data in the wrong format, which messes everything up. See line 297 of `dso1kb.py`). 

The package `scopeReadout` is where the magic happens. Make sure to run `pip install -r requirements.txt`, and to be safe I would recommend doing this in a virtual environment:
```bash
$ python3 -m venv {venv name}
$ . {venv name}/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
```

The programs in the `not vital` folder are the programs I created while trying to understanding what was needed in this process. Some might be useful, such as `timeResolution.py`, but I am fairly sure most of them will not need to be used again. The sub-folder `old` has programs from previous years that were used for debugging and inspiration, but are all pretty much useless now.
