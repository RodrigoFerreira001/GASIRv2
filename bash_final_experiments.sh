#!/usr/bin/env bash
for((number = 0; number < 300; number++)){
	python gasir_new.py out.moreno_highschool 200 10
}

for((number = 0; number < 300; number++)){
	python gasir_new.py out.moreno_innovation 200 35
}

for((number = 0; number < 300; number++)){
	python gasir_new.py out.moreno_oz 200 30
}
