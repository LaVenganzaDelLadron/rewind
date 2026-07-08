from utils.banner import randomizer
from utils.version import version

def show_help():
    randomizer()
    print("""
    Rewind - Linux Time Machine
    
    Usage:
        rewind today
        rewind help 
""")
    version()