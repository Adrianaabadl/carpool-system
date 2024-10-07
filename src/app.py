"""
This run all the services
"""
from services.poblate_otlp import PoblateDB

class Process():
    def __init__(self, entries) -> None:
        self._poblate_db = PoblateDB(entries)

    def run_services(self):
        self._poblate_db.run()
        

if __name__ == "__main__":
    p = Process()
    p.run_services()