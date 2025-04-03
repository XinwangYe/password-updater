from urllib.parse import urlparse, parse_qs

import requests
import urllib3


def get_result_from_location(location):
    parsed = urlparse(location)
    query_params = parse_qs(parsed.query)
    return query_params.get('Error', [None])[0]


def update_password(server, domain_username, password, new_password):
    data = {
        "DomainUserName": domain_username,
        "UserPass": password,
        "NewUserPass": new_password,
        "ConfirmNewUserPass": new_password
    }

    url = f"https://{server}/RDWeb/Pages/en-US/password.aspx"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    resp = requests.post(url, data=data, verify=False, allow_redirects=False)
    return get_result_from_location(resp.headers["Location"])
