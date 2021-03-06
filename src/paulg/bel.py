# >>> from paulg.bel import *
# >>> bel(list("quote", 1))
# 1

import builtins as py

nil = None
t = "t"
o = "o"

_unset = object()

globe = nil
scope = nil

def id(a, b):
  return a is b

def no(x):
  return id(x, nil) or id(x, False) or (isinstance(x, (py.tuple, py.list)) and not x)

def yes(x):
  return not no(x)

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

map = map2

# (set vmark (join))
vmark = join("vmark")

# (def uvar ()
#   (list vmark))
def uvar(name=_unset):
  return list(vmark)

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

# (def keep (f xs)
#   (if (no xs)      nil
#       (f (car xs)) (cons (car xs) (keep f (cdr xs)))
#                    (keep f (cdr xs))))
def keep(f, xs):
  if no(xs):
    return nil
  elif yes(f(car(xs))):
    return cons(car(xs), keep(f, cdr(xs)))
  else:
    return keep(f, cdr(xs))

# (def rem (x ys (o f =))
#   (keep [no (f _ x)] ys))
def rem(x, ys, f=_unset):
  if f is _unset:
    f = equal
  return keep(lambda _: no(f(_, x)), ys)

# (def get (k kvs (o f =))
#   (find [f (car _) k] kvs))
def get(k, kvs, f=_unset):
  if f is _unset:
    f = equal
  return find(lambda _: f(car(_), k), kvs)

# (def put (k v kvs (o f =))
#   (cons (cons k v)
#         (rem k kvs (fn (x y) (f (car x) y)))))
def put(k, v, kvs, f=_unset):
  if f is _unset:
    f = equal
  return cons(cons(k, v),
              rem(k, kvs, lambda x, y: f(car(x), y)))

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

# (def variable (e)
#   (if (atom e)
#       (no (literal e))
#       (id (car e) vmark)))
def variable(e):
  if atom(e):
    return no(literal(e))
  else:
    return id(car(e), vmark)

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

# (def vref (v a s r m)
#   (let g (cadr m)
#     (if (inwhere s)
#         (aif (or (lookup v a s g)
#                  (and (car (inwhere s))
#                       (let cell (cons v nil)
#                         (xdr g (cons cell (cdr g)))
#                         cell)))
#              (mev (cdr s) (cons (list it 'd) r) m)
#              (sigerr 'unbound s r m))
#         (aif (lookup v a s g)
#              (mev s (cons (cdr it) r) m)
#              (sigerr (list 'unboundb v) s r m)))))
def vref(v, a, s, r, m):
  g = cadr(m)
  if inwhere(s):
    if yes(it := (lookup(v, a, s, g) or
                  (car(inwhere(s)) and
                   (lambda cell: [xdr(g, cons(cell, cdr(g))), g][1],
                     cons(v, nil))))):
      return mev(cdr(s), cons(list(it, "d"), r), m)
    else:
      return sigerr("unbound", s, r, m)
  else:
    if yes(it := lookup(v, a, s, g)):
      return mev(s, cons(cdr(it), r), m)
    else:
      return sigerr(list("unboundb", v), s, r, m)


# (set smark (join))
smark = join("smark")

# (def inwhere (s)
#   (let e (car (car s))
#     (and (begins e (list smark 'loc))
#          (cddr e))))
def inwhere(s):
  e = car(car(s))
  return (begins(e, list(smark, "loc")) and
          cddr(e))

# (def lookup (e a s g)
#   (or (binding e s)
#       (get e a id)
#       (get e g id)
#       (case e
#         scope (cons e a)
#         globe (cons e g))))
def lookup(e, a, s, g):
  return (binding(e, s) or
          get(e, a, id) or
          get(e, g, id) or
          cons(e, a) if id(e, scope) else
          cons(e, g) if id(e, globe) else nil)

# (def binding (v s)
#   (get v
#        (map caddr (keep [begins _ (list smark 'bind) id]
#                         (map car s)))
#        id))
def binding(v, s):
  return get(v,
             map(caddr, keep(lambda _: begins(_, list(smark, "bind"), id),
                             map(car, s))),
             id)


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
  y, s = car(x), cdr(x)
  e, a = car(y), cadr(y)
  if yes(literal(e)):
    return mev(s, cons(e, r), m)
  elif variable(e):
    return vref(e, a, s, r, m)
  elif no(proper(e)):
    return sigerr("malformed", s, r, m)
  elif yes(it := get(car(e), forms, id)):
    return cdr(it)(cdr(e), a, s, r, m)
  else:
    return evcall(e, a, s, r, m)

