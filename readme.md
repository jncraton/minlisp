# minlisp

[![Lint](https://github.com/jncraton/minlisp/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/minlisp/actions/workflows/lint.yml)

A minimal [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)) interpreter written in Python

## Features

1. Basic arithmetic
2. Lambda expressions
3. Conditional logic
4. Variable definition

## Tasks

Complete the `parse` function so the supplied doctests pass.

> [!TIP]
> The entire `parse` function can be ~15 lines of code. If you find yourself writing a lot of code, take a step back and consider if there may be a simpler approach.

### Step 1: Atomic Values

Start by handling the simplest possible expressions: constants.

Example:

```python
>>> eval(1)
1
```

### Step 2: Variable Lookup

Expressions can be symbols that refer to values in an [environment](<https://en.wikipedia.org/wiki/Environment_(computer_science)>).

Example:

```python
>>> eval('x', env=[{'x': 1}])
1
```

### Step 3: Sequential Evaluation

A list of expressions should be evaluated in order, returning the result of the final expression.

Example:

```python
>>> eval([1, 2, 3])
3
```

### Step 4: Primitive Function Application

The core of the language is based on function calling using [prefix notation](<https://en.wikipedia.org/wiki/Polish_notation>).

Example:

```python
>>> eval(['+', 1, 1])
2
```

## Step 5: Nested Expressions

The evaluator must handle expressions within expressions.

Example:

```python
>>> eval(['+', 1, ['+', 2, 2]])
5
```

## Step 6: Conditionals

Implement the `if` special form for branching.

Example:

```python
>>> eval(['if', 1, 7, 13])
7
>>> eval(['if', 0, 7, 13])
13
```

## Step 7: Anonymous Functions

Introduce `lambda` to create [closures](<https://en.wikipedia.org/wiki/Closure_(computer_programming)>).

Example:

```python
>>> eval([['lambda', ['n'], ['+', 'n', 1]], 5])
6
```

## Step 8: Variable Binding

Add the ability to define variables in the environment.

Example:

```python
>>> eval([['define', 'x', 10], 'x'])
10
```

## Testing

Tests for the above steps have been provided for you. Ensure that your interpretter works as expected by running the doctests:

```bash
python3 -m doctest minlisp.py
```

or

```bash
make test
```

You can also run a test program as:

```bash
> python3 minlisp.py fib-self-passing.lisp
55
```
