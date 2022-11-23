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

# License

## Open-source license

This software is provided under a noncontagious open-source license towards the open-source community. It's available under three open-source licenses:
 
* License: LGPL v3+, Apache, MIT

<p align="center">
  <a href="http://www.gnu.org/licenses/lgpl-3.0">
    <img src="https://img.shields.io/badge/License-LGPL%20v3-blue.svg" alt="License: LGPL v3" />
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" />
  </a>
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0" />
  </a>
</p>

## Commercial license

This software can also be provided under a commercial license. If you are not an open-source developer or are not planning to release adaptations to the code under one or multiple of the mentioned licenses, contact us to obtain a commercial license.

* License: Crownstone commercial license

# Contact

For any question contact us at <https://crownstone.rocks/contact/> or on our discord server through <https://crownstone.rocks/forum/>.
