[![DOI](https://zenodo.org/badge/253411923.svg)](https://zenodo.org/badge/latestdoi/253411923)

# SATIRE: Scalable Abstraction-guided Technique for Incremental Rigorous analysis of round-off Errors

Satire is a first order error analysis tools for obtaining rigorous bounds on 
floating point round-off errors. It works on straight line floating-point programs.
Satire, sheds light on how scalability and bound-tightness can be attained through
a combination of incremental analysis,  abstraction, and judicious use of concrete 
and symbolic evaluation. 


# Dependencies

Satire requires the following softwares to be installed.

* Requirements:
	* python > 3.6
	* [sly](https://github.com/dabeaz/sly)
	* [ply](https://github.com/dabeaz/ply)
	* [symengine](https://github.com/symengine/symengine)
	* [sympy](https://www.sympy.org/en/index.html)
	* [gelpia](https://github.com/soarlab/gelpia)

## Usage

Satire is a python based framework. The main function is available is "src/satern.py"
The "--help" command clarifies all the supporting arguments

#### Example1 (with default options)
  > python3 src/satern.py --std --file p3 src/satern.py --std --file large_benchmarks/reduction/Reduction_1024.txt

 The execution generates a `default.log` containing logging traces of the execution for debugging. This file name can be modified using the `--logfile <filename1>` option.
 
 The output is available in `outfile.txt`. This file name can be modified using the `--outfile <filename2>` option.
 The `--std` option enables logging information and results to be flushed to the standard output as well.

 The contents of the `outfile.txt` summarizes the execution time, analysis time and absolute error bounds for the specific benchmark

	INPUT_FILE : Reduction_1024.txt
	
	//-------------------------------------
	VAR : A_9_0
	ABSOLUTE_ERROR : 5.684341886080801e-13
	First-order Error : 5.684341886080801e-13
	REAL_INTERVAL : [-1024, 1024.0]
	FP_INTERVAL : [-1024.0000000000005, 1024.0000000000005]
	//-------------------------------------
	
	Optimizer Calls: 5
	Parsing time : 0.10396647453308105
	PreProcessing time : 0.0016448497772216797
	Analysis time : 33.121673822402954
	Full time : 33.23301911354065


#### Example2 (with abstraction option)
  > python3 src/satern.py --std --file large_benchmarks/reduction/Reduction_1024.txt --enable-abstraction --mindepth 15 --maxdepth 25

  Abstraction is by default turned off. Abstraction can be enabled using the  `--enable-abstraction` switch. 
  The default abstraction window inside Satire is set to (10,40). using `--mindepth <lower_depth>` and `--maxdepth <higher_depth>`, the lower bound
  and the upper bound of the abstraction window can be changed as desired.


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
 Smaller tests for both `FPtaylor` and Satire are available inside the test directory. For trying out FPtaylor tests you need to install [FPtaylor](https://github.com/soarlab/FPTaylor). Satire compatible tests are available in `tests/satern-tests/`.
