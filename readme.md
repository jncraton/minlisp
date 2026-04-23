# minlisp

[![Lint](https://github.com/jncraton/minlisp/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/minlisp/actions/workflows/lint.yml)

A minimal [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)) interpreter written in Python

## Learning Outcomes

After completing this assignment, learners will be able to:

* Implement an [interpreter](https://en.wikipedia.org/wiki/Interpreter_(computing)) to evaluate [symbolic expressions](https://en.wikipedia.org/wiki/S-expression).
* Manage lexical scoping and environments using a stack to handle variable shadowing and lookups.
* Implement lazy evaluation for conditional branching to control execution flow.

## Background

This project implements a minimal evaluator to see how symbolic expressions can drive computation. By writing a few lines of Python to handle environment lookups and function application, we can explore the same elegance McCarthy discovered when he reduced the complexity of the early Lisp system. The project focuses on the final, simplified state where a small class of symbolic expressions is sufficient to execute any partial recursive function.

> In the course of its development the Lisp system went through several stages of simplification and eventually came to be based on a scheme for representing the partial recursive functions of a certain class of symbolic expressions.
>
> [John McCarty, 1960](https://dl.acm.org/doi/epdf/10.1145/367177.367199)

## Features

The interpreter developed for this projects supports only a very small subset of the larger Lisp language:

1. Prefix function execution
2. `+` operator
3. `lambda` to define functions
4. `if`
5. `define` to bind names to values

## Example

Once complete, the interpreter should be able to run basic LISP programs such as this one that can multiply two numbers:

```lisp
(
  (define multiply 
    (lambda (a b)
      (
        (lambda (f a b acc) (f f a b acc))
        (lambda (self a b acc)
          (if b
            (self self a (+ b -1) (+ acc a))
            acc))
        a b 0
      )
    )
  )
  (multiply 6 7)
)
```

The above is roughly equivalent to the following in JavaScript:

```js
const multiply = (a, b) => (
  ((f, a, b, acc) => f(f, a, b, acc))(
    (self, a, b, acc) => (
      b
        ? self(self, a, b + -1, acc + a)
        : acc
    ),
    a, b, 0
  )
)

console.log(multiply(6, 7))
```

## Tasks

Complete the `eval` function in [minlisp.py](minlisp.py) so the supplied doctests pass. Note that an example parse is already provided to translate Lisp programs into [S-expressions](https://en.wikipedia.org/wiki/S-expression) as nested Python lists. The input to eval is an S-expression as native Python lists.

> [!TIP]
> The entire `eval` function can be ~15 lines of code. If you find yourself writing a lot of code, take a step back and consider if there may be a simpler approach.

### Step 1: Atomic Values

Start by handling simple constants.

Example:

```python
>>> eval(1)
1
```

### Step 2: Sequential Evaluation

A list of expressions should be evaluated in order, returning the result of the final expression.

Example:

```python
>>> eval([1, 2, 3])
3
```

### Step 3: Variable Lookup

Expressions can be symbols that refer to values in an [environment](<https://en.wikipedia.org/wiki/Environment_(computer_science)>).

Example:

```python
>>> eval('x', env=[{'x': 1}])
1
```

Note that a stack of scopes can be included and [shadow](https://en.wikipedia.org/wiki/Variable_shadowing) one another.

```python
>>> eval('x', env=[{'x': 2}, {'x': 4}])
2
```

### Step 4: Primitive Function Application

The core of the language is based on function calling using [prefix notation](<https://en.wikipedia.org/wiki/Polish_notation>). The `+` function is already defined in the default global environment. Allow it to be called.

Example:

```python
>>> eval(['+', 1, 1])
2
```

The `+` operator is just a function. Look it up in the current scope and call it, but do not hard-code this specific operation. When the `+` function is not provided, an exception of some kind should be raised.

```python
# Raises exception due to undefined `+`
eval(['+', 1, 1], env=[{}])
```

> [!IMPORTANT]
> There is ambiguity in our Lisp dialect here between a list of expressions and a function to be evaluated. We make the decision to evaluate a function if the first item is a list is callable.

## Step 5: Nested Expressions

The evaluator must handle expressions within expressions.

Example:

```python
>>> eval(['+', 1, ['+', 2, 2]])
5
```

## Step 6: Conditionals

Implement the [`if`](https://www.gnu.org/software/emacs/manual/html_node/elisp/Conditionals.html) [special form](https://www.gnu.org/software/emacs/manual/html_node/elisp/Special-Forms.html) for branching.

> [!NOTE]
> Special forms are generally implemented differently than functions. `if` would generally not be a function defined in the global environment.

Example:

```python
>>> eval(['if', 1, 7, 13])
7
>>> eval(['if', 0, 7, 13])
13
```

In many languages, `if` is not evaluated to return a value. Conceptually, the `if` construct in Lisp closely mirrors the ternary operation from languages like JavaScript:

```js
>>> 1 ? 7 : 13
7
>>> 0 ? 7 : 13
13
```

## Step 7: Anonymous Functions

Introduce the [`lambda`](https://www.gnu.org/software/emacs/manual/html_node/elisp/Lambda-Expressions.html) special form to create [closures](<https://en.wikipedia.org/wiki/Closure_(computer_programming)>).

Example:

```python
>>> eval([['lambda', ['n'], ['+', 'n', 1]], 5])
6
```

## Step 8: Variable Binding

Add the ability to define new variables in the environment via the `define` special form.

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

## Turing Completeness

Despite its simplicity, this language and interpreter are [Turing complete](https://en.wikipedia.org/wiki/Turing_completeness) and support universal computation. Although it lacks explicit looping constructs, it supports arbitrary recursion through both named function bindings via `define` and anonymous self-passing techniques. The provided examples demonstrate that this minimal set of features is sufficient to derive complex logic such as primality testing and the Fibonacci sequence, demonstrating that it can compute complex partial recursive functions.
