import difflib
import warnings
import os


class ChangeDetected(Exception):
    pass

def track_delta(file_name, string):
    data = None

    try:
        with open(file_name, 'r') as f:
            data = f.read()
    except IOError:
        # file not found
        with open(file_name, 'w') as f:
            f.write(string)
            warnings.warn('New test case: {}'.format(file_name))
        return    
    
    new_file_name = file_name + '.new'

    diff = list(difflib.unified_diff(
        data.strip().splitlines(), 
        string.strip().splitlines(), 
        fromfile=file_name, 
        tofile=new_file_name,
        lineterm=''
        ))
    
    if len(diff) == 0:
        #they are the same
        try:
            os.remove(new_file_name)
        except OSError:
            pass
        return

    with open(new_file_name, 'w') as f:
        f.write(string)

    raise ChangeDetected('\n'*2 + '\n'.join(diff))
    