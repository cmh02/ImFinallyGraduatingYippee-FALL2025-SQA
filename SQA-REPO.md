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

Another major activity was expanding the architecture for my fuzzing pipeline. Particularly, I needed to formalize how the about input sources were managed and tracked along with how fuzz cases were executed and presented. For this, I created a central execution pipeline ([fuzz.py](test/fuzz/fuzz.py)) that enacts three other submodules: my [fuzzmanager](test/fuzz/fuzzmanager.py) to perform the fuzzing, my [resourcemanager](test/fuzz/resourcemanager.py) to download/parse input sources, and [a logging setup](test/fuzz/logging.py) to make pipeline output more robust. This allowed me to create a well-flowed pipeline that would be ready for continuous integration and ready to provide a post-fuzzing result summary.

#### GitHub Continuous Integration for Fuzzing

To integrate with GitHub CI, I create a [ci workflow configuration](.github/workflows/fuzzing.yml) for a very simple pipeline to be run on any push or PR:

1. Checkout the repo's code
2. Setup Python with the version used during development (`3.13.5`)
3. Install all Python dependencies with PIP
4. Run the main fuzzing pipeline to fuzz the target functions using all input sources
5. Upload the fuzzing summary to GitLab actions for CI insight

#### Addition of Unit Testing

While the fuzzing and initial forensics portion of this project was complete, one missing component was a clear use of the forensics within continuous integration. While fuzzing uses the target source functions and therefor involves the added forensics, displaying this for the 57,000+ fuzz cases would not be easy or clear. Additionally, since the overall objective is to test for bugs within the source code, fuzzing (when performed in the manner done in this project) does a great job at wide coverage but does not pinpoint specific use cases.

To provide visible examples of the added forensics, I extended this project to also include a base sweep of unit test cases for coverage of the five target functions. Primarily, this includes:

* One test case for each expected, normal-behavior result
  * Displays what basic forensics are always available for a function
* One test case for each possible error added with forensics
  * Displays what extra forensics may be available under each possible error case with my added validation

To facilitate the execution of my unit test cases, I decided to use [pytest](https://docs.pytest.org/en/stable/), as it is a much more modern framework and integrates nicely with GitHub's CI (with the use of the pytest-md addon). I implemented test cases to cover each of the target functions and explore forensics in a respective file for each function. All of these use the root logger to allow output to log files and console, enhancing the ability to investigate possible bugs when they occur.

#### GitHub Continuous Integration for Unit Testing

To expand my continious integration for unit testing, I created an [additional workflow](.github/workflows/unit.yml):

1. Checkout the repo's code
2. Setup Python with the version used during development (`3.13.5`)
3. Install all Python dependencies with PIP
4. Run all unit tests with pytest
5. Add the unit testing summary for GitHub actions
6. Upload the report as an artifact

### Code Deliverables

To ensure that the deiverable portion of this assignment was met for the code requirement, you can find the implementation in the following three locations:

* The fuzzing and unit tests are implemented in [test/fuzz](test/fuzz) and [test/unit](test/unit), respectively
* The forensics are implemented in [src/MLForensics_farzana/mining/mining.py](src/MLForensics_farzana/mining/mining.py)
* The CI pipelines are implemented in [.github/workflows](.github/workflows)

### Execution Deliverables

To ensure that the deliverable portion of this assignment was met for the execution requirement, the execution of the forensics, fuzzing, and continuous integration can be found for the respective CI workflows on GitHub.

* The latest fuzz workflow execution (includes fuzzing, fuzz reports, and CI) can be found [here](https://github.com/cmh02/ImFinallyGraduatingYippee-FALL2025-SQA/actions/runs/19778175957)
* The latest unit test workflow execution (includes unit tests, forensics, and CI) can be found [here](https://github.com/cmh02/ImFinallyGraduatingYippee-FALL2025-SQA/actions/runs/19778175942)

For each, the logs for test execution and resutls are shown. Additionally, the build itself should serve as confirmation of continuous integration with the project. Providing screenshots of the entire process seemed messy for my workflows, and to prevent an unorganized presentation, hope that the workflow executions being linked here (and the logs available for each) serve for the deliverable portion of the assignment.

### Results

#### Fuzzing Results

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

Overall, these exceptions show that there may be some vulerabilities within this function and the function should likely be safeguarded against the possible root causes of these exceptions. For instance, enhanced file detection, OS-specific checks, and permission verification may improve the results of this function.

#### Unit Test Results

From the [unit testing continuous integration pipeline](https://github.com/cmh02/ImFinallyGraduatingYippee-FALL2025-SQA/actions/workflows/unit.yml), the results of unit test cases show that all test cases passed for all target functions. There are a total of 49 test cases to provide coverage on these target functions. From the [unit test case summary section](https://github.com/cmh02/ImFinallyGraduatingYippee-FALL2025-SQA/actions/runs/19778175942/attempts/1#summary-56674170303), it is shown the spread of unit tests and the passing status for each:

| filepath                                                                   | function                                                                              | 
$$
\textcolor{#23d18b}{\tt{passed}}
$$

 |                        SUBTOTAL |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------: | ------------------------------: |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_checkPythonFile.py}}
$$

     | 
$$
\textcolor{#23d18b}{\tt{test\\_checkPythonFile\\_outputValueWhenPatterns}}
$$

         |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_checkPythonFile.py}}
$$

     | 
$$
\textcolor{#23d18b}{\tt{test\\_checkPythonFile\\_outputValueWhenNoPatterns}}
$$

       |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_checkPythonFile.py}}
$$

     | 
$$
\textcolor{#23d18b}{\tt{test\\_checkPythonFile\\_validationValueError}}
$$

            |      
$$
\textcolor{#23d18b}{\tt{3}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{3}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_checkPythonFile.py}}
$$

     | 
$$
\textcolor{#23d18b}{\tt{test\\_checkPythonFile\\_validationTypeError}}
$$

             |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_days\\_between.py}}
$$

      | 
$$
\textcolor{#23d18b}{\tt{test\\_days\\_between\\_outputWhenSameDate}}
$$

               |      
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_days\\_between.py}}
$$

      | 
$$
\textcolor{#23d18b}{\tt{test\\_days\\_between\\_outputWhenFirstMoreRecent}}
$$

        |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_days\\_between.py}}
