def parse(program):
    """
    Parses a Lisp string into nested Pythons lists for the eval function.

    >>> parse('1')
    1
    >>> parse('(+ 1 1)')
    ['+', 1, 1]
    >>> parse('(+ 1 (+ 2 2))')
    ['+', 1, ['+', 2, 2]]

    >>> eval(parse('''((lambda (f n)
    ...   (f f n 0 1))
    ...  (lambda (self count cur next)
    ...   (if count
    ...    (self self (+ count -1) next (+ cur next))
    ...     cur))
    ...  10)
    ...  '''))
    55
    >>> eval(parse('(+ 1 (+ 2 2))'))
    5
    >>> eval(parse('((lambda (n) (+ n n)) 2)'))
    4
    >>> eval(parse('(+ 1 (+ 2 2))'))
    5
    >>> eval(parse('((lambda (n) (+ n n)) 2)'))
    4
    """
    tokens = program.replace("(", " ( ").replace(")", " ) ").split()

    def read_from_tokens(tokens):
        if not tokens:
            return None
        token = tokens.pop(0)
        if token == "(":
            lst = []
            while tokens[0] != ")":
                lst.append(read_from_tokens(tokens))
            tokens.pop(0)
            return lst
        try:
            return int(token)
        except ValueError:
            return token

    return read_from_tokens(tokens)


def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    Literal values are returned.

    >>> eval(1)
    1

    Sequences of values return the last value.

    >>> eval([1, 2, 3])
    3

    Variables can be accessed from the supplied `env`.

    >>> eval('x', env=[{'x': 1}])
    1

    Nested scopes shadow values

    >>> eval('x', env=[{'x': 2}, {'x': 4}])
    2

    Function evaluation uses prefix notation.

    `+` is provided as a function in the default global `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5

    Be sure that `+` is accessed from the passed environment.

    >>> eval(['+', 1, 1], env=[{'+': lambda a, b: 42}])
    42

    Sequences of expressions return the value of the last expression

    >>> eval([['+', 1, 1], ['+', 2, 2]])
    4

    Nested subexpressions are properly evaluated

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    `lambda` creates anonymous functions

    >>> eval([['lambda', ['n'], ['+', 'n', 'n']], 2])
    4

    `if` provides a ternary operator with short-circuit evaluation

    >>> eval(['if', 1, 2, 3])
    2

    >>> eval(['if', 0, 2, 3])
    3

    Make sure that only the branch taken is evaluated

    >>> eval(['if', 1, 2, ['square', 1]])
    2

    `define` binds a value to a name in the current scope

    >>> eval([['define', 'x', 2], 'x'])
    2

    >>> eval([['define', 'a', 5], ['define', 'b', 10], ['+', 'a', 'b']])
    15

    >>> eval([['define', 'y', 1], ['define', 'y', 2], 'y'])
    2

    >>> eval([['define', 'z', ['+', 1, 2]], 'z'])
    3

    n-th Fibonacci computation using self-passing

    >>> eval([
    ...   ['lambda', ['f', 'n'], ['f', 'f', 'n', 0, 1]],
    ...   ['lambda', ['self', 'count', 'cur', 'next'],
    ...     ['if', 'count',
    ...       ['self', 'self', ['+', 'count', -1], 'next', ['+', 'cur', 'next']],
    ...        'cur'],
    ...   ], 10
    ... ])
    55

    n-th Fibonacci computation using `define`

    >>> eval([
    ...   ['define', 'fib',
    ...     ['lambda', ['n'],
    ...       ['if', ['+', 'n', -1],
    ...         ['if', ['+', 'n', -2],
    ...           ['+', ['fib', ['+', 'n', -1]], ['fib', ['+', 'n', -2]]],
    ...           1],
    ...         1]]],
    ...   ['fib', 10]
    ... ])
    55

    20th prime number

    >>> eval(parse('''
    ... (
    ...   (define not (lambda (x) (if x 0 1)))
    ...   (define dec (lambda (n) (+ n -1)))
    ...   (define sub (lambda (a b) (if b (sub (dec a) (dec b)) a)))
    ...   (define lt (lambda (a b) (if b (if a (lt (dec a) (dec b)) 1) 0)))
    ...   (define div (lambda (a b) (if (lt a b) 0 (+ 1 (div (sub a b) b)))))
    ...   (define mod (lambda (a b) (if (lt a b) a (mod (sub a b) b))))
    ...   (define has-divisor (lambda (n d) (if (lt d 2) 0 (if (mod n d) (has-divisor n (dec d)) 1))))
    ...   (define is-prime (lambda (n) (if (lt n 2) 0 (if (lt n 4) 1 (not (has-divisor n (div n 2)))))))
    ...   (define find (lambda (count n) (if (is-prime n) (if (dec count) (find (dec count) (+ n 1)) n) (find count (+ n 1)))))
    ...   (find 20 2)
    ... )
    ... '''))
    71
    """
    pass


if __name__ == "__main__":
    import sys
    import doctest

    failed, _ = doctest.testmod()

    if failed == 0 and len(sys.argv) > 1:
        sexp = parse(open(sys.argv[1]).read())
        print(eval(sexp))
