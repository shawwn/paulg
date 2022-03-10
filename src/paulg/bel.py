import builtins as py

nil = None
t = "t"
o = "o"

_unset = object()

globe = nil
scope = nil

def id(a, b):
  return a is b

def join(a=nil, b=nil):
  return [a] if no(b) else [a, b]

def car(x):
  return x if id(x, nil) else x[0] if len(x) > 0 else nil

def cdr(x):
  return x if id(x, nil) else x[1] if len(x) > 1 else nil

def err(msg, *args):
  raise RuntimeError(msg, *args)

def type(x):
  if isinstance(x, py.list):
    return "pair"
  elif isinstance(x, py.str):
    return "symbol"
  else:
    return py.type(x).__name__
  # else:
  #   raise err("unknown-type", x)

def symbol(x):
  return type(x) == "symbol"

def pair(x):
  return type(x) == "pair"

def proper(x):
  return no(x) or (pair(x) and proper(cdr(x)))

def xar(x, y):
  x[0] = y
  return y

def xdr(x, y):
  x[1] = y
  return y

def sym(x):
  return ''.join(py.list(x))

def nom(x):
  return py.list(py.str(x))

def cadr(x): return car(cdr(x))
def cddr(x): return cdr(cdr(x))
def cdar(x): return cdr(car(x))
def caar(x): return car(car(x))
def caddr(x): return car(cdr(cdr(x)))

def cons(x=nil, y=nil, *args):
  if no(args):
    return join(x, y)
  else:
    return join(x, cons(y, *args))

# (def append args
#   (if (no (cdr args)) (car args)
#       (no (car args)) (apply append (cdr args))
#                       (cons (car (car args))
#                             (apply append (cdr (car args))
#                                           (cdr args)))))
def append2(xs, ys):
  if no(xs):
    return ys
  else:
    return cons(car(xs), append2(cdr(xs), ys))

def append(x, *args):
  if no(args):
    return x
  elif no(x):
    return append(*args)
  else:
    return cons(car(x),
                append(cdr(x),
                       *args))

# (def snoc args
#   (append (car args) (cdr args)))

def snoc(*args):
  args = list(*args)
  return append(car(args), cdr(args))

def list(*args):
  return cons(*args, nil)

# (def map (f . ls)
#   (if (no ls)       nil
#       (some no ls)  nil
#       (no (cdr ls)) (cons (f (car (car ls)))
#                           (map f (cdr (car ls))))
#                     (cons (apply f (map car ls))
#                           (apply map f (map cdr ls)))))

# def map2 (f xs)
#   (if (no xs)
#       nil
#       (cons (f (car xs))
#             (map2 f (cdr xs)))))
def map2(f, xs):
  if no(xs):
    return nil
  else:
    return cons(f(car(xs)),
                map2(f, cdr(xs)))

def apply(f, *args):
  raise NotImplementedError()
  # print('apply', f, args)
  # args = cons(*args)
  # # print('apply', f, args)
  # return f(*iterate(args))

def iterate(x):
  while x is not nil:
    yield car(x)
    x = cdr(x)

def sigerr(v, s, r, m):
  return err(v, s, r, m)

def no(x):
  return id(x, nil) or id(x, False) or (isinstance(x, (py.tuple, py.list)) and not x)

def yes(x):
  return not no(x)

# (def atom (x)
#   (no (id (type x) 'pair)))
def atom(x):
  return no(id(type(x), "pair"))

# (def all (f xs)
#   (if (no xs)      t
#       (f (car xs)) (all f (cdr xs))
#                    nil))
def all(f, xs):
  if no(xs):
    return t
  elif yes(f(car(xs))):
    return all(f, cdr(xs))
  else:
    return nil

# (def some (f xs)
#   (if (no xs)      nil
#       (f (car xs)) xs
#                    (some f (cdr xs))))
def some(f, xs):
  if no(xs):
    return nil
  elif yes(f(car(xs))):
    return xs
  else:
    return some(f, cdr(xs))

# (def reduce (f xs)
#   (if (no (cdr xs))
#       (car xs)
#       (f (car xs) (reduce f (cdr xs)))))
def reduce(f, xs):
  if no(cdr(xs)):
    return car(xs)
  else:
    return f(car(xs), reduce(f, cdr(xs)))

def equal(a, b):
  if pair(a) and pair(b):
    return (equal(car(a), car(b)) and
            equal(cdr(a), cdr(b)))
  else:
    return (a == b) or (no(a) and no(b))