$$

      | 
$$
\textcolor{#23d18b}{\tt{test\\_days\\_between\\_outputWhenSecondMoreRecent}}
$$

       |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_days\\_between.py}}
$$

      | 
$$
\textcolor{#23d18b}{\tt{test\\_days\\_between\\_validationValueError}}
$$

             |      
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_days\\_between.py}}
$$

      | 
$$
\textcolor{#23d18b}{\tt{test\\_days\\_between\\_validationTypeError}}
$$

              |      
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_dumpContentIntoFile.py}}
$$

 | 
$$
\textcolor{#23d18b}{\tt{test\\_dumpContentIntoFile\\_fileIsWritten}}
$$

               |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_dumpContentIntoFile.py}}
$$

 | 
$$
\textcolor{#23d18b}{\tt{test\\_dumpContentIntoFile\\_fileContentIsWritten}}
$$

        |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_dumpContentIntoFile.py}}
$$

 | 
$$
\textcolor{#23d18b}{\tt{test\\_dumpContentIntoFile\\_fileContentIsCorrect}}
$$

        |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_dumpContentIntoFile.py}}
$$

 | 
$$
\textcolor{#23d18b}{\tt{test\\_dumpContentIntoFile\\_returnVal}}
$$

                   |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_dumpContentIntoFile.py}}
$$

 | 
