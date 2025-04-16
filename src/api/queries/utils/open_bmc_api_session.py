import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login(bmc_address, username, password):
    url = f"https://{bmc_address}/redfish/v1/SessionService/Sessions"
    payload = {
        "UserName": username,
        "Password": password
    }

    try:
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()

        return response.headers.get("X-Auth-Token"), response.headers.get("Location")

    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha no login: {e}")
        return None, None

def logout(bmc_address, token, location):
    url = f"https://{bmc_address}{location}"
    header = {
        "X-Auth-Token": token
    }

    try:
        response = requests.delete(url, headers=header, verify=False)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha no logout: {e}")
        return None, None