# (def find (f xs)
#   (aif (some f xs) (car it)))
def find(f, xs):
  it = some(f, xs)
  if yes(it):
    return car(it)
  else:
    return nil

# (def begins (xs pat (o f =))
#   (if (no pat)               t
#       (atom xs)              nil
#       (f (car xs) (car pat)) (begins (cdr xs) (cdr pat) f)
#                              nil))
def begins(xs, pat, f=_unset):
  if f is _unset:
    f = equal
  if no(pat):
    return t
  elif atom(xs):
    return nil
  elif yes(f(car(xs), car(pat))):
    return begins(cdr(xs), cdr(pat), f)
  else:
    return nil

def caris(l, x):
  return equal(car(l), x)

# (def rev (xs)
#   (if (no xs)
#       nil
#       (snoc (rev (cdr xs)) (car xs))))
def rev(xs):
  if no(xs):
    return nil
  else:
    return snoc(rev(cdr(xs)), car(xs))

# (def snap (xs ys (o acc))
#   (if (no xs)
#       (list acc ys)
#       (snap (cdr xs) (cdr ys) (snoc acc (car ys)))))
def snap(xs, ys, acc=nil):
  if no(xs):
    return list(acc, ys)
  else:
    return snap(cdr(xs), cdr(ys), snoc(acc, car(ys)))

# (def literal (e)
#   (or (in e t nil o apply)
#       (in (type e) 'char 'stream)
#       (caris e 'lit)
#       (string e)))
def literal(e):
  return (e in [t, nil, o, apply] or
          caris(e, "lit"))

# (def isa (name)
#   [begins _ `(lit ,name) id])
def isa(name):
  return lambda _: begins(_, list("lit", name), id)

# (def bel (e (o g globe))
#   (ev (list (list e nil))
#       nil
#       (list nil g)))
def bel(e, g=_unset):
  if g is _unset:
    g = globe
  return ev(
    list(list(e, nil)),
    nil,
    list(nil, g))

def mev(s, r, m):
  breakpoint()
  p, g = car(m), cadr(m)
  if no(s):
    if yes(p):
      return sched(p, g)
    else:
      return car(r)
  if yes(cdr(binding("lock", s))):
    return sched(cons(list(s, r), p), g)
  else:
    return sched(snoc(p, list(s, r)), g)

# (set smark (join))
#
# (def inwhere (s)
#   (let e (car (car s))
#     (and (begins e (list smark 'loc))
#          (cddr e))))
#
# (def lookup (e a s g)
#   (or (binding e s)
#       (get e a id)
#       (get e g id)
#       (case e
#         scope (cons e a)
#         globe (cons e g))))
#
# (def binding (v s)
#   (get v
#        (map caddr (keep [begins _ (list smark 'bind) id]
#                         (map car s)))
#        id))
def binding(v, s):
  return nil


# (def sched (((s r) . p) g)
#   (ev s r (list p g)))

def sched(x, g):
  x, p = car(x), cdr(x)
  s, r = car(x), cadr(x)
  return ev(s, r, list(p, g))


# (def ev (((e a) . s) r m)
#   (aif (literal e)            (mev s (cons e r) m)
#        (variable e)           (vref e a s r m)
#        (no (proper e))        (sigerr 'malformed s r m)
#        (get (car e) forms id) ((cdr it) (cdr e) a s r m)
#                               (evcall e a s r m)))

def ev(x, r, m):
  e, a, s = car(x), cadr(x), cddr(x)
  breakpoint()
  if yes(literal(e)):
    return mev(s, cons(e, r), m)
  # elif variable(e):
  #   return vref(e, a, s, r, m)
  elif no(proper(e)):
    breakpoint()
    return sigerr("malformed", s, r, m)
  # elif get(car(e), forms, id):
  #   return cdr(it)(cdr(e), a, s, r, m)
  else:
    return evcall(e, a, s, r, m)


prims = ("id join xar xdr wrb ops".split(),
         "car cdr type sym nom rdb cls stat sys".split(),
         "coin".split())

def applyprim(f, args, s, r, m):
  if type(f) == "function":
    breakpoint()
  if any([f in l for l in prims]):
    a = car(args)
    b = cadr(args)
    try:
      if f == 'id':
        v = id(a, b)
      elif f == 'join':
        v = join(a, b)
      elif f == 'car':
        v = car(a)
      elif f == 'cdr':
        v = cdr(a)
      elif f == 'type':
        v = type(a)
      elif f == 'xar':
        v = xar(a, b)
      elif f == 'xdr':
        v = xdr(a, b)
      elif f == 'sym':
        v = sym(a)
      elif f == 'nom':
        v = nom(a)
      return mev(s, cons(v, r), m)
    except Exception as v:
      return sigerr(v, s, r, m)
  else:
    return sigerr("unknown-prim", s, r, m)

