# Usage Instructions

1. Run pip install -r requiremnts.txt from the root directory of the folder
2. Add your local mysql workbench data to the .env file. (Remember never to push this fille when commiting; git will automatically ignore it but just a precationary reminder).

If you do not have a .env file in the root folder directory: create a file called '.env' & add the following lines into the file (replacing the relevant info):
NB: make sure each variable (HOST, USER, etc.) is placed on a new line in your .env file.

HOST = "YOURHOSTNAME"
USER = "YOURUSERNAME"
PASSWD = "YOURPASSWORD"
DATABASE = "YOURDATABASE --default-- = 'rating'"
3. Execute the code in 'rating_system.sql' in mysql workbench to attain the correct local database that the code will reference.
4. run test_app.py
