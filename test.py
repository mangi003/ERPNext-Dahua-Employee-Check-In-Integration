import local_config as config
import datetime
import requests
import json

def _safe_get_error_str(response):
    """
    Extracts a safe error string from the response object.
    """
    try:
        error_data = response.json()
        return error_data.get('message', str(response.content))
    except Exception:
        return str(response.content)

def send_to_erpnext(employee_field_value, timestamp, device_id=None, log_type=None):
    """
    Example: send_to_erpnext('12349', datetime.datetime.now(), 'HO1', 'IN')
    """
    endpoint_app = "hrms" if config.ERPNEXT_VERSION > 13 else "erpnext"
    url = f"{config.ERPNEXT_URL}/api/method/{endpoint_app}.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"
    
    headers = {
        'Authorization': "token " + config.ERPNEXT_API_KEY + ":" + config.ERPNEXT_API_SECRET,
        'Accept': 'application/json'
    }
    data = {
        'employee_field': 'attendance_device_id',  # Dodato polje
        'employee_field_value': employee_field_value,
        'timestamp': timestamp.isoformat(),
        'device_id': device_id,
        'log_type': log_type
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Successfully logged employee check-in.")
        return 200, response.json()
    else:
        error_str = _safe_get_error_str(response)
        print(f"Error during ERPNext API Call: {error_str}")
        return response.status_code, error_str


# Test funkcija
send_to_erpnext('HR-EMP-00004', datetime.datetime.now(), 'HO1', 'IN')


