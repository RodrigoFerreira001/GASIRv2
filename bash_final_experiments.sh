#!/usr/bin/env bash
for((number = 0; number < 100; number++)){
#	python gasir_new.py out.moreno_highschool 200 10
	python gasir_new.py out.moreno_highschool 200 10 --vaccinateds 9 4 5 32 3 61 27 25 19 20
}

for((number = 0; number < 100; number++)){
#	python gasir_new.py out.moreno_innovation 200 35
	python gasir_new.py out.moreno_innovation 200 35 --vaccinateds 232 167 179 137 231 237 25 1 64 215 21 52 178 207 20 118 60 89 102 58 24 128 51 131 78 121 15 152 177 54 48 23 136 2 218
}

for((number = 0; number < 100; number++)){
#	python gasir_new.py out.moreno_oz 200 30
	python gasir_new.py out.moreno_oz 200 30 --vaccinateds 6 9 127 113 45 48 196 90 46 47 201 146 92 199 213 136 217 49 69 178 172 44 87 139 175 8 215 171 198 10
}
