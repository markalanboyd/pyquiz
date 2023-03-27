from pyquiz_app.cli.pyquizcli import pyquizcli as cli
from pyquiz_app.opentriviadb import opentriviadb as ot

def main():
    ot.main_test()
    cli.hello_world()

if __name__ == "__main__":
    main()
    