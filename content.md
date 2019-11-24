<h1 align="center">Compare Go Parallel Programming with Python</h1>
<p align="center">by Lukas Kiederle</p>

## Table of Contents

1. [Motivation](#motivation)
2. [The Raft cluster](#the-Raft-cluster)
3. [The Raft cluster implemented](#the-Raft-cluster-implemented)
3. [Conclusion](#conclusion)
3. [Sources](#sources)

## Motivation
The problem of having spread data over multiple networks is currently
omnipresent. For example databases like [Elastic Search](https://www.elastic.co/de/) or 
[Docker Swarm](https://docs.docker.com/engine/swarm/) need to deal with this efficiently in order to work reliable.

This paper is going to reflect the technical differences between
go and python when building a simulated cluster which contains its status
within all of its nodes. This is accomplished with the Raft algorithm which was
introduced by Diego Ongaro and John Ousterhou in 2014.


## The Raft algorithm
Raft is an understandable distributed consensus algorithm.
It was created based on the consensus algorithm [paxos](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf).
The key goal was to develop an alternative for paxos which is much easier
to understand and programmable.

Raft has been proven to be as efficient as paxos but is structured differently.
Diego Ongaro also claimed in his paper that Raft is more understandable for students
which was verified by a study.

The following chapters describe the Raft algorithm in detail.
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

#### The 2-Phase commit
A node can represent one value. It also has a invisible log.

When a leader node sends a status update to all of his followers, the
state change is added as an entry in the node's invisible log. The node replies 
that it stored the value.
The leader waits until the majority of nodes have stored the change. If he gets enough
responses in a specific time, he sets his state to the new value. Afterwards all
other nodes get the info to change to the new state which was saved in the log previously.

The cluster now has come to consensus or agreement about the system state. This is
called **log replication**.

#### What is a leader election in depth
In Raft there are two timeout settings which control elections. One of them is the election
timeout. The election timeout is the amount of time for a follower-node waits until
becoming a candidate.

After the election timeout a follower-node becomes a candidate and starts an election term.
It then votes for itself and requests votes from all other nodes.
If the receiving node hasn't voted yet in this term then it votes for the candidate
and the node resets its election timeout.
As soon as a candidate-node has more than half of the clusters votes it becomes the leader.

The leader-node begins to send out Append Entries messages to all of its followers.
These messages are sent in time periods specified by the heartbeat timeout.
Every follower-node responds to every Append Entries message it receives.
The leaders tenure will continue until a follower stops receiving heartbeats and
becomes a candidate.

Stopping or loosing a leader in an already working cluster ends in a reelection.
Only one node can be elected to a leader per term.
In order to prevent having multiple candidates at the same time
every node has randomized and therefore different election timer times.
Otherwise an election could result in a draw. This would just trigger a reelection
afterwards but cost additional time.
One more important thing is that the election timer of every node always takes longer than 
the heartbeat timer. Otherwise a node would start an election a healthy cluster which
makes no sense.

## Basic parallel processing
In order to implement the raft algorithm properly parallelism is need as a base.
This chapter explain the differences of golang and python when it comes to
parallel processing.

#### Goroutines:
A "thread" in golang is called goroutine.
This is not the same as a normal parallel processing. A goroutine can be processed concurrently
by every statement or about every line of code. In other languages like java 
the program can only execute whole functions parallel. This results in a finer way of
parallelism and better performance. Overall a pc can execute much more goroutines than 
normal threads because of this slight cutting of the code to be executed parallel.

Making a "thread" by can be easily done by writing the **go** keyword
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
In the following example almost the same code is being shown but returning 
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
In python parallel programming is done with threads.
For this python offers a **Thread**-Class.
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
decrement in the console. Once it has reached 0 the thread
finishes and stops itself.

To be able to call the threads synchronous
like golang does with channels, python uses the `.join()`-method.

## The Raft cluster implemented

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
* python threads are much slower than goroutines
  see: https://madeddu.xyz/posts/go-py-benchmark/

## Sources
* https://pragmacoders.com/blog/multithreading-in-go-a-tutorial
* https://www.geeksforgeeks.org/multithreading-in-python-set-2-synchronization/
* https://github.com/jweigend/concepts-of-programming-languages
* https://www.elastic.co/de/
* https://Raft.github.io/Raft.pdf
* http://thesecretlivesofdata.com/Raft/
* https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf
* https://madeddu.xyz/posts/go-py-benchmark/