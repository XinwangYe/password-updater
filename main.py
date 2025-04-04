import argparse
from contextlib import redirect_stdout
from io import StringIO
from typing import TextIO, cast

import pyperclip

from capture_input_output import TeeOutput, TeeInput, redirect_stdin
from emails import Email
from password_generator import generate_win_password
from password_updater import update_password
from yaml import load_yaml, dump_yaml, dump_to_stream


def update_password_for_account(account):
    new_password = generate_win_password()
    result = update_password(
        server=account['server'],
        domain_username=rf'{account["domain"]}\{account["username"]}',
        password=account['password'],
        new_password=new_password
    )

    if result == 'PasswordSuccess':
        pyperclip.copy(new_password)
        account['password'] = new_password
        return None
    return result


def process_domain_update(target_domain):
    if not target_domain:
        print("No domain provided. Skipping password updates.")
        return

    accounts = load_yaml('accounts.yml')
    updated = False

    for account in accounts['accounts']:
        if account['domain'] == target_domain:
            print(f"Updating password for {account['username']} on {account['domain']}...")
            error = update_password_for_account(account)
            if not error:
                print("Password updated successfully")
                updated = True
            else:
                print(f"Failed to update password: {error}")

    if updated:
        dump_yaml(accounts, 'accounts.yml')
        print("Changes saved to accounts file")


def interactive_mode():
    accounts = load_yaml('accounts.yml')
    domains = [account['domain'] for account in accounts['accounts']]

    print("\nAvailable domains:")
    for idx, domain in enumerate(domains, 1):
        print(f"{idx}. {domain}")

    while True:
        try:
            choice = int(input("\nSelect domain number (or 0 to exit): "))
            if choice == 0:
                return False
            if 1 <= choice <= len(domains):
                process_domain_update(domains[choice - 1])
                return True
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def send_email_report(domains=None):
    buffer = StringIO()
    with redirect_stdout(cast(TextIO, TeeOutput(buffer))), redirect_stdin(TeeInput(buffer)):
        if domains:
            for domain in domains:
                process_domain_update(domain)
            should_send = True
        else:
            should_send = interactive_mode()

    if not should_send:
        print("No changes made. No email will be sent.")
        return

    email_config = load_yaml('email.yml')['email']
    email = Email(
        port=email_config['port'],
        server=email_config['server'],
        sender_name=email_config['sender_name'],
        sender_email=email_config['sender_email'],
        to_recipients=[email_config['to_recipient']],
        cc_recipients=[]
    )

    dump_to_stream(load_yaml('accounts.yml'), stream := StringIO())
    report = f"Report:\n{buffer.getvalue()}\n\nAccounts updated:\n{stream.getvalue()}"
    email.send_email(subject="Password Update Report", content=report)


def main():
    parser = argparse.ArgumentParser(description='Password Updater.')
    parser.add_argument('--send-email', action='store_true', help='Send email report')
    parser.add_argument('--domains', nargs='+', metavar='DOMAIN', help='List of domain to update passwords for')
    args = parser.parse_args()

    if args.send_email:
        send_email_report(args.domains)
    else:
        if args.domains:
            for domain in args.domains:
                process_domain_update(domain)
        else:
            interactive_mode()


if __name__ == '__main__':
    main()