$$
\textcolor{#23d18b}{\tt{test\\_dumpContentIntoFile\\_validationValueError}}
$$

        |      
$$
\textcolor{#23d18b}{\tt{4}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{4}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_dumpContentIntoFile.py}}
$$

 | 
$$
\textcolor{#23d18b}{\tt{test\\_dumpContentIntoFile\\_validationTypeError}}
$$

         |      
$$
\textcolor{#23d18b}{\tt{6}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{6}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_getPythonFileCount.py}}
$$

  | 
$$
\textcolor{#23d18b}{\tt{test\\_getPythonFileCount\\_outputValueWhenPythonFiles}}
$$

   |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_getPythonFileCount.py}}
$$

  | 
$$
\textcolor{#23d18b}{\tt{test\\_getPythonFileCount\\_outputValueWhenNoPythonFiles}}
$$

 |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_getPythonFileCount.py}}
$$

  | 
$$
\textcolor{#23d18b}{\tt{test\\_getPythonFileCount\\_validationValueError}}
$$

         |      
$$
\textcolor{#23d18b}{\tt{3}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{3}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_getPythonFileCount.py}}
$$

  | 
$$
\textcolor{#23d18b}{\tt{test\\_getPythonFileCount\\_validationTypeError}}
$$

          |      
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{1}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_makeChunks.py}}
$$

          | 
$$
\textcolor{#23d18b}{\tt{test\\_makeChunks\\_listGetsSplit}}
$$

                        |      
$$
\textcolor{#23d18b}{\tt{3}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{3}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_makeChunks.py}}
$$

          | 
$$
\textcolor{#23d18b}{\tt{test\\_makeChunks\\_listGetsSplitToSize}}
$$

                  |      
$$
\textcolor{#23d18b}{\tt{5}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{5}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_makeChunks.py}}
$$

          | 
$$
\textcolor{#23d18b}{\tt{test\\_makeChunks\\_validationValueError}}
$$

                 |      
$$
\textcolor{#23d18b}{\tt{5}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{5}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{test/unit/tests/test\\_makeChunks.py}}
$$

          | 
$$
\textcolor{#23d18b}{\tt{test\\_makeChunks\\_validationTypeError}}
$$

                  |      
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |  
$$
\textcolor{#23d18b}{\tt{2}}
$$

 |
| 
$$
\textcolor{#23d18b}{\tt{TOTAL}}
$$

                                         |                                                                                       |     
$$
\textcolor{#23d18b}{\tt{49}}
$$

 | 
$$
\textcolor{#23d18b}{\tt{49}}
$$

 |

#### Forensics

With the above unit test cases, it is very easy to see the logged forensics for each of the target functions. While the entire logged forensics for each test case are shown in the [Unit Testing Step for the CI job](https://github.com/cmh02/ImFinallyGraduatingYippee-FALL2025-SQA/actions/runs/19778175942/job/56674170303), here's a quick example from each target test case during normal execution (without any error cases):

##### Forensics Example: dumpContentIntoFile()

```
test/unit/tests/test_dumpContentIntoFile.py::test_dumpContentIntoFile_fileContentIsCorrect 
-------------------------------- live log call ---------------------------------
INFO     root:test_dumpContentIntoFile.py:116 Unit Testing Logger Initialized!
INFO     root:test_dumpContentIntoFile.py:119 Starting test_dumpContentIntoFile_returnval!
INFO     root:mining.py:44 Call was made to dump content into file: /tmp/pytest-of-runner/pytest-0/test_dumpContentIntoFile_fileC1/test_output.txt
DEBUG    root:mining.py:69 File Path Type: <class 'str'>
DEBUG    root:mining.py:70 Content Type: <class 'str'>
DEBUG    root:mining.py:71 Content to Write Length: 40
DEBUG    root:mining.py:72 Content to write:

I am gonna graduate in like 2 weeks!!!

INFO     root:mining.py:85 Content successfully written to file: /tmp/pytest-of-runner/pytest-0/test_dumpContentIntoFile_fileC1/test_output.txt!
DEBUG    root:mining.py:86 Size of content written to file: 40 bytes!
PASSED                                                                   [ 34%]
```

##### Forensics Example: makeChunks()

```
 test/unit/tests/test_makeChunks.py::test_makeChunks_listGetsSplit[testList0-10] 
-------------------------------- live log call ---------------------------------
INFO     root:test_makeChunks.py:41 Unit Testing Logger Initialized!
INFO     root:test_makeChunks.py:44 Starting test_makeChunks_listGetsSplit!
INFO     root:mining.py:102 Call was made to make chunks for a list!
DEBUG    root:mining.py:130 Chunk Size Type: <class 'int'>
DEBUG    root:mining.py:131 Chunk Size Value: 10
DEBUG    root:mining.py:132 List Type: <class 'list'>
DEBUG    root:mining.py:133 List Length: 100
DEBUG    root:mining.py:134 List Content (truncated to 500 characters): 
['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_6', 'item_7', 'item_8', 'item_9', 'item_10', 'item_11', 'item_12', 'item_13', 'item_14', 'item_15', 'item_16', 'item_17', 'item_18', 'item_19', 'item_20', 'item_21', 'item_22', 'item_23', 'item_24', 'item_25', 'item_26', 'item_27', 'item_28', 'item_29', 'item_30', 'item_31', 'item_32', 'item_33', 'item_34', 'item_35', 'item_36', 'item_37', 'item_38', 'item_39', 'item_40', 'item_41', 'item_42', 'item_43', 'item_44', 'item_45', 'it
PASSED                                                                   [ 71%] 
```

##### Forensics Example: checkPythonFile()

```
test/unit/tests/test_checkPythonFile.py::test_checkPythonFile_outputValueWhenPatterns[/home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests] 
-------------------------------- live log call ---------------------------------
INFO     root:test_checkPythonFile.py:43 Unit Testing Logger Initialized!
INFO     root:test_checkPythonFile.py:46 Starting test_checkPythonFile_outputValueWhenPatterns!
INFO     root:mining.py:160 Call was made to check for patterns in python files!
DEBUG    root:mining.py:177 Directory Path Type: <class 'str'>
DEBUG    root:mining.py:178 Directory Path Value: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests
DEBUG    root:mining.py:190 Beginning walk to file looking for patterns!
DEBUG    root:mining.py:191 -> Pattern Dictionary: ['sklearn', 'h5py', 'gym', 'rl', 'tensorflow', 'keras', 'tf', 'stable_baselines', 'tensorforce', 'rl_coach', 'pyqlearning', 'MAMEToolkit', 'chainer', 'torch', 'chainerrl']
DEBUG    root:mining.py:192 -> OS Walk: [('/home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests', ['__pycache__'], ['test_checkPythonFile.py', 'test_makeChunks.py', 'test_dumpContentIntoFile.py', 'test_days_between.py', 'test_getPythonFileCount.py']), ('/home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/__pycache__', [], ['test_days_between.cpython-313-pytest-8.4.2.pyc', 'test_makeChunks.cpython-313-pytest-8.4.2.pyc', 'test_checkPythonFile.cpython-313-pytest-8.4.2.pyc', 'test_dumpContentIntoFile.cpython-313-pytest-8.4.2.pyc', 'test_getPythonFileCount.cpython-313-pytest-8.4.2.pyc'])]
DEBUG    root:mining.py:202 Checking directory: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests with 5 files!
DEBUG    root:mining.py:203 -> Dirnames (1): 
DEBUG    root:mining.py:205    --> __pycache__
DEBUG    root:mining.py:206 -> Filenames (5): 
DEBUG    root:mining.py:208    --> test_checkPythonFile.py
DEBUG    root:mining.py:208    --> test_makeChunks.py
DEBUG    root:mining.py:208    --> test_dumpContentIntoFile.py
DEBUG    root:mining.py:208    --> test_days_between.py
DEBUG    root:mining.py:208    --> test_getPythonFileCount.py
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_checkPythonFile.py
DEBUG    root:mining.py:230 --> File is a Python file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_checkPythonFile.py
DEBUG    root:mining.py:248 ----> Pattern found: sklearn in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_checkPythonFile.py
DEBUG    root:mining.py:248 ----> Pattern found: gym in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_checkPythonFile.py
DEBUG    root:mining.py:248 ----> Pattern found: sklearn in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_checkPythonFile.py
DEBUG    root:mining.py:248 ----> Pattern found: gym in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_checkPythonFile.py
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_makeChunks.py
DEBUG    root:mining.py:230 --> File is a Python file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_makeChunks.py
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:230 --> File is a Python file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:248 ----> Pattern found: tf in file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_dumpContentIntoFile.py
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_days_between.py
DEBUG    root:mining.py:230 --> File is a Python file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_days_between.py
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_getPythonFileCount.py
DEBUG    root:mining.py:230 --> File is a Python file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/test_getPythonFileCount.py
DEBUG    root:mining.py:202 Checking directory: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/__pycache__ with 5 files!
DEBUG    root:mining.py:203 -> Dirnames (0): 
DEBUG    root:mining.py:206 -> Filenames (5): 
DEBUG    root:mining.py:208    --> test_days_between.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:208    --> test_makeChunks.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:208    --> test_checkPythonFile.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:208    --> test_dumpContentIntoFile.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:208    --> test_getPythonFileCount.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/__pycache__/test_days_between.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/__pycache__/test_makeChunks.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/__pycache__/test_checkPythonFile.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/__pycache__/test_dumpContentIntoFile.cpython-313-pytest-8.4.2.pyc
DEBUG    root:mining.py:220 --> Checking file: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests/__pycache__/test_getPythonFileCount.cpython-313-pytest-8.4.2.pyc
PASSED                                                                   [  2%]
```

##### Forensics Example: days_between()

```
test/unit/tests/test_days_between.py::test_days_between_outputWhenSameDate[d1_1-d2_1] 
-------------------------------- live log call ---------------------------------
INFO     root:test_days_between.py:40 Unit Testing Logger Initialized!
INFO     root:test_days_between.py:43 Starting test_days_between_outputValueWhenPatterns!
INFO     root:mining.py:266 Call was made to calculate the days between two dates!
DEBUG    root:mining.py:283 Date 1 Type: <class 'datetime.datetime'>
DEBUG    root:mining.py:284 Date 1 Value: 2002-05-14 00:00:00
DEBUG    root:mining.py:285 Date 2 Type: <class 'datetime.datetime'>
DEBUG    root:mining.py:286 Date 2 Value: 2002-05-14 00:00:00
PASSED                                                                   [ 16%]
```

##### Forensics Example: getPythonFileCount()

```
test/unit/tests/test_getPythonFileCount.py::test_getPythonFileCount_outputValueWhenPythonFiles[/home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests] 
-------------------------------- live log call ---------------------------------
INFO     root:test_getPythonFileCount.py:39 Unit Testing Logger Initialized!
INFO     root:test_getPythonFileCount.py:42 Starting test_getPythonFileCount_outputValueWhenPythonFiles!
INFO     root:mining.py:361 Call was made to get python file count!
DEBUG    root:mining.py:378 Directory Path Type: <class 'str'>
DEBUG    root:mining.py:379 Directory Path Value: /home/runner/work/ImFinallyGraduatingYippee-FALL2025-SQA/ImFinallyGraduatingYippee-FALL2025-SQA/test/unit/tests
PASSED                                                                   [ 59%]
```

### Lessons Learned

#### Lesson One: Select fuzz input carefully

While someone intuitive, one important lesson I learned was that the sources of your fuzz input need to be selected carefully. If only a small set of fuzz inputs are used, then your testing will, by nature, be very limited. On the other hand, if you use too many sources, there is likely going to be lots of overlap and wasted time testing that overlap.

#### Lesson Two: Understand the goal beforehand, not after

Although this assignment was somewhat clear on what was expected, "fuzzing" and "forensics" still leaves a lot of room in direction. I found it very helpful and productive by clearly identifying what the end goal should be prior to starting or expanding my fuzzing. Instead of just diving in, knowing what I want to achieve made accomplishing it much easier.

Additionally, I spent quite a bit of time after completing the fuzzing and forensics portion on adding in the unit test cases. While not explicitly stated in the instructions, the assignment deliverables requires that we provide evidence of the execution of forensics. Because of this, I needed to add some formal way to be able to show the various forensics that I have added. If I had thought it through earlier on in the project, I may not have had to spend as much time doing these unit cases later on.

#### Lesson Three: Don't expect clean code

While I may be used to my development patterns, which would have a standard for logging forensics, runtime validation, comments, hinting, etc., this cannot be expected to happen in every project you come across. Knowing how to read and understand others' code is important, and provided particularly useful for this assignment. There was no "hey test this" or "this is important info" or "here's a vulnerability", it simply came down to understanding how to fuzz functions to find potential issues.

#### Lesson Four: Even with pre-built codebases, structure the project well

One of my largest hiccups was the need to restructure my project halfway through. This primarily arose when I wanted to modularize my fuzzing, get consistent references to the target source code, and prepare for continuous integration. Just because an assignment gives you a test-ready codebase does not mean that you should just throw files around - organizing it smartly helps productivity down the road. This especially helped me later on when I added unit testing, as my organization made it very easy to add on a new form of testing with a new CI pipeline, requiring minimal changes to my existing fuzzing structure (other than a few refactoring changes to differentiate between fuzzing and unit testing)

#### Lesson Five: Start small, then grow

Another major lesson that I have picked up throughout my undergraduate journey and proved true in this class is the idea of starting a project small and grow/scale it up from there. Often I find myself and others I work with to have a habit of thinking *big.* It is easy to want to do everything the project asks, from the start, especially when you feel that you have a good grasp on everything needed to be accomplished. However, it is still important to start with a basic prototype that accomplishes the minimum objective needed. From there, the project can be expanded out to cover more and more requirements, but throwing everything in all at once can just result in spaghetti code, endless debugging, major changes, and many other problems that plague software development.