def fu(args, f):
  return list("lit", "clo", nil, args, list(apply, f, args))

# (def evcall (e a s r m)
#   (mev (cons (list (car e) a)
#              (fu (s r m)
#                (evcall2 (cdr e) a s r m))
#              s)
#        r
#        m))
def evcall(e, a, s, r, m):
  breakpoint()
  return mev(cons(list(car(e), a),
                  fu(list("s", "r", "m"),
                     lambda s, r, m: evcall2(cdr(e), a, s, r, m)),
                  s),
             r,
             m)

# (def evcall2 (es a s (op . r) m)
#   (if ((isa 'mac) op)
#       (applym op es a s r m)
#       (mev (append (map [list _ a] es)
#                    (cons (fu (s r m)
#                            (let (args r2) (snap es r)
#                              (applyf op (rev args) a s r2 m)))
#                          s))
#            r
#            m)))

def evcall2(es, a,  s, x, m):
  op, r = car(x), cdr(x)
  breakpoint()
  if isa("mac")(op):
    return applym(op, es, a, s, r, m)
  else:
    return mev(append(map(lambda _: list(_, a), es),
                      cons(fu(list("s", "r", "m"),
                               lambda s, r, m:
                              (lambda args, r2:
                                applyf(op, rev(args), a, s, r2, m))(
                                car(snap(es, r)), cdr(snap(es, r)))),
                           s)),
               r,
               m)

# (def applym (mac args a s r m)
#   (applyf (caddr mac)
#           args
#           a
#           (cons (fu (s r m)
#                   (mev (cons (list (car r) a) s)
#                        (cdr r)
#                        m))
#                 s)
#           r
#           m))

def applym(mac, args, a, s, r, m):
  return applyf(caddr(mac),
                args,
                a,
                cons(fu(list("s", "r", "m"),
                        lambda s, r, m:
                        mev(cons(list(car(r), a), s),
                            cdr(r),
                            m)),
                     s),
                r,
                m)

# (def applyf (f args a s r m)
#   (if (= f apply)    (applyf (car args) (reduce join (cdr args)) a s r m)
#       (caris f 'lit) (if (proper f)
#                          (applylit f args a s r m)
#                          (sigerr 'bad-lit s r m))
#                      (sigerr 'cannot-apply s r m)))
def applyf(f, args, a, s, r, m):
  breakpoint()
  if equal(f, apply):
    return applyf(car(args), reduce(join, cdr(args)), a, s, r, m)
  elif caris(f, "lit"):
    if proper(f):
      return applylit(f, args, a, s, r, m)
    else:
      return sigerr("bad-lit", s, r, m)
  else:
    return sigerr("cannot-apply", s, r, m)


# (def applylit (f args a s r m)
#   (aif (and (inwhere s) (find [(car _) f] locfns))
#        ((cadr it) f args a s r m)
#        (let (tag . rest) (cdr f)
#          (case tag
#            prim (applyprim (car rest) args s r m)
#            clo  (let ((o env) (o parms) (o body) . extra) rest
#                   (if (and (okenv env) (okparms parms))
#                       (applyclo parms args env body s r m)
#                       (sigerr 'bad-clo s r m)))
#            mac  (applym f (map [list 'quote _] args) a s r m)
#            cont (let ((o s2) (o r2) . extra) rest
#                   (if (and (okstack s2) (proper r2))
#                       (applycont s2 r2 args s r m)
#                       (sigerr 'bad-cont s r m)))
#                 (aif (get tag virfns)
#                      (let e ((cdr it) f (map [list 'quote _] args))
#                        (mev (cons (list e a) s) r m))
#                      (sigerr 'unapplyable s r m))))))
def applylit(f, args, a, s, r, m):
  breakpoint()
  x = cdr(f)
  tag, rest = car(x), cdr(x)
  if tag == "prim":
    return applyprim(car(rest), args, s, r, m)
  elif tag == "clo":
    raise NotImplementedError()
  elif tag == "mac":
    return applym(f, map(lambda _: list("quote", _), args), a, s, r, m)
  elif tag == "cont":
    raise NotImplementedError()
  else:
    return sigerr("unapplyable", s, r, m)