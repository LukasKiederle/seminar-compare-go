<h1 align="center">Compare Go Parallel Programming with Python</h1>
<p align="center">by Lukas Kiederle</p>

## Table of Contents
1. [Motivation](#motivation)
2. [The raft cluster](#the-raft-cluster)
3. [The raft cluster implemented](#the-raft-cluster-implemented)
3. [Conclusion](#conclusion)
3. [Sources](#sources)

## Motivation
This paper is going to reflect the technical differences between
Go and Python when building a simulated cluster which persists its status
 within all of its nodes. As soon as one node is updated, all the other
 nodes get informed about the new status.


## The raft cluster
* Theory
* Basics

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

#### In Go:
* 

#### In Python:
*

#### Differences

## Conclusion
* Comparison code length
* Code complexity
* 

## Sources
* https://pragmacoders.com/blog/multithreading-in-go-a-tutorial
* https://www.geeksforgeeks.org/multithreading-in-python-set-2-synchronization/
* https://github.com/jweigend/concepts-of-programming-languages