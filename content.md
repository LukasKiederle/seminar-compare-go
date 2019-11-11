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

#### Goroutines:
In go you can just make a "thread" by writing the **go** keyword
in front of a function like in the following example.

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
**a = 4, b = 8 or a = 4, b = 2**
For this problem of inconsistency golang uses channels. In the
following example almost same code is being shown but returning 
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

* Goroutines:
    * basic
    * channels
* Python: 
    * 

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