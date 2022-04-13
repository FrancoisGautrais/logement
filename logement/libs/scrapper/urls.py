from django.conf import settings

from logement.libs.scrapper.base.request import Post
from logement.libs.scrapper.sites.square_habitat import SquarePost

LOOKUP_URLS = [
    "https://www.century21.fr/annonces/f/location-appartement/cpv-35000_rennes/s-55-90/st-0-/b-0-950/p-3-4/",
    "http://www.dany-richard-immo.com/location/",
    SquarePost("https://www.squarehabitat.fr/", {
        "ctl00$menuheader$txtSearchD": "",
        "ctl00$menuheader$txtSearchM": "",
        "token": "",
        "ctl00$cphContent$ctl00$typeProjet": "1",
        "ctl00$cphContent$ctl00$txtGeoloc1A": "RENNES+(35000)",
        "ctl00$cphContent$ctl00$search_id1A": "35238_3",
        "ctl00$cphContent$ctl00$typeBien": "1",
        "ctl00$cphContent$ctl00$surfaceMini": "60+m²",
        "ctl00_cphContent_ctl00_surfaceMini_ClientState": "{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"60\",\"valueAsString\":\"60\",\"minValue\":0,\"maxValue\":70368744177664,\"lastSetTextBoxValue\":\"60+m²\"}",
        "ctl00$cphContent$ctl00$prixMini": "600+€",
        "ctl00_cphContent_ctl00_prixMini_ClientState": "{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"600\",\"valueAsString\":\"600\",\"minValue\":0,\"maxValue\":70368744177664,\"lastSetTextBoxValue\":\"600+€\"}",
        "ctl00$cphContent$ctl00$prixMaxi": "950+€",
        "ctl00_cphContent_ctl00_prixMaxi_ClientState": "{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"950\",\"valueAsString\":\"950\",\"minValue\":1,\"maxValue\":70368744177664,\"lastSetTextBoxValue\":\"950+€\"}",
        "ctl00$cphContent$ctl00$pieces": "3",
        "ctl00$cphContent$ctl00$txtReference": "",
        "ctl00$cphContent$ctl05$txtGeoloc5A_1": "",
        "ctl00$cphContent$ctl05$search_id5A_1": "",
        "ctl00$cphContent$ctl05$txtGeoloc5A_2": "",
        "ctl00$cphContent$ctl05$search_id5A_2": "",
    }),
    "https://www.guenno.com/biens/recherche?realty_type[]=1&mandate_type=2&number_room[]=3&min_surface=&town=RENNES&price_max=950",
    "https://www.blot-immobilier.fr/habitat/location/appartement--appartement-neuf/ille-et-vilaine/rennes/?t3=true&t4=true",
    "https://www.ouestfrance-immo.com/louer/appartement--3-pieces_4-pieces/?lieux=100003,100013&prix=0_950",
    "https://www.giboire.com/recherche-location/appartement/?address%5B%5D=RENNES&priceMin=500&priceMax=950&livingSurfaceMin=55&livingSurfaceMax=90&nbBedrooms%5B%5D=2&nbBedrooms%5B%5D=3&searchBy=undefined#both",
    "https://www.pigeaultimmobilier.com/location/?sous-categorie%5B%5D=1455&agences%5B%5D=26548&prix_min=500&prix_max=950&submitted=1&o=date-desc&action=load_search_results&wia_6_type=location&searchOnMap=0&wia_1_reference=",
    "https://www.bienici.com/realEstateAds.json?filters=%7B%22size%22%3A24%2C%22from%22%3A0%2C%22showAllModels%22%3Afalse%2C%22filterType%22%3A%22rent%22%2C%22propertyType%22%3A%5B%22flat%22%5D%2C%22minPrice%22%3A600%2C%22maxPrice%22%3A950%2C%22minRooms%22%3A3%2C%22maxRooms%22%3A4%2C%22minArea%22%3A55%2C%22maxArea%22%3A90%2C%22page%22%3A1%2C%22sortBy%22%3A%22relevance%22%2C%22sortOrder%22%3A%22desc%22%2C%22onTheMarket%22%3A%5Btrue%5D%2C%22zoneIdsByTypes%22%3A%7B%22zoneIds%22%3A%5B%22-54517%22%5D%7D%7D&extensionType=extendedIfNoResult",
    "https://www.cabinet-martin.fr/location/appartement/rennes/3-pieces--4-pieces/600-euros-minimum/950-euros-maximum",
]

if __name__=="__main__":
    from logement.libs.scrapper import scrap
    for url in LOOKUP_URLS:
        x = scrap(url)
        for v in x.elements:
            d = v.visit()
            print(f"ID = {d.custom_id}")
            print(f"title = {d.title}")
            print(f"content = {d.content}")
            print(f"imgs = {d.imgs}")
            print(f"prix = {d.prix}")
            print(f"phone = {d.phones}")
            print(f"surface = {d.surface}")
            print(f"address = {d.address}")
            print("\n\n")
