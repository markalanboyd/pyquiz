import opentriviadb as ot


# Global constants


# Global variables
token = ot.request_token()
category = None

# Functions
def main():
    """Main function."""
    
    questions = ot.request_questions(token, 
                                     category=category, 
                                     amount=2)
    ot.main_test(questions)


if __name__ == '__main__':
    main()