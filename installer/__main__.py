import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from installer.main import ArchTUI

if __name__ == "__main__":
    app = ArchTUI()
    app.run()