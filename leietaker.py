from pymongo import MongoClient

client = MongoClient("mongodb+srv://Minionward:czQmUj28yr9kR9S@cluster0.szjwecp.mongodb.net/")
database = client["leietaker_database"]
leietaker_collection = database["leietakere"]

class Leietaker:
    def __init__(self, navn, kontaktinfo, leie_start, leie_slutt):
        self.navn = navn
        self.kontaktinfo = kontaktinfo
        self.leie_start = leie_start
        self.leie_slutt = leie_slutt

    def lagre_i_database(self):
        leietaker_collection.insert_one({
            "navn": self.navn,
            "kontaktinfo": self.kontaktinfo,
            "leie_start": self.leie_start,
            "leie_slutt": self.leie_slutt
        })

    def oppdater_i_database(self):
        leietaker_collection.update_one(
            {"navn": self.navn},
            {"$set": {
                "kontaktinfo": self.kontaktinfo,
                "leie_start": self.leie_start,
                "leie_slutt": self.leie_slutt
            }}
        )

    @staticmethod
    def slett_fra_database(navn):
        leietaker_collection.delete_one({"navn": navn})

def hovedmeny():
    while True:
        print("\n--- LEIETAKERREGISTER ---")
        print("1. Legg til ny leietaker")
        print("2. Vis leietakere")
        print("3. Søk etter leietaker")
        print("4. Oppdater leietakerinformasjon")
        print("5. Slett leietaker")
        print("6. Avslutt")

        valg = input("Velg en handling: ")

        if valg == "1":
            legg_til_ny_leietaker()
        elif valg == "2":
            vis_leietakere()
        elif valg == "3":
            sok_leietaker()
        elif valg == "4":
            oppdater_leietaker()
        elif valg == "5":
            slett_leietaker()
        elif valg == "6":
            print("Programmet avsluttes.")
            break
        else:
            print("Ugyldig valg. Prøv igjen.")

def legg_til_ny_leietaker():
    navn = input("Navn: ")
    kontaktinfo = input("Kontaktinformasjon: ")
    leie_start = input("Leieavtale startdato: ")
    leie_slutt = input("Leieavtale sluttdato: ")

    ny_leietaker = Leietaker(navn, kontaktinfo, leie_start, leie_slutt)
    ny_leietaker.lagre_i_database()
    print(f"{navn} er lagt til som leietaker.")

def vis_leietakere():
    alle_leietakere = leietaker_collection.find()
    print("\n--- LEIETAKERE ---")
    for leietaker in alle_leietakere:
        print(leietaker)

def sok_leietaker():
    navn = input("Skriv inn navnet på leietakeren du søker etter: ")
    leietaker = leietaker_collection.find_one({"navn": navn})
    if leietaker:
        print("\n--- LEIETAKER FUNNET ---")
        print(leietaker)
    else:
        print("Ingen leietaker med det navnet ble funnet.")

def oppdater_leietaker():
    navn = input("Skriv inn navnet på leietakeren du vil oppdatere: ")
    eksisterende_leietaker = leietaker_collection.find_one({"navn": navn})
    
    if eksisterende_leietaker:
        print("\n--- EKSISTERENDE LEIETAKER INFO ---")
        print(eksisterende_leietaker)

        kontaktinfo = input("Oppdater kontaktinformasjon: ")
        leie_start = input("Oppdater leieavtale startdato: ")
        leie_slutt = input("Oppdater leieavtale sluttdato: ")

        oppdatert_leietaker = Leietaker(navn, kontaktinfo, leie_start, leie_slutt)
        oppdatert_leietaker.oppdater_i_database()

        print(f"{navn} er oppdatert.")
    else:
        print("Ingen leietaker med det navnet ble funnet.")

def slett_leietaker():
    navn = input("Skriv inn navnet på leietakeren du vil slette: ")
    eksisterende_leietaker = leietaker_collection.find_one({"navn": navn})
    
    if eksisterende_leietaker:
        Leietaker.slett_fra_database(navn)
        print(f"{navn} er slettet fra leietakerregisteret.")
    else:
        print("Ingen leietaker med det navnet ble funnet.")

if __name__ == "__main__":
    hovedmeny()
