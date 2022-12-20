# TelBot
A Telegram bot made in python for students of KL University

### Note: 
1. After you have logged in once using this program, you can also login later until a certain period of time without the use of your full password or captcha as this program makes use of session ids which can be used for this purposes.
2. You can get the API_KEY through BotFather in telegram
3. If you don't know your telegram user ID which is a number, 
    1. You can first attempt to use the program (which it won't allow).
    2. After attempting, you can see your user ID in the 'attempts' table of the database 'MainDB'.
    3. Then copy your User ID and place it in the 'Keys' module.
    4. After placing it in the 'Keys' Module, run the following commands in the terminal
        1. `python sqlcreate.py 0` : You don't need to run this if you have already executed it once.
        2. `python sqlcreate.py 1` : You should run this if you have updated your User ID after running the first command.
        
### Steps to use
1. Copy the files in src to your PyCharm Editor
2. Update all the fields in Keys.py file.
    1. API_KEY : Your telegram api key
    2. U_ID : Your telegram user ID
    3. name : How would you like to referred by this program
    4. PATH, RPATh : Your local file directory which you would like to access via telegrm
    5. Driver_Path : Your local chrome driver path
    6. TEST_PATH : A sample local path to test some functionalities. Preferable with different types of files
    7. Student_ID : Your KLU Student ID (10 digit number given by university)
    8. SEMID : 0 if Odd Sem || 1 if Even Sem || 2 if Summer Sem
3. Now, in the terminal run the following commands (Apple)
    1. `python sqlcreate.py 0` - Create a new Database and then create the necessary tables
    2. `python sqlcreate.py 1` - if you did not update your User ID before running the first command
4. Now, run the main.py to start the bot

### Some Basic commands after running the bot (Should be typed in telegram)
1. `/g <KLU_ID> <KLU_Password>` : Login to your ERP
2. `/g logout` : Logout
3. `/g minclasses` : The number of classes that can be skipped while maintaining the required attendance percentage
4. `/g att` : Calculates your total current attendance percentage
5. `/cap <captcha>` : To enter the captcha to login
6. `<upload file directly>` : Just send the file to your bot. The sent file will be stored in your specified directory
7. `/rfile <filename>` : Receive the file from your remote directory
8. `/a lsfs` : List all files in the directory
9. `/a add` <id> - add user
10. `/a rem <id>` - remove user
11. `/a attempts` - list the attempts in console window
12. `/a attemptsls` - send the attemp list to your telegram
13. `/a allusers` - sends the list of users as telegram message
