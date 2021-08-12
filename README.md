# Firmware tests

Tests to be performed for a firmware release.

## Install

There is no fancy installer at the moment. The code depends on the [python BLE lib](https://github.com/crownstone/crownstone-lib-python-ble).

## Config

The file `config.yaml` should first be configured.

- crownstones: A list of crownstones to be used for the test. There must be at least 1 normal, and 1 with brokent, always on, IGBT.
- tests: A selection of tests. Simply comment out tests you do not want to perform.
- keys: The keys to use for the tests.

## Running

Run `main.py`. For more options, run `main.py --help`.

It is an interactive program, where you will be asked to perform certain tasks.

## Output

There are 3 output files:

- ..result.txt
    - Contains a simple list of tests and whether they passed or failed.
- ...log
    - The log file of the tests. Can be used to debug when a test failed.
- ...json
    - Contains the state of the program, can be used later to resume tests.

