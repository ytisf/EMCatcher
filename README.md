# EMCatcher
EMCatcher is a headless assistant tool for the Proxrmark3. It is designed to work on a RaspberryPi or any small linux system that has the Proxmark3 connected and the Proxmark3 binary either installed or in path. The purpose of the EMCatcher is to enable the user to headlessly use the Proxmark3 to record LF/HF cards and store them to a file on longterm memory. 

## WorkFlow // Why
The Proxmark3 is a great tool. However, in headless mode, the Proxmark3 has no long term memory to store the cards. The EMCatcher is a tool that enables the user to use the Proxmark3 to record LF cards and store them to a file on longterm memory. In a Red Team engagement, we have not came across many situations where it is reasonable to walk up to an infiltration point carrying a Proxmark3 nor rarely will you collect the cards and then utilize them immediately. 

In our experience it is more common to collect the information ahead of time and write the tags to a T5577 (or any other cloned card for that matter) and utilize that. However, although the Proxmark3 is capable of collecting tags in headless mode, it can only store up to 2-4 tags (depending on your version) and what makes it even more challenging, is that retention of the collected tags depends on constant power supply as well as another Proxmark3 to re-read the collected tags off the existing proxmark. 

What we set out to do was to create a modification that will allow collection of a large set of tags that can be used in another stage, while operating in headless mode. 

## Operataions

### Setup
The setup for the EMCatcher requires that the Proxmark3 will be connected to a RaspberryPi. This setup has ONLY been tested on a Raspberry Pi Zero. After setup, the Raspberry Pi can be connected to a power source. In Our experience this works best if the Proxmark3 is embedded into an external item of clothing, such as an interior of a jacket sleeve on the exterior side, while the Raspberry Pi and power source are located in a less conspicuous place. 

Of course, it is highly recommended to test the setup multiple times before deploying it. 

### Configuration File
The configuration file is located at `settings.conf` as JSON and is in the following format:

```json
{
    "device": "/dev/tty.usbmodemiceman1",  // serial port
    "mode": "r", // r for read, w for write (not implemented)
    "freq": "lf", //  low frequency. hf for high frequency.
    "sample_rate": 0.1, // in seconds
    "custom_command": "" //overrides the default command
}
```

An alternative configuration file can be specified by providing a path to the configuration file with the `-s` or `--settings` option.

Configuration file can be verified with the `-v` or `--verify` option. This will include not just the integrity of the configuration file, but also attempt to connect to the Proxmark3 and verify that the configuration is valid. This does **not** include verification of a custom command.

### Background Process
By running `python3 EMCatcher.py` the EMCatcher will run directly and will not be a background process. That is mainly done for the testing purposes until the user can confirm that the EMCatcher is working as expected. For background execution the user can run `./EMCatcher_Background.sh` which will run the EMCatcher as a background process. If you want to specify some special command just edit the file `EMCatcher_Background.sh` and add the command you wish.

### Output
- Minimal logging is available with `stdout` and `stderr` since main operation should be in a headless mode.
- At the `logs` directory, a file is created for each run of the EMCatcher. The file name is the date and time of the execution. It will log general debugging information and any errors that occur.
- At the `cards` directory, a file is created for each catch of a card. The file name is the date and time of the execution. It will log the card data. It will log any output from the Proxmark3 as long as it does not display a *No tags found* prompt.

## Current Issues // Future Work
- At the moment, the setup just sends an `lf search` or `hf search` and stores values appropriately. It is setup for a sleep of 0.1 seconds between scans. However, scanning times for each **lf** or **hf** vary for us and are between 2-3 seconds on rotation. If you know the specific card type we highly recommend settings a specific command with the `custom_command` type in the settings file. For example, with a `lf em em410 read` we are able to complete cycles in ~0.08 seconds. 

- Need to add support in configuration file for custom path to Proxmark3 binary.

## Thanks
Obviously big shout out to the Proxmark3 community and authors @RfidResearchGroup & @iceman1001.






