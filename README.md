# seminar-compare-go

## Known issues in python raft example:
- election_timer can't be canceled because the timer is not available.
- election after restarting the old leader node doesnt work as expected