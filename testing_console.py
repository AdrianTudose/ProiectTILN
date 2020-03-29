from main import import_word_sets, preprocesare, analiza_semantica
import rowordnet as rwn

text = "Biserica din cărămidă de la sfârșitul secolului XV-lea, de lângă Palatul Culturii, \
este Biserica Sf Nicolae. O plimbare de 5 minute spre nord, pe Bulevardul Ștefan \
cel Mare, te duce la Biserica Trei Ierarhi (str Ștefan cel Mare și Sfânt nr 28). \
Biserica Armenească de la începutul secolului XIX-lea se află pe Strada \
Armenească, o plimbare de 8 minute la nord-est de Piața Palatului, pe Strada \
Costache Negri. Mergi puțin mai departe spre nord, până pe Strada Cuza Vodă nr \
51, unde se înalță Mănăstirea Golia. \
Biserica Sf Nicolae Domnesc este situată în centrul orașului, pe Str Anastasie \
Panu nr 65, în preajma vechii Curți Domnești, între Palatul Culturii și Casa cu \
arcade (Casa Dosoftei)."

propozitii = preprocesare(text)
analiza_semantica(propozitii)