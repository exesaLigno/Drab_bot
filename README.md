# DREC DRAB chat bot_longpoll

## Using
Chatbot receiving messages in public dialogues and trying to search similar question in database.
If question not found in database, bot forwards question to moderators chat.

* To answer question, moderator must **reply to forwarded question**. Answer will be forwarded to enrolee and added to database.
* If question inappropriate, moderator can reply with text **"/ignore"** and question will be ignored.
* Also moderator can get .txt file with database with command **"/getdb"** and send new database file with command **"/setdb"** with attached .txt file with questions.

## Setting up

### Installing
To install required libraries you just need to write command
```
pip3 install -r requirements.txt
```
And start bot with command in directory with bot
```
python3 bot.py
```
Or you can use chatbot manager **(NOT IMPLEMENTED)**

### Configurating bot
First of all you need make database file like that (without '<', '>')
```
Q: <question>
A: <answer>

Q: ....
```
After that you need to configure *bot_settings.txt* (without '<', '>')
```
public_id = <public id (without word 'public', just number)>
token = <public token>
moderators_chat_id = <id of modeators chat>
database_file = <name of database file>
accept_level = <level of coincedence of strings to consider them the same (float number between 0 and 1)>
```

### Gedding data for configurating
#### Token
You need to open public settings (section "Work with API") and push button "Create key".
After that you need to mark all points in list below. The string you will receive is token.

#### Setting up public API
At the same section you need to choose tab *"Long Poll API"* and on this tab choose
```
Long Poll API: Enabled
API version: 5.103
```

In subsection named "Event types" you need to choose all points you need (Recommended to select all)

#### Searching for moderators chat ID
ID of moderators chat is number is equal to the ordinal number in which the chat bot was added to the conversation.
You can find it randomly (Starting from 1 and increasing it until it works)

#### Accept level
It is the float number between 0 and 1. If strings much more than accept level, they are considered matching.





