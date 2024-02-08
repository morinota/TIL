## link

- https://syedhasan010.medium.com/pipe-and-filter-architecture-bd7babdb908

# Pipe and Filter Architecture

Definition

Pipe and Filter is another architectural pattern, which has independent entities called filters (components) which perform transformations on data and process the input they receive, and pipes, which serve as connectors for the stream of data being transformed, each connected to the next component in the pipeline.

Many systems are required to transform streams of discrete data items, from input to output. Many types of transformations occur repeatedly in practice, and so it is desirable to create these as independent, reusable parts, Filters. (Len Bass, 2012)

Description of the Pattern

The pattern of interaction in the pipe-and-filter pattern is characterized by successive

transformations of streams of data. As you can see in the diagram, the data flows in one direction. It starts at a data source, arrives at a filter’s input port(s) where processing is done at the component, and then, is passed via its output port(s) through a pipe to the next filter, and then eventually ends at the data target.

A single filter can consume data from, or produce data to, one or more ports. They can also run concurrently and are not dependent. The output of one filter is the input of another, hence, the order is very important.

A pipe has a single source for its input and a single target for its output. It preserves the sequence of data items, and it does not alter the data passing through.

Advantages of selecting the pipe and filter architecture are as follows:

· Ensures loose and flexible coupling of components, filters.

· Loose coupling allows filters to be changed without modifications to other filters.

· Conductive to parallel processing.

· Filters can be treated as black boxes. Users of the system don’t need to know the logic behind the working of each filter.

· Re-usability. Each filter can be called and used over and over again.

However, there are a few drawbacks to this architecture and are discussed below:

· Addition of a large number of independent filters may reduce performance due to excessive computational overheads.

· Not a good choice for an interactive system.

· Pipe-and-fitter systems may not be appropriate for long-running computations.

Applications of the Pattern

In software engineering, a pipeline consists of a chain of processing elements (processes, threads, functions, etc.), arranged so that the output of each element is the input of the next. (Wiki, n.d.).

The architectural pattern is very popular and used in many systems, such as the text-based utilities in the UNIX operating system. Whenever different data sets need to be manipulated in different ways, you should consider using the pipe and filter architecture. More specific implementations are discussed below:

1. Compilers:

A compiler performs language transformation: Input is in language A and output is in language B. In order to do that the input goes through various stages inside the compiler — these stages form the pipeline. The most commonly used division consists of 3 stages: front-end, middle-end, and back-end.

The front-end is responsible for parsing the input language and performing syntax and semantic and then transforms it into an intermediate language. The middle-end takes the intermediate representation and usually performs several optimization steps on it, the resulting transformed program in is passed to the back-end which transforms it into language B.

Each level consists of several steps as well, and everything together forms the pipeline of the compiler.

2. UNIX Shell:

The Pipeline is one of the defining features of the UNIX shell, and obviously, the same goes for Linux, MacOS, and any other Unix-based or inspired systems.

In a nutshell, it allows you to tie the output of one program to the input of another. The benefit it brings is that you don’t have to save the results of one program before you can start processing it with another. The long-term and even more important benefit is that it encourages programs to be small and simple.

There is no need for every program to include a word-counter if they can all be piped into wc. Similarly, no program needs to offer its own built-in pattern matching facilities, as it can be piped into grep.

In the provided example, the input.txt is read and the output is then provided to grep as input which searches for the pattern “text” and then passes the results to sort, which sorts the results and outputs into the file, output.txt.

References
Len Bass, P. C. a. R. K., 2012. Software Architectures in Practice. 3rd ed. s.l.:Addison-Wesley Professional.

Wiki, n.d. Pipelining (Software). [Online]
Available at: https://en.wikipedia.org/wiki/Pipeline_(software)
