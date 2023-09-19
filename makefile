all:
	python3 main.py ./testcases/t1.txt
grammar:
	python -m lark.tools.standalone json.lark > grammar.py