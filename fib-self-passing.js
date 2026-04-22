console.log(

((f, n) => f(f, n, 0, 1))(
  (self, count, cur, next) => 
    count == 0 ? cur : self(self, count-1, next, cur+next)
  , 10)

)