prims = ("id join xar xdr wrb ops".split(),
         "car cdr type sym nom rdb cls stat sys".split(),
         "coin".split())

def applyprim(f, args, s, r, m):
  if type(f) == "function":
    breakpoint()
    raise NotImplementedError()
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

# (mac fu args
#   `(list (list smark 'fut (fn ,@args)) nil))

# (def evmark (e a s r m)
#   (case (car e)
#     fut  ((cadr e) s r m)
#     bind (mev s r m)
#     loc  (sigerr 'unfindable s r m)
#     prot (mev (cons (list (cadr e) a)
#                     (fu (s r m) (mev s (cdr r) m))
#                     s)
#               r
#               m)
#          (sigerr 'unknown-mark s r m)))
def evmark(e, a, s, r, m):
  x = car(e)
  if x == "fut":
    return cadr(e)(s, r, m)
  elif x == "bind":
    return mev(s, r, m)
  elif x == "loc":
    return sigerr("unfindable", s, r, m)
  elif x == "prot":
    return mev(cons(list(cadr(e), a),
                    fu(list("s", "r", "m"), list("mev", "s", list("cdr", "r"), "m")),
                    s),
               r,
               m)
  else:
    return sigerr("unknown-mark", s, r, m)

# (set forms (list (cons smark evmark)))
forms = list(cons(smark, evmark))

# (mac form (name parms . body)
#   `(set forms (put ',name ,(formfn parms body) forms)))
def form(name, parms, body):
  global forms
  forms = put(name, formfn(parms, body), forms)

# (def formfn (parms body)
#   (with (v  (uvar)
#          w  (uvar)
#          ps (parameters (car parms)))
#     `(fn ,v
#        (eif ,w (apply (fn ,(car parms) (list ,@ps))
#                       (car ,v))
#                (apply sigerr 'bad-form (cddr ,v))
#                (let ,ps ,w
#                  (let ,(cdr parms) (cdr ,v) ,@body))))))
def formfn(parms, body):
  # v = uvar("v")
  # w = uvar("w")
  # ps = parameters(car(parms))
  raise NotImplementedError()

# (def parameters (p)
#   (if (no p)           nil
#       (variable p)     (list p)
#       (atom p)         (err 'bad-parm)
#       (in (car p) t o) (parameters (cadr p))
#                        (append (parameters (car p))
#                                (parameters (cdr p)))))
#
# (form quote ((e) a s r m)
#   (mev s (cons e r) m))
def quote (x, a, s, r, m):
  e = car(x)
  return mev(s, cons(e, r), m)

forms = put("quote", quote, forms)

# (form if (es a s r m)
#   (if (no es)
#       (mev s (cons nil r) m)
#       (mev (cons (list (car es) a)
#                  (if (cdr es)
#                      (cons (fu (s r m)
#                              (if2 (cdr es) a s r m))
#                            s)
#                      s))
#            r
#            m)))

# (def if2 (es a s r m)
#   (mev (cons (list (if (car r)
#                        (car es)
#                        (cons 'if (cdr es)))
#                    a)
#              s)
#        (cdr r)
#        m))


def macro(args, body):
  return list("list", list("quote", "lit"), list("quote", "mac"), list("fn", args, body))

def fu(args, body):
  return list("lit", "mac", list("list", list("list", "smark", list("quote", "fut"), list("fn", args, body)), nil))

# def fu(args, f):
#   return list("lit", "clo", nil, args, list(apply, f, args))

# (def evcall (e a s r m)
#   (mev (cons (list (car e) a)
#              (fu (s r m)
#                (evcall2 (cdr e) a s r m))
#              s)
#        r
#        m))
def evcall(e, a, s, r, m):
  return mev(cons(list(car(e), a),
                  # fu(list("s", "r", "m"),
                  #    lambda s, r, m: evcall2(cdr(e), a, s, r, m)),
                  fu(list("s", "r", "m"),
                     list("evcall2", list("cdr", "e"), "a", "s", "r", "m")),
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
                              #  lambda s, r, m:
                              (lambda args, r2:
                                applyf(op, rev(args), a, s, r2, m))(
                                car(snap(es, r)), cdr(snap(es, r)))),
                              # list("let", list("args", "r2"), list("snap", es, r),
                              #      list("applyf", op, list("rev", args,)))
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
                        # lambda s, r, m:
                        # mev(cons(list(car(r), a), s),
                        #     cdr(r),
                        #     m)
                        list(mev, list(cons, list(list, list(car, r), a, s),
                                       list(cdr, r),
                                       m))
                        ),
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