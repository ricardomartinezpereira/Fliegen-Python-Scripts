
## Send Mails Script:

This script can send mails to email addresses, the email addresses to send the message to must be specify in `./emails.csv` file, 
the message to be sent can be either text plain or html content, it also allows to send files attached with the mails. If 
you want to send html content with the mail modify the `./html_content.html` file.


### Modify config.json:

Before run the script you must modify the `./config.json` file, you must specify the host, port, username and password
of the smtp server.


### Install Required Packages:

```Python
pip install -r requirements.txt
```

### Execute Script:

```Python
python main.py
```
