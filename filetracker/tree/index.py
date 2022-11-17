from functools import reduce

def empty():
  return {}

def update(t, k, f):
  if k in t:
    return { **t, k: f(get(t, k)) }
  else:
    return { **t, k: f() }

def get(t, k, default = None):
  if k in t:
    return t[k]
  else:
    return default

def append(t, k, v):
  return update(t, k, lambda r = []: [ *r, v ])

def index(ls, indexer):
  return reduce \
    ( lambda t, v: append(t, indexer(v), v)
    , ls
    , empty()
    )
