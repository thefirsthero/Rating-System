# Usage Instructions

1. Run pip install -r requiremnts.txt from the root directory of the folder
2. Add your local mysql workbench data to the .env file. (Remember never to push this fille when commiting; git will automatically ignore it but just a precationary reminder).

If you do not have a .env file in the root folder directory: create a file called '.env' & add the following lines into the file (replacing the relevant info):

HOST = "YOURHOSTNAME"
USER = "YOURUSERNAME"
PASSWD = "YOURPASSWORD"
DATABASE = "YOURDATABASE"

3. run test_app.py