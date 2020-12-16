[![DOI](https://zenodo.org/badge/253411923.svg)](https://zenodo.org/badge/latestdoi/253411923)

# SATIRE: Scalable Abstraction-guided Technique for Incremental Rigorous analysis of round-off Errors

Satire is a first order error analysis tool for obtaining rigorous bounds on 
worst case floating point round-off errors. It works on straight line floating-point programs.
Satire, sheds light on how scalability and bound-tightness can be attained through
a combination of incremental analysis,  abstraction, and judicious use of concrete 
and symbolic evaluation. 


# Dependencies

Satire requires the following softwares to be installed.

* Requirements:
	* python > 3.6
	* [sly](https://github.com/dabeaz/sly) > 0.3
	* [symengine](https://github.com/symengine/symengine) > 0.5.1
	* [sympy](https://www.sympy.org/en/index.html) > 1.4
	* [gelpia](https://github.com/soarlab/gelpia) (working commit ID: c28bf25593423f71ce6ef86122f2a8aa22bf0b33)
		* After installation, make gelpia/bin available in $PATH


## Usage

Satire is a python based framework. The main function is available is "src/satern.py"
The "--help" command clarifies all the supporting arguments

#### Example1 (with default options: serialized, no abstraction, no empirical analysis)
  > python3 src/satern.py --std --file large_benchmarks/reduction/Reduction_1024.txt

 The execution generates a `default.log` containing logging traces of the execution for debugging. This file name can be modified using the `--logfile <filename1>` option.
 
 The output is available in `outfile.txt`. This file name can be modified using the `--outfile <filename2>` option.
 The `--std` option enables logging information and results to be flushed to the standard output as well.

 The contents of the `outfile.txt` summarizes the execution time, analysis time and absolute error bounds for the specific benchmark

	INPUT_FILE : Reduction_1024.txt
	
	//-------------------------------------
	VAR : A_9_0
	ABSOLUTE_ERROR : 1.2505552149377763e-12
	First-order Error : 1.2505552149377763e-12
	REAL_INTERVAL : [-1024, 1024.0]
	FP_INTERVAL : [-1024.0000000000014, 1024.0000000000014]
	//-------------------------------------
	
	Optimizer Calls: 0
	Parsing time : 0.16805672645568848
	
	PreProcessing time : 0.0013127326965332031
	Analysis time : 29.50110626220703
	Full time : 29.67192506790161

#### Example2 (with abstraction option)
  > python3 src/satire.py --std --file large_benchmarks/reduction/Reduction_1024.txt --enable-abstraction --mindepth 15 --maxdepth 25

  Abstraction is by default turned off. Abstraction can be enabled using the  `--enable-abstraction` switch. 
  The default abstraction window inside Satire is set to (10,40). using `--mindepth <lower_depth>` and `--maxdepth <higher_depth>`, the lower bound
  and the upper bound of the abstraction window can be changed as desired.

#### Example3 (with parallelism enabled)
  > python3 src/satire.py --std --file large_benchmarks/reduction/Reduction_1024.txt --parallel

  Using `--parallel` switch, the user can fork multiple optimizer calls concurrently. To enable this, Satire maintains a worklist
  of optimizer queries, and resorts to solving them in parallel once the worklist exceeds a certain threshold (currently set at 20).
  The paralleism support is enabled on top of an expression hashing mechanism that reduces query time by storing digital signatures of the
  already solved queries.
  
#### Example4 (with Empirical Code Analysis option)
> python3 src/satire.py --std --file large_benchmarks/reduction/Reduction_1024.txt --empirical 100000000

The `--empirical` flag generates a C++ code for the benchmark performing shadow value analysis for single precision and double precision types. For higher precision it uses quad precision as a proxy to real numbers. The input this flag takes is an integer which denotes the number of times the shadow value analysis is performed and the code outputs the max error and the average error for the two types over all executions. The default value for this flag is 0 in which case the C++ code is not generated.

#### Testing
 A `runScipt` is provided inside the directory `large_benchmarks`. It contains the list of all
 large benchmark problems that has been tested with Satire. The `collect_results.py' script extracts the
 output information from each and aggregates into a final `Results.txt'

 Please make sure to modify $GPHOME inside runScript to point to Gelpia home directory. Gelpia bin directory must also be available to the PATH variable.

	> cd large_benchmarks 
	> bash runScript.sh 
	> gvim Results.txt 

 Full execution of the `runScript` will take few hours. Selectively, benchmarks can be commented out from `runScipt` as required.

#### Quick tests
 Smaller tests for both `FPtaylor` and Satire are available inside the test directory. For trying out FPtaylor tests you need to install [FPtaylor](https://github.com/soarlab/FPTaylor). Satire compatible tests are available in `tests/satire-tests/`.
