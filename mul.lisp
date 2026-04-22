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
