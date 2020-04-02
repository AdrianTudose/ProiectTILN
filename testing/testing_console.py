from algorithms import Preprocesor, SemanticAnalizer, Geolocator


text = "Biserica din cărămidă frumos de la sfârșitul secolului XV-lea, de lângă Palatul Culturii, este Biserica Sf Nicolae. " \
       "O plimbare de 5 minute spre nord, pe Bulevardul Ștefan cel Mare, te duce la Biserica Trei Ierarhi (str. Ștefan " \
       "cel Mare și Sfânt nr 28). "
text1 = "Biserica Armenească de la începutul secolului XIX-lea se află pe Strada Armenească, " \
       "o plimbare de 8 minute la nord-est de Piața Palatului, pe Strada Costache Negri. Mergi puțin mai departe spre " \
       "nord, până pe Strada Cuza Vodă nr 51, unde se înalță Mănăstirea Golia. Biserica Sf Nicolae Domnesc este " \
       "situată în centrul orașului, pe Str Anastasie Panu nr 65, în preajma vechii Curți Domnești, între Palatul " \
       "Culturii și Casa cu arcade (Casa Dosoftei). "



processed_text = Preprocesor.process(text)

directions = SemanticAnalizer.analise(processed_text)

coordinates = Geolocator.get_coordinates(directions)

print(coordinates)