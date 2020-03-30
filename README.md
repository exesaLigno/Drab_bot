# DREC DRAB chat bot

## Using
Chatbot receiving messages in public dialogues and trying to search similar question in database.
If question not found in database, bot forwards question to moderators chat.

* To answer question, moderator must **reply to forwarded question**. Answer will be forwarded to enrolee and added to database.
* If question inappropriate, moderator can reply with text **"/ignore"** and question will be ignored.

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
First of all you need make database file like that **(symbols '<', '>' are required!)**. You can add Q&A couples and facts.
```
Q: <question>
A: <answer>

Q: ...

FACT: <fact>
FACT: ...
```
After that you need to configure *bot_settings.txt* **(without '<', '>')**
```
public_id = <public id (without word 'public', just number)>
token = <public token>
moderators_chat_id = <id of modeators chat>
database_file = <name of database file>
accept_level = <level of coincedence of strings to consider them the same (float number between 0 and 1)>
```

### Getting data for configurating
#### Token
You need to open public settings (section "Work with API") and push button "Create key".
After that you need to enable access to *public messages* in list below. The string you will receive is token.
![alt-текст][token1]
![alt-текст][token2]


#### Setting up public API
At the same section you need to choose tab *"Long Poll API"* and on this tab choose
```
Long Poll API: Enabled
API version: 5.103
```
![alt-текст][longpoll1]

In subsection named "Event types" you need to choose all points you need. 
Recommended to select *"Incoming messages"* and *"Outgoing messages"* 
(If you have another chat bot, you need to mark also points required for this bot)
![alt-текст][longpoll2]

#### Searching for moderators chat ID
ID of moderators chat is number is equal to the ordinal number in which the chat bot was added to the conversation.
You can find it randomly (Starting from 1 and increasing it until it works)

#### Accept level
It is the float number between 0 and 1. If strings much more than accept level, they are considered matching.

[token1]: https://github.com/exesaLigno/Drab_bot/blob/master/README_pictures/token1.png "Create key"
[token2]: https://github.com/exesaLigno/Drab_bot/blob/master/README_pictures/token2.png "Allow access to public messages"
[longpoll1]: https://github.com/exesaLigno/Drab_bot/blob/master/README_pictures/longpoll1.png "Configurating Long Poll"
[longpoll2]: https://github.com/exesaLigno/Drab_bot/blob/master/README_pictures/longpoll2.png "Configurating Long Poll event types"



