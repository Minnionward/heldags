#når jeg laget programmet fikk jeg mye hjelp av en kompis som har jobbet som fullstack dev i 3 år når jeg lagde demo version
#jeg fikk også hjelp til hvordan jeg skulle videre utvikle programmet hvis det var nødvendig.




# Importer MongoClient-klassen fra pymongo-modulen
from pymongo import MongoClient

# Koble til MongoDB Atlas-klyngen ved hjelp av tilkoblingsstrengen
client = MongoClient("mongodb+srv://Minionward:czQmUj28yr9kR9S@cluster0.szjwecp.mongodb.net/")

# Få tilgang til databasen "leietaker_database"
database = client["leietaker_database"]

# Få tilgang til samlingen "leietakere" innenfor databasen
leietaker_collection = database["leietakere"]

# Definer en klasse som representerer en Leietaker
class Leietaker:
    def __init__(self, navn, etternavn, kontaktinfo, leie_start, leie_slutt, kontornummer, faktura):
        # Initialiser instansvariabler med gitt verdier
        self.navn = navn
        self.etternavn = etternavn
        self.kontaktinfo = kontaktinfo
        self.kontornummer = kontornummer
        self.leie_start = leie_start
        self.leie_slutt = leie_slutt
        self.faktura = faktura
        

    # Metode for å lagre Leietaker-instansen i MongoDB-samlingen
    def lagre_i_database(self):
        leietaker_collection.insert_one({
            "navn": self.navn,
            "etternavn": self.etternavn,
            "kontaktinfo": self.kontaktinfo,
            "leie_start": self.leie_start,
            "leie_slutt": self.leie_slutt,
            "kontornummer": self.kontornummer,
            "faktura": self.faktura,
        })

    # Metode for å oppdatere Leietaker-instansen i MongoDB-samlingen
    def oppdater_i_database(self):
        leietaker_collection.update_one(
            {"navn": self.navn},
            {"$set": {
                "etternavn": self.etternavn,
                "kontaktinfo": self.kontaktinfo,
                "leie_start": self.leie_start,
                "leie_slutt": self.leie_slutt,
                "kontornummer": self.kontornummer,
                "faktura": self.faktura
                
            }}
        )

    # Statisk metode for å slette en Leietaker fra MongoDB-samlingen etter navn
    @staticmethod
    def slett_fra_database(navn):
        leietaker_collection.delete_one({"navn": navn})

# Funksjon som representerer hovedmenyen i programmet
def hovedmeny():
    while True:
        # Vis hovedmenyalternativene
        print("\n--- LEIETAKERREGISTER ---")
        print("1. Legg til ny leietaker")
        print("2. Vis leietakere")
        print("3. Søk etter leietaker")
        print("4. Oppdater leietakerinformasjon")
        print("5. Slett leietaker")
        print("6. Avslutt")

        # Hent brukerens valg
        valg = input("Velg en handling: ")

        # Utfør handlinger basert på brukerens valg
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

# Funksjon for å legge til en ny Leietaker basert på brukerinput
def legg_til_ny_leietaker():
    navn = input("Navn: ")
    etternavn = input ("Etternavn")
    kontaktinfo = input("Kontaktinformasjon: ")
    leie_start = input("Leieavtale startdato: ")
    leie_slutt = input("Leieavtale sluttdato: ")
    kontornummer = input("kontornummer")
    faktura = input("faktura")

    # Opprett en ny Leietaker-instans
    ny_leietaker = Leietaker(navn, etternavn, kontaktinfo, leie_start, leie_slutt, kontornummer, faktura)
    # Lagre den nye Leietaker-instansen i MongoDB-samlingen
    ny_leietaker.lagre_i_database()
    print(f"{navn} er lagt til som leietaker.")

# Funksjon for å vise alle Leietaker-instanser i MongoDB-samlingen
def vis_leietakere():
    alle_leietakere = leietaker_collection.find()
    print("\n--- LEIETAKERE ---")
    for leietaker in alle_leietakere:
        print(leietaker)

# Funksjon for å søke etter en spesifikk Leietaker etter navn
def sok_leietaker():
    navn = input("Skriv inn navnet på leietakeren du søker etter: ")
    leietaker = leietaker_collection.find_one({"navn": navn})
    if leietaker:
        print("\n--- LEIETAKER FUNNET ---")
        print(leietaker)
    else:
        print("Ingen leietaker med det navnet ble funnet.")

# Funksjon for å oppdatere informasjonen til en eksisterende Leietaker
def oppdater_leietaker():
    navn = input("Skriv inn navnet på leietakeren du vil oppdatere: ")
    eksisterende_leietaker = leietaker_collection.find_one({"navn": navn})
    
    if eksisterende_leietaker:
        print("\n--- EKSISTERENDE LEIETAKER INFO ---")
        print(eksisterende_leietaker)

        # Hent oppdatert informasjon fra brukeren
        etternavn = input("Oppdater etternavn")
        kontaktinfo = input("Oppdater kontaktinformasjon: ")
        leie_start = input("Oppdater leieavtale startdato: ")
        leie_slutt = input("Oppdater leieavtale sluttdato: ")
        kontornummer = input("Oppdater kontornummer")
        faktura = input("oppdater faktura")

        # Opprett en oppdatert Leietaker-instans
        oppdatert_leietaker = Leietaker(navn, etternavn, kontaktinfo, leie_start, leie_slutt, kontornummer, faktura)
        # Oppdater Leietaker-instansen i MongoDB-samlingen
        oppdatert_leietaker.oppdater_i_database()

        print(f"{navn} er oppdatert.")
    else:
        print("Ingen leietaker med det navnet ble funnet.")

# Funksjon for å slette en Leietaker fra MongoDB-samlingen
def slett_leietaker():
    navn = input("Skriv inn navnet på leietakeren du vil slette: ")
    eksisterende_leietaker = leietaker_collection.find_one({"navn": navn})
    
    if eksisterende_leietaker:
        # Slett Leietaker fra MongoDB-samlingen
        Leietaker.slett_fra_database(navn)
        print(f"{navn} er slettet fra leietakerregisteret.")
    else:
        print("Ingen leietaker med det navnet ble funnet.")

# Oppstartssted for programmet
if __name__ == "__main__":
    hovedmeny()
