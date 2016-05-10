# PIAS-NS2
## Installation
Download [Network Simulator (NS) 2.34](https://sourceforge.net/projects/nsnam/files/allinone/ns-allinone-2.34/) and unzip it.
```
$ tar -zxvf ns-allinone-2.34.tar.gz
```

Copy [pFabric.patch](https://github.com/HKUST-SING/PIAS-NS2/blob/master/pFabric.patch) to the *top ns-2.34 folder* (```ns-allinone-2.34```) and apply the patch. Then install NS2.
```
$ cd ns-allinone-2.34
$ patch -p1 --ignore-whitespace -i pFabric.patch
$ ./install
```
Copy files in [tcp](https://github.com/HKUST-SING/PIAS-NS2/tree/master/tcp) folder to ```ns-allinone-2.34/ns-2.34/tcp/```.

Copy files in [queue](https://github.com/HKUST-SING/PIAS-NS2/tree/master/queue) folder to ```ns-allinone-2.34/ns-2.34/queue/```.

Add ```queue/priority.o``` to ```ns-allinone-2.34/ns-2.34/Makefile```.
 
Run ```make``` on ```/ns-allinone-2.34/ns-2.34```.

## Simulation Results
Please see our [latest online version](http://sing.cse.ust.hk/~wei/papers/pias-new.pdf) which is modified from the original NSDI version. In this new version, we update demotion threshold derivation and fix some bugs that may degrade the performance of PIAS.

## Running Large-Scale Simulations
You can find simulation scrips in [scripts](https://github.com/HKUST-SING/PIAS-NS2/tree/master/scripts) folder:
- [CDF_dctcp.tcl](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/CDF_dctcp.tcl) (web search workload), [CDF_vl2.tcl](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/CDF_vl2.tcl) (data mining workload) give flow size distributions used in our paper.
- [spine_empirical.tcl](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/spine_empirical.tcl), [spine_empirical_heter.tcl](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/spine_empirical_heter.tcl) (heterogeneous traffic pattern) and [tcp-common-opt.tcl] (https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/tcp-common-opt.tcl) are NS2 TCL simulation scripts.  
- [result.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/result.py) is used to parse final results.  
- [run_pias_dctcp.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_pias_dctcp.py) is used to run PIAS and DCTCP (one-priority PIAS) using the web search workload.
- [run_pias_vl2.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_pias_vl2.py) is used to run PIAS  and DCTCP (one-priority PIAS) using the data mining workload.
- [run_pfabric_dctcp.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_pfabric_dctcp.py) is used to run pFabric (remaining size and bytes sent) using the web search workload.
- [run_pfabric_vl2.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_pfabric_vl2.py) is used to run pFabric (remaining size and bytes sent) using the data mining workload.
- [run_lldct_dctcp.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_lldct_dctcp.py) is used to run L2DCT using the web search workload.
- [run_lldct_vl2.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_lldct_dctcp.py) is used to run L2DCT using the data mining workload.
- [run_pias_dctcp_oversub.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_pias_dctcp_oversub.py) is used to run PIAS and DCTCP (one-priority PIAS) using the web search workload in a 3:1 oversubscribed network.
- [run_pias_heter.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/run_pias_heter.py) is used to run PIAS and DCTCP (one-priority PIAS) using the heterogeneous workload (a mix of web search and data mining).

There are many parameters to configue in `run_[transport]_[workload].py`. Note that you need to modify ```ns_path``` and ```sim_script ``` correspondingly. 

For each simulation, it will create a folder whose name is `[workload]_[transport]_[load]`. For example, if we run PIAS using the websearch workload at 90% load, we will get a folder named `websearch_pias_90`.

Each folder contains two files: ```flow.tr``` and ```logFile.tr```. The ```flow.tr``` gives flow completion time results with the following format:
```
number of packets, flow completion time, number of timeouts, src ID, dst ID
```

You can use [result.py](https://github.com/HKUST-SING/PIAS-NS2/blob/master/scripts/result.py) to parse ```flow.tr``` files as follows:
```
$ python result.py -a -i [path]/flow.tr
```

## Contact
If you have any question about PIAS simulation code, please contact [Wei Bai](http://sing.cse.ust.hk/~wei/).

## Acknowledgements
We thank [Mohammad Alizadeh](https://people.csail.mit.edu/alizadeh/) for sharing pFabric simulation code.  




