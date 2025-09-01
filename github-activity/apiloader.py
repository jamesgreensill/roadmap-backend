import json


class Loader:
    @staticmethod
    def load(filepath: str):
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None, None

        hostname = data.get('hostname')
        endpoints = data.get('endpoints')

        if not hostname or not isinstance(endpoints, dict):
            return None, None

        return hostname, endpoints


class Builder:
    @staticmethod
    def build_api(hostname: str, endpoints: dict):
        api = type('API', (), {})()
        for name, path in endpoints.items():
            setattr(api, name, f"{hostname}{path}")
        return api
