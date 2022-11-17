from .index import index, get

def empty():
  return []

def tree (all, indexer, maker, root = None):
  mem = index(all, indexer)

  def many(all):
    return list(map(one, all))

  def one(single):
    return maker(single, lambda r: many(get(mem, r, empty())))

  return many(get(mem, root))
