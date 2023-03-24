# pyenv activate pyquiz-3.11.2
import eel
import opentriviadb as ot


# Global constants


# Global variables
token = ot.request_token()


# Functions
def main():
    """Main function."""
    
    # questions = ot.request_questions(token, 
    #                            ``      category=category, 
    #                                  amount=2)
    # ot.main_test(questions)
    
    eel.init('web')
    
    
    
    eel.start('index.html', size=(800, 600))

if __name__ == '__main__':
    main()