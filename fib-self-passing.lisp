((lambda (f n)
  (f f n 0 1))
 (lambda (self count cur next)
  (if count
   (self self (+ count -1) next (+ cur next))
   cur))
 10)