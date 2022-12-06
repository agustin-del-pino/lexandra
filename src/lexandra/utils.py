def char_range(start: int, end: int) -> str:
    r = ''
    for i in range(start, end+1):
        r += chr(i) 
    
    return r

__all__ = ["char_range"]