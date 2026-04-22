all: test

test:
	python3 -m doctest minlisp.py

lint:
	uvx black@24.1.0 --check .

format:
	uvx black@24.1.0 .

%.py: %-impl.py
	python3 -m doctest $<
	uvx dropimpl@0.3.0 $< $@ eval
	uvx black@24.1.0 $@

clean:
	rm -rf __pycache__
