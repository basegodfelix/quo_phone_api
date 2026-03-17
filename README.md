# quo_phone_api

# Description
quo_phone_api is simple Python bindings for Quo Phone REST API.
The purpose of this library is to create simplified, pythonic bindings for this API.

Keep in mind the methods accept all common number formats used in the US.
(xxx) xxx-xxxx, xxx.xxx.xxxx, xxx-xxx-xxxx are all accepted.

Please keep in mind, this is not meant to be an exhaustive library but a
functional library that gives us the core functions of the REST API
provided to us by Quo, so that we can integrate phones with automated systems.

## Contact
BaseGodFelix - felixmobile87@gmail.com

## Dependencies
felog
requests
## Installation
```
pip install quo_phone_api
```
# Usage
## Setup a Phone
```
import quo_phone_api.core as Quo


quo = Quo.Phone(<Quo API Key>)
quo.connect()

```
## Get Conversations
The way Quo API works allows you to list conversations between your phone and others.
These conversations can be enumerated to see open conversations for CRM purposes.

The documentation for this method says that technically its possible to filter
the results of this method but when I try to provide the necessary phoneNumbers
field, it throws errors. Their API may be having some sort of issues, we will return
to the filtering functionality.

**Note:** This method does not require you connect the phone but it is good practice.

### Return
This method returns a list of dictionaries with the results.
Error messages will be index 0 and have a dictionary key of 'error'.

### Method Usage
```
import quo_phone_api.core as Quo


quo = Quo.Phone(<Quo API Key>)
quo.connect()
conversations = quo.get_conversations()
```
## Get Messages
This method retrieves all text messages from a specific number.

### Return
This method returns a list of dictionaries with the results.
Error messages will be index 0 and have a dictionary key of 'error'.

### Method Usage
```
import quo_phone_api.core as Quo


quo = Quo.Phone(<Quo API Key>)
quo.connect()
messages = quo.get_messages('(xxx) xxx-xxxx')

```
## Get Calls
This method retrieves all calls from a specific number.

### Return
This method returns a list of dictionaries with the results.
Error messages will be index 0 and have a dictionary key of 'error'.

### Method Usage
```
import quo_phone_api.core as Quo


quo = Quo.Phone(<Quo API Key>)
quo.connect()
calls = quo.get_calls('(xxx) xxx-xxxx')

```
## Send a text message
This method sends text messages to a specific number.
**Note:** As per Quo, the text has to be between 1-1600 characters in length.

### Return
This method returns a dictionary with the results.
Error messages will have a dictionary key of 'error'.

### Method Usage
```
import quo_phone_api.core as Quo


quo = Quo.Phone(<Quo API Key>)
quo.connect()
sent = quo.send_message('(xxx) xxx-xxxx',<MESSAGE BODY>)

```