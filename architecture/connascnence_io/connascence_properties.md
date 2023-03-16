## link

- https://connascence.io/strength.html

# Properties

## Strength

The strength of a form of connascence is determined by the ease with which that type of coupling can be refactored. For example, connascence of name is a weak form of connascence because renaming entities across a codebase is usually reasonably trivial. However, connascence of meaning is considered a stronger form of connascence since semantic meaning is harder to find across an entire codebase.

Static connascences are considered to be weaker than dynamic connascences, since static connascences can be determined simply by examining the source code. Dynamic connascences require knowledge of run-time behavior, and thus are harder to reason about.

Strength and locality should be considered together. Stronger forms of connascence are often found within the same function, class, or module where their impact can be more easily observed.

## Locality

The locality of an instance of connascence is how close the two entities are to each other. Code that is close together (in the same module, class, or function) should typically have more, and higher forms of connascence than code that is far apart (in separate modules, or even codebases). Many of the stronger forms of connascence that can be devastating to the readability and maintainability of a codebase when they appear far apart are innocuous when close together.

![]()

Locality matters! Stronger connascences are more acceptible within a module. Weaker connascences should be used between entities that are far apart (in separate modules or even codebases).

## Degree

The degree of a piece of connascence is related to the size of its impact. Does the coupling in question affect 2 entities, or 200?

## The Origins of COnnascence

Connascence is a software quality metric that attempts to measure coupling between entities. The term was used in a computer science context by Meilir Page-Jones in his article, Comparing techniques by means of encapsulation and connascence, Communications of the ACM volume 35 issue 9 (September 1992).

In 1996, Meilir Page-Jones included a large section on connascence in his book "What every programmer should know about object-oriented design". The book can still be found on amazon.com.

## Other Resources

Since Meilir Page-Jones published his book, several other people have adapted and expanded on the concept of connascnence.

### Jim Weirich

The greatest proponent of connascence is probably the late Jim Weirich. Several examples of his contributions to the industry can be found below:

Connascence Examined. A one hour long talk from 2012 that goes into considerable detail of the various types of connascence.
Grand Unified Theory of Software Design. A 45 minute talk given at 'Aloha on Rails'.
The Grand Unified Theory. An earlier talk from 2009. Note: The audio quality on this talk is questionable at times.
Connascence Examined. Jim Weirich gave an hour long talk at YOW in 2012.
Ruby Rogues ep. 60. Ruby Rogues is a weekly podcast about programming. This episode features Jim Weirich, and discusses both the SOLID principles and connascence.

### Kevin Rutherford

Kevin Rutherford has published a series of blog posts about connascence: they have inspired much of the content on this website. He also has a recorded talk, Red, Green, ... now what?!, where he goes over the usage of connascence during a refactoring kata.

### Multiple Authors

In 2013, this google hangout was broadcast that included several luminaries of the software development industry, including Corey Haines, Curtis Cooley, Dale Emery, J. B. Rainsberger, Jim Weirich, Kent Beck, Nat Pryce, and Ron Jeffries.

### Josh Robb

In 2015 Josh Robb gave a talk titled Connascence & Coupling at codemania. That talk was the inspiration to build this site.

### Thomi Richards

In 2015 Thomi Richards summarized the contents of this website in a talk at Kiwi PyCon.

### Gregory Brown

In 2016 Gregory Brown wrote "Connascence as a Software Design Metric" for the practicingruby.com blog.

### Patches Welcome!

The connascence.io website is an open source project hosted on github. Help us make this website awesome! We're interested in any and all contributions you might have, including:

Spelling and grammatical fixes
New and better content
Links to other resources about connascence
Graphical & design changes
Translating pages into other languages
Translating examples into other programming languages
...anything else - give us your good ideas!
