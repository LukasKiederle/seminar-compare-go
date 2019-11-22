# seminar-compare-go
## Setup:
- install python 3.8
- call test functions in [testmain.py](https://github.com/LukasKiederle/seminar-compare-go/blob/master/test/testmain.py)

## Known issues in python raft example:
- election_timer can't be canceled because the timer is not available.
- election after restarting the old leader node doesnt work as expected