const multiply = ((a, b) => (
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