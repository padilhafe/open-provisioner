from app.models.device import Device

# Simulated DB
fake_devices = [
    Device(id=1, name="Huawei00"),
    Device(id=2, name="Huawei01"),
]

def get_all_devices():
    return fake_devices

def get_device_by_id(device_id: int):
    return next((device for device in fake_devices if device.id == device_id), None)
