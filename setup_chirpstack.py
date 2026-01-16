import requests

# Update these variables with your ChirpStack instance details
CHIRPSTACK_URL = "https://scomm.southerneleven.com/api"
API_TOKEN      = "<your-api-key-here>"  # create an API key in ChirpStack UI and paste it here

HEADERS = {
    "Grpc-Metadata-Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def create_tenant(name, description="", max_gateway_count=5, max_device_count=5,
                  private_gateways_up=True, private_gateways_down=True):
    url = f"{CHIRPSTACK_URL}/tenants"
    payload = {
        "tenant": {
            "name": name,
            "description": description,
            "max_gateway_count": max_gateway_count,
            "max_device_count": max_device_count,
            "private_gateways_up": private_gateways_up,
            "private_gateways_down": private_gateways_down,
        }
    }
    resp = requests.post(url, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def create_application(tenant_id, name, description=""):
    url = f"{CHIRPSTACK_URL}/applications"
    payload = {
        "application": {
            "tenant_id": tenant_id,
            "name": name,
            "description": description,
        }
    }
    resp = requests.post(url, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def create_device_profile(tenant_id, name, region_config, mac_version="1.0.3", adr_algorithm_id="default"):
    url = f"{CHIRPSTACK_URL}/device-profiles"
    payload = {
        "device_profile": {
            "tenant_id": tenant_id,
            "name": name,
            "region_config_id": region_config,
            "mac_version": mac_version,
            "adr_algorithm_id": adr_algorithm_id,
            "supports_otaa": True,
        }
    }
    resp = requests.post(url, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def create_gateway(tenant_id, gateway_id, name, network_server_id, description=""):
    url = f"{CHIRPSTACK_URL}/gateways"
    payload = {
        "gateway": {
            "tenant_id": tenant_id,
            "id": gateway_id,
            "name": name,
            "description": description,
            "network_server_id": network_server_id,
        }
    }
    resp = requests.post(url, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def create_device(application_id, device_profile_id, name, dev_eui, join_eui, description=""):
    url = f"{CHIRPSTACK_URL}/devices"
    payload = {
        "device": {
            "application_id": application_id,
            "device_profile_id": device_profile_id,
            "name": name,
            "description": description,
            "dev_eui": dev_eui,
            "join_eui": join_eui,
        }
    }
    resp = requests.post(url, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def set_otaa_keys(dev_eui, app_key):
    url = f"{CHIRPSTACK_URL}/devices/{dev_eui}/keys"
    payload = {"device_keys": {"dev_eui": dev_eui, "app_key": app_key}}
    resp = requests.put(url, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

# Example usage:
# 1. Create tenant
tenant = create_tenant("Southern IoT", "Example tenant", max_gateway_count=5, max_device_count=5)
tenant_id = tenant["id"]

# 2. Create application
app = create_application(tenant_id, "New LoRaWAN Setup", "Application for the new LoRaWAN setup")
app_id = app["id"]

# 3. Create device profile (region_config depends on your ChirpStack region settings, e.g., "as923_2")
profile = create_device_profile(tenant_id, "RnD Device Profile", region_config="as923_2")
device_profile_id = profile["id"]

# 4. Create gateway (replace network_server_id with your own)
# gateway = create_gateway(tenant_id, "ac1f09fffe1f340d", "SouthernIoT-Gateway", network_server_id="<network-server-id>")

# 5. Create device
device = create_device(app_id, device_profile_id, "sep_idf_test",
                       dev_eui="ac1f09fffe1d84d6", join_eui="ac1f09fff9153172",
                       description="Cloned from RnD")
# 6. Set OTAA keys
set_otaa_keys("ac1f09fffe1d84d6", "ac1f09fffe1d84d6ac1f09fff9153172")

print("Setup complete!")
