#!/usr/bin/env bash

python plot_convergence.py out.moreno_oz_convergence_norm.txt
python plot_convergence.py out.moreno_oz_convergence_vacin.txt

python plot_convergence.py out.moreno_highschool_convergence_norm.txt
python plot_convergence.py out.moreno_highschool_convergence_vacin.txt

python plot_convergence.py out.moreno_innovation_convergence_norm.txt
python plot_convergence.py out.moreno_innovation_convergence_vacin.txt