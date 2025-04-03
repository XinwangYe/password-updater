# Install dependencies

```bash
> pip install -r requirements.txt
```

# Fill out the accounts.yml and email.yml

```yaml
# accounts.yml
accounts:
  - domain: "domain1"
    username: "username1"
    password: "password1"
    server: "server1"

  - domain: "domain2"
    username: "username2"
    password: "password2"
    server: "server2"
```

```yaml
# email.yml
email:
  port: 25
  server: 'smtp server'
  sender_name: 'your name'
  sender_email: 'your email'
  to_recipient: 'your email'
```

# Run the script

The new password will be generated randomly and saved in the `accounts.yml` file.
Also, the password will be written to the clipboard.

## interactive mode

```bash
> python main.py
```

## arguments mode

```bash
> python main.py --domains domain1 domain2
```

## send email report for both interactive and arguments mode

```bash
> python main.py --send-email
> python main.py --domains domain1 domain2 --send-email
```

# Create a schedule task to run the script every 40 days

## Note: The python.exe need an absolute path, because the task will run in a different context which can't read the environment variables correctly.

If you are using a virtual environment, you need to specify the absolute path to the python.exe in your virtual
environment.

```bash
> schtasks /create /tn "UpdatePassword" /tr "\absolute\path\to\python.exe \absolute\path\to\main.py --domains domain1 domain2 --send-email" /sc daily /mo 40 /st 00:00 /f
```

## Enable "Run task as soon as possible after a scheduled start is missed"

You can manually configure the task so that if it is missed, it will run as soon as possible when the computer is turned
on.

### **Steps:**

1. Open **Task Scheduler** (`taskschd.msc`).
2. Locate your task in the **Task Scheduler Library**.
3. Double-click the task to open its **Properties**.
4. Go to the **Settings** tab.
5. Check the box **"Run task as soon as possible after a scheduled start is missed"**.
6. Click **OK** and save the task.

This ensures that if the computer is off at the scheduled time, the task will run the next time the system starts.