import argparse
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pyperclip
from ruamel.yaml import YAML

from emails import Email
from password_generator import generate_win_password
from password_updater import update_password

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)


def load_accounts():
    """Load accounts from the YAML file."""
    yaml_path = Path(__file__).parent / 'accounts.yml'
    with open(yaml_path, 'r') as f:
        return yaml.load(f)


def save_accounts(accounts_data):
    """Save updated accounts back to YAML file."""
    yaml_path = Path(__file__).parent / 'accounts.yml'
    with open(yaml_path, 'w') as f:
        yaml.dump(accounts_data, f)


def read_email_config():
    yaml_path = Path(__file__).parent / 'email.yml'
    with open(yaml_path, 'r') as f:
        return yaml.load(f)


def attempt_password_update(account):
    """Update password for a single account."""
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
        return True, None
    return False, result


def update_domain_account_password(target_domain=None):
    """Main function to handle account password updates."""
    if not target_domain:
        print("No domain provided. Skipping password updates.")
        return

    accounts_data = load_accounts()
    updated = False

    for account in accounts_data['accounts']:
        if account['domain'] == target_domain:
            print(f"Updating password for {account['username']} on {account['domain']}...")
            success, error = attempt_password_update(account)
            if success:
                print("Password updated successfully")
                updated = True
            else:
                print(f"Failed to update password: {error}")

    if updated:
        save_accounts(accounts_data)
        print("Changes saved to accounts file")
    else:
        if not any(account['domain'] == target_domain for account in accounts_data['accounts']):
            print(f"Domain not found: {target_domain}")
        else:
            print("No passwords were updated due to errors")


def run_with_interactive_mode():
    domains = [account['domain'] for account in load_accounts()['accounts']]
    print("\nAvailable domains:")
    for idx, domain in enumerate(domains, 1):
        print(f"{idx}. {domain}")
    while True:
        try:
            choice = int(input("\nSelect domain number (or 0 to exit): "))
            if choice == 0:
                sys.exit(0)
            if 1 <= choice <= len(domains):
                update_domain_account_password(domains[choice - 1])
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def run_with_arguments_mode(domains):
    for domain in domains:
        update_domain_account_password(domain)


def capture_output(func, *args, **kwargs):
    with redirect_stdout(buffer := io.StringIO()):
        ret = func(*args, **kwargs)
    return ret, buffer.getvalue()


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Password Updater.')
    parser.add_argument('--send-email', action='store_true', default=False, help='Send email report')
    parser.add_argument('--domains', nargs='+', help='List of domain to update passwords for')
    return parser.parse_args()


def setup_email_client():
    email_config = read_email_config()['email']
    return Email(
        port=email_config['port'],
        server=email_config['server'],
        sender_name=email_config['sender_name'],
        sender_email=email_config['sender_email'],
        to_recipients=[email_config['to_recipient']],
        cc_recipients=[]
    )


def update_password_and_generate_report(args):
    if args.domains:
        _, report = capture_output(run_with_arguments_mode, domains=args.domains)
    else:
        _, report = capture_output(run_with_interactive_mode)

    yaml.dump(load_accounts(), stream := io.StringIO())
    return f"Report:\n{report}\n\nAccounts updated:\n{stream.getvalue()}"


def update_password_and_send_report(args):
    email = setup_email_client()
    report_content = update_password_and_generate_report(args)
    email.send_email(
        subject="Password Update Report",
        content=report_content
    )


def handle_password_updates(args):
    if args.domains:
        run_with_arguments_mode(domains=args.domains)
    else:
        run_with_interactive_mode()


def main():
    args = parse_command_line_arguments()

    if args.send_email:
        update_password_and_send_report(args)
    else:
        handle_password_updates(args)


if __name__ == '__main__':
    main()
