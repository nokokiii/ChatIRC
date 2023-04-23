# Application Name: IRC Chat

**Description:**
IRC (Internet Relay Chat) is an internet protocol that enables real-time communication. IRC Chat is an application that allows users to connect to IRC servers and participate in chat rooms.

**Features:**
- Join and participate in multiple chat rooms
- Create your own private chat rooms
- Customize your client preferences, such 4 different themes

**Usage:**
- Open the IRC Chat application.
- Use the HELLO command to enter your nickname and then join your first channel with JOIN.
- Start chatting!

**Contributing:**
If you'd like to contribute to IRC Chat, please submit a pull request on GitHub.

**License:**
IRC Chat is licensed under the MIT License.

 **Command scheme and list:**
- HELLO|{NickName} - should be your first command
- CREATE|{ChannelName}|{Password}|{MaxUsers} - creates channel
- JOIN|#{ChannelName} - Joins a channel
- QUIT - Leaves the program
- LIST - Prints out the list of available channels
- HELP - Shows the list of commands
- GET - Shows you the last 10 messages of the channel or less 
- MESS|{Message} - Writes a message
- THEME|{ThemeName} - Selecting themes
- THEMELIST - Gives you the list of themes

**Error Codes**
- Error 0: Invalid command
- Error 1: Invalid arguments
- Error 2: You have to be logged to use this command
- Error 3: You are already logged in
- Error 4: You have to be in chat to use this command
- Error 5: You are already in chat
- Error 6: No such chat
- Error 7: Password is incorrect
- Error 8: The channel name is invalid
- Error 9: The channel already exists
- Error 10: The channel is full
- Error 12: There is no such a theme

**Libraries used:**
- threading
- socket
-  datetime

**Authors:**
- Nokokiii 
- Mundek
