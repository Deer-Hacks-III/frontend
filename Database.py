import requests

class UPCManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def add_upc(self, upc):
        response = requests.post(f"{self.base_url}/list/{upc}", json={"upc": upc})
        return response.json()

    def get_upc(self, upc):
        response = requests.get(f"{self.base_url}/list/{upc}")
        return response.json()

    def delete_upc(self, upc):
        response = requests.delete(f"{self.base_url}/list/{upc}")
        return response.json()

    def get_all_upcs(self):
        response = requests.get(f"{self.base_url}/list")
        return response.json()

class UPCManagerLocal:
    def __init__(self):
        self.upcs = []

    def add_upc(self, upc):
        if not upc in self.upcs:
            self.upcs.append(upc)
        return {"upc": False}

    def get_upc(self, upc):
        return {"upc": upc}

    def delete_upc(self, upc):
        self.upcs.remove(upc)
        return {"upc": upc}

    def get_all_upcs(self):
        return self.upcs

# Usage example:
if __name__ == "__main__":
    upc_manager = UPCManager("http://localhost:5000")
    
    # Add UPC
    print(upc_manager.add_upc("123456789"))  # Example UPC

    # Get UPC
    print(upc_manager.get_upc("123456789"))  # Example UPC
    
    # Delete UPC
    print(upc_manager.delete_upc("123456789"))  # Example UPC
    
    # Get all UPCs
    print(upc_manager.get_all_upcs())
