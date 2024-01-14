**<h1> To start project: </h1>**
**<h2> Create .env file in root dir by .env.example </h2>**
 - **<h3> Open first terminal </h3>**
 - - **<h3> ```alembic upgrade head``` </h3>**
 - - **<h3> ```source .env``` </h3>**
 - - **<h3> ```cd src/api``` </h3>**
 - - **<h3> ```uvicorn main:app``` </h3>**
 - **<h3> Open second terminal </h3>**
 - - **<h3> ```source .env``` </h3>**
 - - **<h3> ```cd src/telegram_bot``` </h3>**
 - - **<h3> ```python main.py``` </h3>**

**<h2> This project provides: </h2>**
 - **<h3> Login by qr code </h3>**
 - **<h3> Send message to another user by telegram bot </h3>**
 - **<h3> Storing and getting this messages </h3>**
 - **<h3> Parsing wildberries.com </h3>**

**<h2> Bot commands: </h2>**
 - **<h3> ```/login 71231231313``` to get qr code </h3>**
 - **<h3> ```/check_login 71231231313``` to get verify status (logined, waiting, error) </h3>**
 - **<h3> ```/send_message @username text``` to send message to another user </h3>**
 - **<h3> ```/get_messages @username``` to get latest 50 messages that addressed to this user </h3>**
 - **<h3> ```wild: product name``` to get first 10 products from wildberries.com </h3>**

**<h2> Web Application enpoints: </h2>**
- **<h3> </h3>**
```
POST /login
request:
{
    "phone": "71231231313"
}
response:
{
    "qr_link_url": "https://host/verify/{token}/{user_id}",
}
```
- **<h3> </h3>**
```
GET /verify/{token}/{user_id}
response:
"OK" // or null
```
- **<h3> </h3>**
```
GET /check/login?phone=71231231313
response:
{
	"status": "waiting_qr_login" // or logined or error
}
```
- **<h3> </h3>**
```
GET /messages?phone=71231231313&uname=chat_username
response:
{
	messages: [
		{
			"username": "",
			"is_self": "false",  //true
			"message_text": ""
		}
	]
}
```
- **<h3> </h3>**
```
POST /messages
request:
{
	"message_text": "Hello world!",
	"from_phone": "71231231313",
	"username": "testname"
}
response:
{
	"status": "ok" // error
}
```

**<h2> Stack </h2>**
- **<h3> FastAPI </h3>**
- **<h3> SQLAlchemy </h3>**
- **<h3> Telethon </h3>**
- **<h3> Selenium </h3>**
