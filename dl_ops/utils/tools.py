import os

def increment_version(s):
    f = ''
    start = False
    for idx, i in enumerate(reversed(s)):
        if i.isdigit():
            f = i + f
            
            if not start:
                end_idx = idx
                
            start = True

        
        if not i.isdigit() and start:
            start_idx = idx
            break
    
    inc = int(f) + 1
    new_s = s[:-start_idx] + f'{inc:0{len(f)}d}'
    new_s = new_s + s[-end_idx:]  if end_idx > 0 else new_s
    
    return new_s


               
      