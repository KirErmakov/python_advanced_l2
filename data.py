from datetime import datetime, timezone

register_user = {
    "email": "eve.holt@reqres.in",
    "password": "pistol"
}

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
