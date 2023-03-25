# pyenv activate pyquiz-3.11.2
import eel
import opentriviadb as ot


# Global variables
token = ot.request_token()


# Functions
def main():
    """Main function."""
    eel.init('web')
    
    # Code Goes Here

    eel.start('index.html', size=(800, 600))

if __name__ == '__main__':
    main()