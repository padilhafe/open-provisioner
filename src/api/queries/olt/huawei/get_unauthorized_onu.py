# api/queries/olt/huawei/get_unauthorized_onu.py

from netmiko import ConnectHandler
import re

def parse_autofind_output(output):
    onu_entries = output.strip().split('----------------------------------------------------------------------------')[1:-1]
    results = []

    for entry in onu_entries:
        data = {}
        lines = [line.strip() for line in entry.strip().splitlines() if line.strip()]
        for line in lines:
            if "F/S/P" in line:
                fsp = line.split(":")[1].strip()
                frame, slot, port = map(int, fsp.split("/"))
                data["frame"] = frame
                data["slot"] = slot
                data["port"] = port
            elif "Ont SN" in line:
                raw_sn = line.split(":")[1].strip()
                sn_match = re.search(r'\((.*?)\)', raw_sn)
                data["sn"] = sn_match.group(1) if sn_match else raw_sn
            elif "Password" in line:
                pwd_match = re.search(r'\((.*?)\)', line)
                data["password"] = pwd_match.group(1) if pwd_match else ""
            elif "Loid" in line:
                data["loid"] = line.split(":")[1].strip()
            elif "VendorID" in line:
                data["vendor_id"] = line.split(":")[1].strip()
            elif "Ont Version" in line:
                data["version"] = line.split(":")[1].strip()
            elif "Ont SoftwareVersion" in line:
                data["software_version"] = line.split(":")[1].strip()
            elif "Ont EquipmentID" in line:
                data["equipment_id"] = line.split(":")[1].strip()
            elif "Ont autofind time" in line:
                data["autofind_time"] = line.split(":")[1].strip()

        if data:
            results.append(data)

    return results

def get_unauthorized_onu(mgmt_ipv4: str, device_username: str, device_password: str, device_type: str, port: int = 22):
    try:
        connection = ConnectHandler(
            device_type=device_type,
            host=mgmt_ipv4,
            username=device_username,
            password=device_password,
            port=port
        )
        connection.enable()
        output = connection.send_command("display ont autofind all")
        parsed_data = parse_autofind_output(output)
        connection.disconnect()
        return parsed_data
    except Exception as e:
        raise RuntimeError(f"Erro na conexão ou execução do comando: {e}")
