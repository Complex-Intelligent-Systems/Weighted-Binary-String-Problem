# Weighted Binary String Problem

This repository contains the benchmark instances and generator presented in the paper _"A Weighted Binary String Benchmark to Assess the Efficiency of Stochastic Search Pro"_

The study was conducted by **Vincenzo Cutello**, **Alessio Mezzina**, **Mario Pavone**, and **Francesco Zito** from the Department of Mathematics and Computer Science, University of Catania.

_Manuscript accepted for publication; full bibliographic reference will be updated soon._

**Department of Mathematics and Computer Science**  
University of Catania  
viale Andrea Doria 6, 95125 Catania, Italy

---

## Abstract

One-Max problem is a well-known benchmark toy problem in evolutionary computation, mainly used to evaluate the performance and search features of stochastic algorithms on binary strings. However, although it is one of the main toy problems used, it does not account for the importance and influence of decision variables, consequently limiting its applicability to real-world scenarios where binary choices carry different weights or costs. To address this limitation, a Weighted Binary String problem is proposed that can be seen as a variant of the One-Max problem based on weighted decision variables. We provide an open-source instance generator along with the specific instances used in our experiments. To study the nature of the proposed problem, we compare the performance of four classic metaheuristics: Genetic Algorithm, Particle Swarm Optimization, Immunological Algorithm, and Iterated Local Search. Outcomes suggest that exploitation-centric strategies yield outperforming results in this problem domain.

---

## Contents

- `InstanceGenerator/`: Python script for generating WBS instances
- `Instance/`: 21 Benchmark instances used in the paper

---

## Citation

If you use this generator or benchmark in your work, please cite:

> Cutello, V., Mezzina, A., Pavone, M., Zito, F.  
> "A Weighted Binary String Benchmark to Assess the Efficiency of Stochastic Search Processes"  
> Manuscript accepted for publication; full bibliographic reference will be updated soon.

---

For any questions or collaborations, please contact:  
📧 cutello@unict.it
📧 alessio.mezzina@phd.unict.it  
📧 mpavone@dmi.unict.it
📧 francesco.zito@unict.it
