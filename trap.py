def trap(func, args):
    try:
        return (0, func(*args))
    except Exception as e:
        return (1, e)
