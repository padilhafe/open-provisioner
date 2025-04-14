import re
from netmiko import ConnectHandler

def get_users(device_mgmt_ipv4: str, device_username: str, device_password: str, device_type: str, port: int = 22):
    try:
        connection = ConnectHandler(
            device_type=device_type,
            host=device_mgmt_ipv4,
            username=device_username,
            password=device_password,
            port=port
        )
        connection.enable()
        output = connection.send_command("display local-user")
        connection.disconnect()

        # Regex para capturar nomes de usuário válidos
        user_pattern = re.compile(r'^\s*([a-zA-Z0-9_]+)\s+[A-Z]\s+', re.MULTILINE)
        users = user_pattern.findall(output)
        
        return users

    except Exception as e:
        raise RuntimeError(f"Erro na conexão ou execução do comando: {e}")
