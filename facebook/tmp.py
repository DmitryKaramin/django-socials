def tracer(func): calls = 0
    def wrapper(*args, **kwargs):
        nonlocal calls
# State via enclosing scope and nonlocal # Instead of class attrs or global
# calls is per-function, not global
        calls += 1
        print('call %s to %s' % (calls, func.__name__)) return func(*args, **kwargs)
        return wrapper