from services.poblate_otlp import PoblateOltp
from services.poblate_olap import PoblateOlap

class Process():
    def __init__(self, number_entries) -> None:
        self._poblate_db = PoblateOltp(number_entries)
        self._populate_dwh = PoblateOltp()

    def run_services(self):
        self._poblate_db.run()
        self._populate_dwh.run()
        

if __name__ == "__main__":
    p = Process(number_entries=5)
    p.run_services()