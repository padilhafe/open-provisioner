import requests
import api.queries.utils.open_bmc_api_session as open_bmc_api_session

def power_actions(device, action):
    token, session_location = open_bmc_api_session.login(device.device_mgmt_ipv4, device.device_username, device.device_password)
    url = f"https://{device.device_mgmt_ipv4}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
    payload = { "ResetType": action }
    header = { "X-Auth-Token": token }

    try:
        response = requests.post(url, json=payload, headers=header, verify=False)
        response.raise_for_status()
        open_bmc_api_session.logout(device.device_mgmt_ipv4, token, session_location)
        return response.json()

    except requests.exceptions.RequestException as e:
        open_bmc_api_session.logout(device.device_mgmt_ipv4, token, session_location)
        print(f"{{ error: {e} }}")
        return None

