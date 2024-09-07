# Welcome to DTCNS!

**DTCNS**  is a Python open source toolbox building Digital Twin-Oriented Complex Network Systems

The project was started in 2021 by Miss. Jiaqi Wen, [Prof. Bogdan Gabrys](https://profiles.uts.edu.au/Bogdan.Gabrys) and [Prof. Kaska Musial-Gabrys](https://profiles.uts.edu.au/katarzyna.musial-gabrys)  at the Complex Adaptive Systems Lab - The University of Technology Sydney. This project is a core module for the simulation of Digital Twin-Oriented Complex Networked Systems in the near future.

We aim to develop and assess a modelling paradigm called Digital Twin Oriented Complex Networked System (DT-CNS) that incorporates increasing complexity levels dependent on heterogeneous network components and their changes over time. The DT-CNSs are composed of networks and dynamics of and on the networks [<sup>1</sup>](#refer-anchor-1). The networks can be represented as set of nodes connected with each other via edges where both nodes and edges can have attributes. The DT-CNS dynamics can be either considered as: (i) dynamic processes on the networks, which involve spreading phenomena including epidemic processes and information spreading processes, or (ii) dynamic networks with evolving structures and attributes (a.k.a. features) [<sup>2</sup>](#refer-anchor-2). For example, the DT-CNS of a social networked system can be composed of an evolving social network and the epidemic spreading process that propagates on the social networks through social contacts  (See the below Figure).


![image](https://github.com/JiaqWen/DTCNS/blob/main/Plots/SNSexample.png)


We propose a conceptual modelling framework for DT-CNSs, which progresses from the generation 1 DT-CNS to the generation 5 DT-CNS (a DT) with an increasing complexity level across five generations [<sup>1</sup>](#refer-anchor-1)[<sup>2</sup>](#refer-anchor-2). The generations of DT-CNSs each systemically vary in three key aspects: evolvability in dynamics, interrelations in dynamics and their interplay with the real world (See Figure below; Refer to [Project Overview](https://github.com/JiaqWen/DTCNS/blob/main/Overview.md) for more details). 

![image](https://github.com/JiaqWen/DTCNS/blob/main/Plots/ComplexityGen.png)

**DTCNS** package aims to realise the abovementioned conceptual ideas and the current functionalities enable the modelling of generation 1 DT-CNSs and their extension towards higher complexity levels. Currently, we initialise generation 1 DT-CNSs based on heterogeneous node features and feature representation, interaction rules (feature preferences) and transmission rules (seed selection and transmissibility set-ups) [<sup>3</sup>](#refer-anchor-3)[<sup>4</sup>](#refer-anchor-4). More details can be found in [Generation 1 DT-CNS (A Quick Start)](https://github.com/JiaqWen/DTCNS/blob/main/G1documents.ipynb).

**Please note that this package is under active development. We will soon supplement functionalities and documents for DT-CNSs in higher generations.**

## Installation Prerequisite

```
$ pip install numpy copy pandas networkx heapq os math
```
## Project Installation

Please navigate to the folder and run command:

```
$ python setup.py install
```

## Documents

[Project Overview](https://github.com/JiaqWen/DTCNS/blob/main/Overview.md)

[Generation 1 DT-CNS (A Quick Start)](https://github.com/JiaqWen/DTCNS/blob/main/G1documents.ipynb)

## References
[1. Jiaqi Wen, Bogdan Gabrys, and Katarzyna Musial. "Towards Digital Twin Oriented Modelling of Complex Networked Systems and Their Dynamics: A Comprehensive Survey." IEEE Access (2022).](https://ieeexplore.ieee.org/abstract/document/9801816)
  
[2. Jiaqi Wen, Bogdan Gabrys, and Katarzyna Musial. "Review and Assessment of Digital Twin--Oriented Social Network Simulators." IEEE Access (2023).](https://ieeexplore.ieee.org/document/10239386?source=authoralert)

[3. Jiaqi Wen, Bogdan Gabrys, and Katarzyna Musial. "Digital Twin-Oriented Complex Networked Systems based on Heterogeneous node features and interaction rules." arXiv preprint arXiv:2308.11034 (2023).](https://arxiv.org/abs/2308.11034)

[4. Jiaqi Wen, Bogdan Gabrys, and Katarzyna Musial. "Heterogeneous Feature Representation for Digital Twin-Oriented Complex
Networked Systems." arXiv preprint arXiv:2308.11034 (2023).](http://arxiv.org/abs/2309.13229)


## How to cite DTCNS

If you use BibTeX, cite using the following entries:

    @article@article{wen2024dtcns,
    title={DTCNS: A python toolbox for digital twin-oriented complex networked systems},
    author={Wen, Jiaqi and Gabrys, Bogdan and Musial, Katarzyna},
    journal={SoftwareX},
    volume={27},
    pages={101818},
    year={2024},
    publisher={Elsevier}
    }
    

