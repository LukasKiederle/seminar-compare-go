<h1 align="center">Compare Go Parallel Programming with Python</h1>
<p align="center">by Lukas Kiederle</p>

## Table of Contents

1. [Motivation](#motivation)
2. [The raft cluster](#the-raft-cluster)
3. [The raft cluster implemented](#the-raft-cluster-implemented)
3. [Conclusion](#conclusion)
3. [Sources](#sources)

## Motivation
The problem of having spread data over multiple networks is currently
omnipresent. For example databases like [Elastic Search](https://www.elastic.co/de/) or 
[Docker Swarm](https://docs.docker.com/engine/swarm/) need to deal with this efficiently in order to work reliable.

This paper is going to reflect the technical differences between
go and python when building a simulated cluster which contains its status
within all of its nodes. This is accomplished with the raft algorithm which was
introduced by Diego Ongaro and John Ousterhou in 2014.


## The raft algorithm
Raft is an understandable distributed consensus algorithm.
It was created based on the consensus algorithm [paxos](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf).
The key goal was to develop an alternative for paxos which is much easier
to understand and programmable.

Raft has been proven to be as efficient as paxos but is structured differently.
Diego Ongaro also claimed in his raft-paper that raft is more understandable for students
which was verified by a study.

The following chapters describe the raft algorithm in detail.
There will also be a comparison of an implementation in **go** and **python**.

#### Which problem does Raft solve?
First of all there is a node. A node can store a single value. 
A client now sends a request to the server(this one node). Coming to an agreement which is the new
state is easy. The node just updates its value. But what about having multiple nodes 
that should contain the same state? How are these nodes finding a consensus? 


#### What are the Raft Basics?
In order to have a working cluster multiple nodes are needed which know each other.
A node can be in one of these three states: FOLLOWER, CANDIDATE or LEADER.
FOLLOWER is the starting state for every node. If FOLLOWER-nodes don't hear in
a specific time from a LEADER they can become CANDIDATE.
 
The CANDIDATE requests votes from each other node in the cluster.
Every node will answer with their vote. The CANDIDATE becomes the leader if it gets the majority
of votes. This process is called leader election. It is described in the next chapter in detail.

The cluster is now in a correct state. This includes having exactly one leader and the
majority of nodes being reachable for the leader-node.


All incoming changes to the system now go through the leader-node. Its job is to inform 
all of his available follower-nodes with the new state. This is 
accomplished with a 2-phase commit.

#### 2-Phase commit
A node can represent one value. It also has a none visible log.

When a leader node sends a status update to all of his followers, the
state change is added as an entry in the node's none visible log. The node replies 
that it stored the value.
The leader waits until the majority of nodes have stored the change. If he gets enough
responses in a specific time, he sets his state to the new value. Afterwards all
other nodes get the info to change to the new state which was saved in the log previously.

The cluster now has come to consensus or agreement about the system state. This is
called **log replication**.

#### What is a leader election in depth
* In Raft there are two timeout settings which control elections.
* First is the election timeout.
* The election timeout is the amount of time a follower waits until becoming a candidate.
* election timeout is randomized
* After the election timeout the follower becomes a candidate and starts a new election term
, votes for himself, and sends out request votes
* If the receiving node hasn't voted yet in this term then it votes for the candidate
and the node resets its election timeout.
* Once a candidate has a majority of votes it becomes leader.
* The leader begins sending out Append Entries messages to its followers.
* These messages are sent in intervals specified by the heartbeat timeout.
* Followers then respond to each Append Entries message.
* This election term will continue until a follower stops receiving heartbeats and becomes a candidate.
* stopping the leader in a already working cluster results in a reelection
* Only one leader can be elected per term
* If two nodes become candidates at the same time then a split vote can occur.
* The nodes will wait for a new election

## Parallel processing
What are the differences from golang to python when it comes to
parallel programming.

#### Goroutines:
In go you can just make a "thread" by writing the **go** keyword
in front of a function like displayed in the following example.

``` go
package main

import (
  "fmt"
)

func main() {
  a, b := 1, 2

  go func() {
    b = a * b
  }()

  a = b * b

  fmt.Printf("a = %d, b = %d\n", a, b)
}
```
Depending on which task is being executed first, `a = b * b` or
the `go func()` the result will differ. Possible results are: 
**a = 4, b = 8 or a = 4, b = 2**.
This is called asynchronous execution.

To execute goroutines synchronous golang uses channels.
In the following example almost same code is being shown but returning 
a consistent result.

```go
package main

import (
  "fmt"
)

func main() {
  a, b := 1, 2

  operationDone := make(chan bool)
  go func() {
    b = a * b

    operationDone <- true //or false
  }()

  <-operationDone

  a = b * b

  fmt.Printf("a = %d, b = %d\n", a, b)
}
```
With the channel `operationDone` and the `go func()` writing a bool
into `operationDone` the program is able to wait at the call
`<-operationDone` for an element which is saved in operationDone
(Like a queue).
As soon as `<-operationDone` has a value the program goes ahead.

#### Python parallel programming:
Python offers a **Thread**-Class for parallel programming.
A class which can be used as thread looks like the following code block.

```python
from threading import Thread

class ServerThread(Thread):

    def __init__(self, counter):
        Thread.__init__(self)
        self.counter = counter

    def run(self):
        try:
            for i in range(0, self.counter):
                print(i)
        finally:
            print("Thread finished")
```
```python
from src.server.serverThread import ServerThread

if __name__ == '__main__':

    for x in range(8):
        server = ServerThread(x)
        server.start()
        # wait for the thread to terminate
        server.join()
```
This thread is a class which has a run function that counts down
one by one from a given value and prints every new
decrement in the terminal. Once it has reached 0 the thread
finishes and stops itself. To be able to call the threads synchronous
like goland does with channels, python uses the `.join()`-method.

## The raft cluster implemented

#### To implement
* Node
    * request_vote()
    * append_entries()
* Statemachine
* Timer
    * election_timeout()
    * hearbeat_timeout()
* ReplicatedLog
* Cluster

#### In Go:
* 

#### In Python:
*

#### Differences

## Conclusion
In conclusion ...

* Comparison code length
* Code complexity
* 

## Sources
* https://pragmacoders.com/blog/multithreading-in-go-a-tutorial
* https://www.geeksforgeeks.org/multithreading-in-python-set-2-synchronization/
* https://github.com/jweigend/concepts-of-programming-languages
* https://www.elastic.co/de/
* https://raft.github.io/raft.pdf
* http://thesecretlivesofdata.com/raft/
* https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf