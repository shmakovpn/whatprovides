"""
whatprovides build_package.py

This script runs 'python setup.py sdist'
"""
import os
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))


def run_setup():
    os.chdir(SCRIPT_DIR)
    os.system('python setup.py sdist')
    print('__END__')


if __name__ == '__main__':
    run_setup()
