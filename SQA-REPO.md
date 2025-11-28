# ImFinallyGraduatingYippee-FALL2025-SQA Report

Class: COMP5710 Software Quality Assurance

Team Name: ImFinallyGraduatingYippee

Team Members: Chris Hinkson [@cmh02](https://github.com/cmh02)

### Introduction

For this project, a source taget codebase was provided. The goal was to create a Continuous Integration (CI) to fuzz this codebase on five select functions. Additionally, new forensics should be added to select functions from the codebase.

### Activities

#### Initial Look Around

The first step I took in the this assignment was to "scope around" the target codebase, identified what it was intended for, and gain overall insight into what I would be testing for. Next, I thought out how I could organize my fuzzing and CI pipeline to support this codebase. With this in mind, I moved into creating my first fuzzing script, using the same fuzzing input (Big List of Naughty Words) from a previous workshop. After doing some simple tests to ensure conceptual vision, I began to formalize my codebase and expand my fuzzing pipeline.

#### Fuzz Input Source Selection

One major activity was identifying which sources I could pull inputs from for the fuzzing pipeline. From my knowledge and based on previous assignments, I determind two main sources of fuzzing input to use in this project:

* [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings)
* [FuzzDB](https://github.com/fuzzdb-project/fuzzdb)

#### Fuzz Target Selection

After looking around the codebase, I identified that the most-fuzzible functions (to demonstrate in this assignment, at least) were located in [the mining.py source code submodule](src/MLForensics_farzana/mining/mining.py). Based on the overall signature of the functions and the desire for me to not mess up my local git, I selected five functions from this submodule:

* `dumpContentIntoFile()`
* `makeChunks()`
* `checkPythonFile()`
* `days_between()`
* `getPythonFileCount()`

Looking a bit further at these functions (into more of a Greybox fuzzing scenario or even Whitebox depending upon perspective), the functions lack initial explicit handling of validation. Particularly, there is no type hinting, no nullity check, no valid type checking, and little validation. Most functions simply attempt to perform an operation and rely on other calls to "pass up" any errors (or rather, they hope that they don't occur at all). 

To align with these expectations, I based my `pass` and `fail` criteria on the presence of un-whitelisted exceptions. To implement this, I make a list of exceptions that I expect to occur under certain conditions, including `TypeError` and `ValueError`. The idea is that, even though the target functions do not explicitly check for conditions that would result in these errors, the underlying behavior of them should lead to them for the majority of input and does not designate a system failure on their own. Instead, more rare errors - as observed for a smaller subset of fuzzing input - would indicate that the selected target functions contain critical bugs.

#### Expanding Fuzz Architecture

Another major activity was expanding the architecture for my fuzzing pipeline. Particularly, I needed to formalize how the about input sources were managed and tracked along with how fuzz cases were executed and presented. For this, I created a central execution pipeline ([fuzz.py](test/fuzz/fuzz.py)) that enacts three other submodules: my [fuzzmanager](test/fuzz/fuzzmanager.py) to perform the fuzzing, my [resourcemanager](test/fuzz/resourcemanager.py) to download/parse input sources, and [a logging setup](test/fuzz/logging.py) to make pipeline output more robust.

#### GitHub Continuous Integration

To integrate with GitHub CI, I create a [ci workflow configuration](.github/workflows/ci.yml) for a very simple pipeline to be run on any push or PR:

1. Checkout the repo's code
2. Setup Python with the version used during development (`3.13.5`)
3. Install all Python dependencies with PIP
4. Run the main fuzzing pipeline to fuzz the target functions using all input sources
5. Upload the fuzzing summary to GitLab actions for CI insight

### Results

#### Overall Fuzzing Results

With the final fuzzing pipeline, the following cases were performed:

* Total Fuzzed Functions: `5`
* Total Fuzzing Operations Run: `57470`
* Total Fuzzing Operations Passed: `57050`
* Total Fuzzing Operations Failed: `420`

Additionally, it is worth mentioning that only one target function (`dumpContentIntoFile`) out of the original five caused the fuzzing failures shown above. Here's a detailed look at the results from this function:

* Total Fuzzing Operations Run: 11494
* Total Fuzzing Operations Passed: 11074
* Total Fuzzing Operations Failed: 420
* Error Counts:
  * `FileNotFoundError`: 390
  * `OSError`: 16
  * `PermissionError`: 12
  * `NotADirectoryError`: 1
  * `IsADirectoryError`: 1

Overall, these exceptions show that there may be some vulerabilities within this function. and the function should likely be safeguarded against the possible root causes of these exceptions.

### Lessons Learned

#### Lesson One: Select fuzz input carefully

While someone intuitive, one important lesson I learned was that the sources of your fuzz input need to be selected carefully. If only a small set of fuzz inputs are used, then your testing will, by nature, be very limited. On the other hand, if you use too many sources, there is likely going to be lots of overlap and wasted time testing that overlap.

#### Lesson Two: Understand the goal beforehand, not after

Although this assignment was somewhat clear on what was expected, "fuzzing" and "forensics" still leaves a lot of room in direction. I found it very helpful and productive by clearly identifying what the end goal should be prior to starting or expanding my fuzzing. Instead of just diving in, knowing what I want to achieve made accomplishing it much easier.

#### Lesson Three: Don't expect clean code

While I may be used to my development patterns, which would have a standard for logging forensics, runtime validation, comments, hinting, etc., this cannot be expected to happen in every project you come across. Knowing how to read and understand others' code is important, and provided particularly useful for this assignment. There was no "hey test this" or "this is important info" or "here's a vulnerability", it simply came down to understanding how to fuzz functions to find potential issues.

#### Lesson Four: Even with pre-built codebases, structure the project well

One of my largest hiccups was the need to restructure my project halfway through. This primarily arose when I wanted to modularize my fuzzing, get consistent references to the target source code, and prepare for continuous integration. Just because an assignment gives you a test-ready codebase does not mean that you should just throw files around - organizing it smartly helps productivity down the road.

#### Lesson Five: Start small, then grow

Another major lesson that I have picked up throughout my undergraduate journey and proved true in this class is the idea of starting a project small and grow/scale it up from there. Often I find myself and others I work with to have a habit of thinking *big.* It is easy to want to do everything the project asks, from the start, especially when you feel that you have a good grasp on everything needed to be accomplished. However, it is still important to start with a basic prototype that accomplishes the minimum objective needed. From there, the project can be expanded out to cover more and more requirements, but throwing everything in all at once can just result in spaghetti code, endless debugging, major changes, and many other problems that plague software development.
