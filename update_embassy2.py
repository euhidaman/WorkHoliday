import os
import re

BASE = r"c:\Users\User\Desktop\Freelancing\WorkHoliday\countries"

# Remaining 213 pairs — embassy of DESTINATION in ORIGIN country
EMBASSIES = {
    # Argentina as origin
    ("Argentina", "Denmark"): ("Royal Danish Embassy, Buenos Aires", "Avenida Leandro N. Alem 1074, Piso 9, C1001AAS Buenos Aires, Argentina", "+54 11 4312 6901", "argentina.um.dk", "Apply via the Danish Embassy in Buenos Aires. Schengen visa applications may be handled by VFS Global."),
    ("Argentina", "Hungary"): ("Embassy of Hungary, Buenos Aires", "Suipacha 1111, Piso 9, C1008 Buenos Aires, Argentina", "+54 11 4312 1661", "buenosaires.mfa.gov.hu", "Apply at the Hungarian Embassy in Buenos Aires. Long-stay WHV requires in-person application."),
    ("Argentina", "Norway"): ("Royal Norwegian Embassy, Buenos Aires", "Carlos Pellegrini 1427, Piso 2, C1011AAC Buenos Aires, Argentina", "+54 11 3724 1200", "norway.no/argentina", "Apply via the Norwegian Embassy in Buenos Aires. WHV requires advance application before departure."),
    ("Argentina", "Poland"): ("Embassy of Poland, Buenos Aires", "Alejandro Maria de Aguado 2870, C1425CEB Buenos Aires, Argentina", "+54 11 4808 1700", "buenosaires.msz.gov.pl", "Apply at the Polish Embassy in Buenos Aires. Long-stay WHV requires in-person application."),
    ("Argentina", "Portugal"): ("Embassy of Portugal, Buenos Aires", "Maipú 942, Piso 17, C1006ACN Buenos Aires, Argentina", "+54 11 4312 3524", "buenosaires.embaixadaportugal.mne.gov.pt", "Apply at the Portuguese Embassy in Buenos Aires. WHV requires in-person application with required documents."),
    ("Argentina", "Sweden"): ("Embassy of Sweden, Buenos Aires", "Olga Cossettini 731, Piso 2, C1107CDA Buenos Aires, Argentina", "+54 11 4329 0800", "swedenabroad.se/argentina", "Apply via the Swedish Embassy in Buenos Aires. WHV requires appointment and advance application."),

    # Australia as origin
    ("Australia", "Argentina"): ("Embassy of Argentina, Canberra", "John McEwen House, Level 2, 7 National Circuit, Barton ACT 2600, Australia", "+61 2 6273 9111", "eaust.cancilleria.gob.ar", "Apply at the Argentine Embassy in Canberra or the Consulate-General in Sydney. Check eVisa eligibility at migraciones.gob.ar."),
    ("Australia", "Belgium"): ("Embassy of Belgium, Canberra", "19 Arkana Street, Yarralumla ACT 2600, Australia", "+61 2 6273 2501", "australia.diplomatie.belgium.be", "Apply at the Belgian Embassy in Canberra. Long-stay work visa applications require an appointment."),
    ("Australia", "Brazil"): ("Embassy of Brazil, Canberra", "QGCN Lote 14, 70800-400 Brasília (Canberra: 19 Forster Crescent, Yarralumla ACT 2600)", "+61 2 6273 2372", "canberra.itamaraty.gov.br", "Apply at the Brazilian Embassy in Canberra. Check visa requirements at vfsglobal.com/brazil."),
    ("Australia", "Bulgaria"): ("Embassy of Bulgaria, Canberra", "33 Culgoa Circuit, O'Malley ACT 2606, Australia", "+61 2 6286 9711", "mfa.bg/embassies/australia", "Apply at the Bulgarian Embassy in Canberra. Long-stay visa requires in-person application and appointment."),
    ("Australia", "Chile"): ("Embassy of Chile, Canberra", "10 Culgoa Circuit, O'Malley ACT 2606, Australia", "+61 2 6286 2430", "chile.gob.cl/australia", "Apply at the Chilean Embassy in Canberra or Consulate-General in Sydney. Check visa requirements at consularchile.gov.cl."),
    ("Australia", "Colombia"): ("Embassy of Colombia, Canberra", "101 Northbourne Avenue, Turner ACT 2612, Australia", "+61 2 6257 2027", "australia.embajada.gov.co", "Apply at the Colombian Embassy in Canberra. WHV requires in-person application with all required documents."),
    ("Australia", "Costa Rica"): ("Embassy of Costa Rica, Canberra", "10 Denver Circuit, Yarralumla ACT 2600, Australia", "+61 2 6290 3071", "embajadacr.com.au", "Apply at the Costa Rican Embassy in Canberra. Visa requirements available at migracion.go.cr."),
    ("Australia", "Croatia"): ("Embassy of Croatia, Canberra", "14 Jindalee Crescent, O'Malley ACT 2606, Australia", "+61 2 6286 6988", "au.mvep.hr", "Apply at the Croatian Embassy in Canberra. Long-stay work visa requires appointment and in-person application."),
    ("Australia", "Cyprus"): ("High Commission of Cyprus, Canberra", "30 Beale Crescent, Deakin ACT 2600, Australia", "+61 2 6281 0832", "mfa.gov.cy/australia", "Apply at the Cyprus High Commission in Canberra. Schengen/EU work visa requires advance application."),
    ("Australia", "Czech Republic"): ("Embassy of Czech Republic, Canberra", "8 Culgoa Circuit, O'Malley ACT 2606, Australia", "+61 2 6290 1386", "mzv.cz/canberra", "Apply at the Czech Embassy in Canberra. Long-stay work visa requires appointment and advance application."),
    ("Australia", "Denmark"): ("Royal Danish Embassy, Canberra", "15 Hunter Street, Yarralumla ACT 2600, Australia", "+61 2 6270 5333", "australien.um.dk", "Apply at the Danish Embassy in Canberra. Schengen visa applications via VFS Global or the embassy."),
    ("Australia", "Estonia"): ("Embassy of Estonia, Canberra (via Singapore)", "83 Lorong Chuan, #01-01 New Tech Park, Singapore 556778", "+65 6509 9700", "singapore.mfa.ee", "Australian applicants contact the Estonian Embassy in Singapore. Long-stay visa requires advance application."),
    ("Australia", "Finland"): ("Embassy of Finland, Canberra", "12 Darwin Avenue, Yarralumla ACT 2600, Australia", "+61 2 6273 3800", "finland.org.au", "Apply at the Finnish Embassy in Canberra. Schengen work visa requires advance appointment and application."),
    ("Australia", "Greece"): ("Embassy of Greece, Canberra", "9 Turrana Street, Yarralumla ACT 2600, Australia", "+61 2 6273 3011", "mfa.gr/australia", "Apply at the Greek Embassy in Canberra. Long-stay work visa requires in-person application and appointment."),
    ("Australia", "Hungary"): ("Embassy of Hungary, Canberra", "79 Hopetoun Circuit, Yarralumla ACT 2600, Australia", "+61 2 6282 3226", "mfa.gov.hu/kulkepviselet/au", "Apply at the Hungarian Embassy in Canberra. Long-stay WHV requires in-person application."),
    ("Australia", "Indonesia"): ("Embassy of Indonesia, Canberra", "8 Darwin Avenue, Yarralumla ACT 2600, Australia", "+61 2 6250 8600", "kemlu.go.id/canberra", "Apply at the Indonesian Embassy in Canberra or via the e-visa portal at molina.imigrasi.go.id."),
    ("Australia", "Italy"): ("Embassy of Italy, Canberra", "12 Grey Street, Deakin ACT 2600, Australia", "+61 2 6273 3333", "ambcanberra.esteri.it", "Apply at the Italian Embassy in Canberra. Long-stay work visa requires appointment and advance application."),
    ("Australia", "Latvia"): ("Embassy of Latvia, Canberra (via Singapore)", "333 Orchard Road, #07-02/03 Mandarin Gallery, Singapore 238867", "+65 6737 1567", "mfa.gov.lv/australia", "Australian applicants contact the Latvian Embassy in Singapore. Long-stay visa requires advance application."),
    ("Australia", "Lithuania"): ("Embassy of Lithuania, Canberra (via Singapore)", "105 Cecil Street, #16-00 The Octagon, Singapore 069534", "+65 6339 4234", "sg.mfa.lt", "Australian applicants contact the Lithuanian Embassy in Singapore. Long-stay visa requires advance application."),
    ("Australia", "Luxembourg"): ("Embassy of Luxembourg, Canberra (via Brussels)", "Avenue des Arts 58, 1000 Brussels, Belgium", "+32 2 444 2711", "mae.lu/en/australia", "Australian applicants contact the Luxembourg Embassy in Brussels. Long-stay work visa requires advance application."),
    ("Australia", "Mainland China"): ("Embassy of China, Canberra", "15 Coronation Drive, Yarralumla ACT 2600, Australia", "+61 2 6228 3999", "au.china-embassy.gov.cn", "Apply at the Chinese Embassy in Canberra or Consulate-General in Sydney, Melbourne, Adelaide, or Perth. Use COVA visa portal."),
    ("Australia", "Malaysia"): ("High Commission of Malaysia, Canberra", "7 Perth Avenue, Yarralumla ACT 2600, Australia", "+61 2 6120 0300", "kln.gov.my/web/aus_canberra", "Apply at the Malaysian High Commission in Canberra. Check eVisa at windowmalaysia.my."),
    ("Australia", "Malta"): ("High Commission of Malta, Canberra", "261 La Perouse Street, Red Hill ACT 2603, Australia", "+61 2 6290 1724", "mfa.gov.mt/australia", "Apply at the Malta High Commission in Canberra. Long-stay EU work visa requires advance application."),
    ("Australia", "Mexico"): ("Embassy of Mexico, Canberra", "14 Perth Avenue, Yarralumla ACT 2600, Australia", "+61 2 6273 3963", "embamex.sre.gob.mx/australia", "Apply at the Mexican Embassy in Canberra. Check visa requirements at consulmex.sre.gob.mx."),
    ("Australia", "Netherlands"): ("Embassy of Netherlands, Canberra", "120 Empire Circuit, Yarralumla ACT 2600, Australia", "+61 2 6220 9400", "netherlands.org.au", "Apply at the Dutch Embassy consulate in Sydney. Schengen work visa requires VFS Global appointment."),
    ("Australia", "Norway"): ("Royal Norwegian Embassy, Canberra", "17 Hunter Street, Yarralumla ACT 2600, Australia", "+61 2 6270 5700", "norway.no/australia", "Apply at the Norwegian Embassy in Canberra. WHV requires advance application before departure."),
    ("Australia", "Peru"): ("Embassy of Peru, Canberra", "40 Brisbane Avenue, Barton ACT 2600, Australia", "+61 2 6273 7351", "peru.org.au", "Apply at the Peruvian Embassy in Canberra. Check visa requirements at rree.gob.pe."),
    ("Australia", "Philippines"): ("Embassy of the Philippines, Canberra", "1 Moonah Place, Yarralumla ACT 2600, Australia", "+61 2 6273 2535", "canberra.philembassy.net", "Apply at the Philippine Embassy in Canberra. Check visa and Special Work Permit requirements at dfa.gov.ph."),
    ("Australia", "Poland"): ("Embassy of Poland, Canberra", "7 Turrana Street, Yarralumla ACT 2600, Australia", "+61 2 6272 1000", "canberra.msz.gov.pl", "Apply at the Polish Embassy in Canberra. Long-stay work visa requires in-person application and appointment."),
    ("Australia", "Portugal"): ("Embassy of Portugal, Canberra", "23 Culgoa Circuit, O'Malley ACT 2606, Australia", "+61 2 6290 1733", "sydney.embaixadaportugal.mne.gov.pt", "Apply at the Portuguese Embassy in Canberra or Consulate-General in Sydney. WHV requires advance application."),
    ("Australia", "Romania"): ("Embassy of Romania, Canberra", "4 Dalman Crescent, O'Malley ACT 2606, Australia", "+61 2 6286 2343", "canberra.mae.ro", "Apply at the Romanian Embassy in Canberra. Long-stay work visa requires in-person application and appointment."),
    ("Australia", "Singapore"): ("High Commission of Singapore, Canberra", "17 Forster Crescent, Yarralumla ACT 2600, Australia", "+61 2 6271 2000", "mfa.gov.sg/canberra", "Apply at the Singapore High Commission in Canberra. Check eVisa at mom.gov.sg for work pass requirements."),
    ("Australia", "Slovakia"): ("Embassy of Slovakia, Canberra", "47 Culgoa Circuit, O'Malley ACT 2606, Australia", "+61 2 6290 1516", "mzv.sk/canberra", "Apply at the Slovak Embassy in Canberra. Long-stay work visa requires in-person application and appointment."),
    ("Australia", "Slovenia"): ("Embassy of Slovenia, Canberra", "Level 6, 60 Marcus Clarke Street, Canberra City ACT 2601, Australia", "+61 2 6243 4830", "canberra.veleposlanistvo.si", "Apply at the Slovenian Embassy in Canberra. Long-stay work visa requires advance appointment and application."),
    ("Australia", "Spain"): ("Embassy of Spain, Canberra", "15 Arkana Street, Yarralumla ACT 2600, Australia", "+61 2 6273 3555", "exteriores.gob.es/australia", "Apply at the Spanish Embassy in Canberra. Long-stay work visa requires appointment and advance application."),
    ("Australia", "Sweden"): ("Embassy of Sweden, Canberra", "5 Turrana Street, Yarralumla ACT 2600, Australia", "+61 2 6270 2700", "swedenabroad.se/australia", "Apply at the Swedish Embassy in Canberra. WHV applications handled in person; appointment required."),
    ("Australia", "Thailand"): ("Royal Thai Embassy, Canberra", "111 Empire Circuit, Yarralumla ACT 2600, Australia", "+61 2 6206 0100", "thaiembassy.org.au", "Apply at the Thai Embassy in Canberra or Thai Consulate-General in Sydney. Check visa at thaievisa.go.th."),
    ("Australia", "USA"): ("Embassy of the USA, Canberra", "Moonah Place, Yarralumla ACT 2600, Australia", "+61 2 6214 5600", "au.usembassy.gov", "Apply at the US Embassy in Canberra. US visa applications via ustraveldocs.com; no WHV program but B1/B2 or other categories available."),
    ("Australia", "Uruguay"): ("Embassy of Uruguay, Canberra", "Level 4, 31 Market Street, Sydney NSW 2000, Australia", "+61 2 9262 6398", "embassyofuruguay.com.au", "Apply at the Uruguayan Embassy in Sydney (covers Australia). Check visa requirements at consulado.mrree.gub.uy."),
    ("Australia", "Vietnam"): ("Embassy of Vietnam, Canberra", "6 Timbarra Crescent, O'Malley ACT 2606, Australia", "+61 2 6286 6059", "vietnamembassy.org.au", "Apply at the Vietnamese Embassy in Canberra or Consulate-General in Sydney. Check e-visa at evisa.xuatnhapcanh.gov.vn."),

    # Austria as origin
    ("Austria", "Argentina"): ("Embassy of Argentina, Vienna", "Goldschmiedgasse 2/1, 1010 Vienna, Austria", "+43 1 533 8585", "eavie.cancilleria.gob.ar", "Apply at the Argentine Embassy in Vienna. Check visa requirements at migraciones.gob.ar."),
    ("Austria", "Chile"): ("Embassy of Chile, Vienna", "Lugeck 1-2, 1010 Vienna, Austria", "+43 1 512 9281", "chile.gob.cl/austria", "Apply at the Chilean Embassy in Vienna. WHV requires in-person application and advance submission."),
    ("Austria", "Mainland China"): ("Embassy of China, Vienna", "Metternichgasse 4, 1030 Vienna, Austria", "+43 1 710 3649", "at.china-embassy.gov.cn", "Apply at the Chinese Embassy in Vienna. Use the COVA visa application portal for long-stay visas."),
    ("Austria", "USA"): ("Embassy of the USA, Vienna", "Boltzmanngasse 16, 1090 Vienna, Austria", "+43 1 313 390", "at.usembassy.gov", "Apply for a US visa at the American Embassy in Vienna. Use ustraveldocs.com for appointment and application."),

    # Canada as origin
    ("Canada", "Belgium"): ("Embassy of Belgium, Ottawa", "360 Albert Street, Suite 820, Ottawa, ON K1R 7X7, Canada", "+1 613 236 7267", "diplomatbelgique.com/canada", "Apply at the Belgian Embassy in Ottawa. Long-stay EU work visa requires in-person application."),
    ("Canada", "Chile"): ("Embassy of Chile, Ottawa", "50 O'Connor Street, Suite 1413, Ottawa, ON K1P 6L2, Canada", "+1 613 235 4402", "chile.gob.cl/canada", "Apply at the Chilean Embassy in Ottawa. WHV requires in-person application with all required documents."),
    ("Canada", "Costa Rica"): ("Embassy of Costa Rica, Ottawa", "325 Dalhousie Street, Suite 407, Ottawa, ON K1N 7G2, Canada", "+1 613 562 2855", "embajadadecostarica.ca", "Apply at the Costa Rican Embassy in Ottawa. Check visa requirements at migracion.go.cr."),
    ("Canada", "Croatia"): ("Embassy of Croatia, Ottawa", "229 Chapel Street, Ottawa, ON K1N 7Y6, Canada", "+1 613 562 7820", "ca.mvep.hr", "Apply at the Croatian Embassy in Ottawa. Long-stay work visa requires in-person application and appointment."),
    ("Canada", "Czech Republic"): ("Embassy of Czech Republic, Ottawa", "251 Cooper Street, Ottawa, ON K2P 0G2, Canada", "+1 613 562 3875", "mzv.cz/ottawa", "Apply at the Czech Embassy in Ottawa. Long-stay work visa requires advance appointment and application."),
    ("Canada", "Denmark"): ("Royal Danish Embassy, Ottawa", "47 Clarence Street, Suite 450, Ottawa, ON K1N 9K1, Canada", "+1 613 562 1811", "canada.um.dk", "Apply at the Danish Embassy in Ottawa. Schengen work visa applications via VFS Global or the embassy."),
    ("Canada", "Estonia"): ("Embassy of Estonia, Ottawa", "260 Dalhousie Street, Suite 210, Ottawa, ON K1N 7E4, Canada", "+1 613 789 4222", "ottawa.mfa.ee", "Apply at the Estonian Embassy in Ottawa. Long-stay EU work visa requires advance appointment and application."),
    ("Canada", "Finland"): ("Embassy of Finland, Ottawa", "55 Metcalfe Street, Suite 850, Ottawa, ON K1P 6L5, Canada", "+1 613 288 2233", "finlandincanada.com", "Apply at the Finnish Embassy in Ottawa. Schengen work visa requires advance application and appointment."),
    ("Canada", "Greece"): ("Embassy of Greece, Ottawa", "80 MacLaren Street, Ottawa, ON K2P 0K6, Canada", "+1 613 238 6271", "mfa.gr/canada", "Apply at the Greek Embassy in Ottawa. Long-stay work visa requires in-person appointment and application."),
    ("Canada", "Hungary"): ("Embassy of Hungary, Ottawa", "299 Waverley Street, Ottawa, ON K2P 0V9, Canada", "+1 613 230 2717", "ottawa.mfa.gov.hu", "Apply at the Hungarian Embassy in Ottawa. Long-stay WHV requires in-person application."),
    ("Canada", "Italy"): ("Embassy of Italy, Ottawa", "275 Slater Street, 21st Floor, Ottawa, ON K1P 5H9, Canada", "+1 613 232 2401", "ambottawa.esteri.it", "Apply at the Italian Embassy in Ottawa. Long-stay work visa requires appointment and advance application."),
    ("Canada", "Latvia"): ("Embassy of Latvia, Ottawa", "350 Sparks Street, Suite 1200, Ottawa, ON K1R 7S8, Canada", "+1 613 238 6014", "ottawa.mfa.gov.lv", "Apply at the Latvian Embassy in Ottawa. Long-stay EU work visa requires advance application."),
    ("Canada", "Lithuania"): ("Embassy of Lithuania, Ottawa", "150 Metcalfe Street, Suite 1600, Ottawa, ON K2P 1P1, Canada", "+1 613 567 5458", "ca.mfa.lt", "Apply at the Lithuanian Embassy in Ottawa. Long-stay EU work visa requires advance application."),
    ("Canada", "Luxembourg"): ("Embassy of Luxembourg, Ottawa (via Washington)", "2200 Massachusetts Avenue NW, Washington, DC 20008, USA", "+1 202 265 4171", "mae.lu/en/usa", "Canadian applicants contact the Luxembourg Embassy in Washington D.C. Long-stay work visa requires advance application."),
    ("Canada", "Mainland China"): ("Embassy of China, Ottawa", "515 St. Patrick Street, Ottawa, ON K1N 5H3, Canada", "+1 613 789 3434", "ca.china-embassy.gov.cn", "Apply at the Chinese Embassy in Ottawa. Use the COVA visa portal or VFS Global. Also contact Consulate-General in Toronto, Vancouver, Calgary."),
    ("Canada", "Netherlands"): ("Embassy of Netherlands, Ottawa", "350 Albert Street, Suite 2020, Ottawa, ON K1R 1A4, Canada", "+1 613 237 5030", "netherlands.ca", "Apply at the Dutch Embassy in Ottawa or consulate in Toronto. Schengen work visa via VFS Global."),
    ("Canada", "Norway"): ("Royal Norwegian Embassy, Ottawa", "150 Metcalfe Street, Suite 1300, Ottawa, ON K2P 1P1, Canada", "+1 613 238 6571", "norway.no/canada", "Apply at the Norwegian Embassy in Ottawa. WHV requires advance application before departure."),
    ("Canada", "Poland"): ("Embassy of Poland, Ottawa", "443 Daly Avenue, Ottawa, ON K1N 6H3, Canada", "+1 613 789 0468", "ottawa.msz.gov.pl", "Apply at the Polish Embassy in Ottawa. Long-stay work visa requires in-person appointment and application."),
    ("Canada", "Portugal"): ("Embassy of Portugal, Ottawa", "645 Island Park Drive, Ottawa, ON K1Y 0B8, Canada", "+1 613 729 0883", "ottawa.embaixadaportugal.mne.gov.pt", "Apply at the Portuguese Embassy in Ottawa. WHV requires advance application and appointment."),
    ("Canada", "Slovakia"): ("Embassy of Slovakia, Ottawa", "50 Rideau Terrace, Ottawa, ON K1M 2A1, Canada", "+1 613 749 4442", "ottawa.mfa.sk", "Apply at the Slovak Embassy in Ottawa. Long-stay work visa requires in-person application and appointment."),
    ("Canada", "Slovenia"): ("Embassy of Slovenia, Ottawa", "150 Metcalfe Street, Suite 2101, Ottawa, ON K2P 1P1, Canada", "+1 613 565 5781", "ottawa.veleposlanistvo.si", "Apply at the Slovenian Embassy in Ottawa. Long-stay work visa requires advance appointment and application."),
    ("Canada", "Spain"): ("Embassy of Spain, Ottawa", "74 Stanley Avenue, Ottawa, ON K1M 1P4, Canada", "+1 613 747 2252", "exteriores.gob.es/canada", "Apply at the Spanish Embassy in Ottawa. Long-stay work visa requires appointment and advance application."),
    ("Canada", "Sweden"): ("Embassy of Sweden, Ottawa", "377 Dalhousie Street, Ottawa, ON K1N 9N8, Canada", "+1 613 244 8200", "swedenabroad.se/canada", "Apply at the Swedish Embassy in Ottawa. WHV applications handled in person; appointment required."),
    ("Canada", "Switzerland"): ("Embassy of Switzerland, Ottawa", "5 Marlborough Avenue, Ottawa, ON K1N 8E6, Canada", "+1 613 235 1837", "eda.admin.ch/canada", "Apply at the Swiss Embassy in Ottawa. Long-stay work visa requires advance appointment and application."),
    ("Canada", "USA"): ("Embassy of the USA, Ottawa", "490 Sussex Drive, Ottawa, ON K1N 1G8, Canada", "+1 613 238 5335", "ca.usembassy.gov", "Apply for a US visa at the American Embassy in Ottawa. Use ustraveldocs.com for appointment and application."),

    # Chile as origin
    ("Chile", "Colombia"): ("Embassy of Colombia, Santiago", "Isidora Goyenechea 2583, Piso 10, Las Condes, Santiago, Chile", "+56 2 2233 5066", "chile.embajada.gov.co", "Apply at the Colombian Embassy in Santiago. Check visa requirements at cancilleria.gov.co."),
    ("Chile", "Czech Republic"): ("Embassy of Czech Republic, Santiago", "Av. El Golf 62, Piso 12, Las Condes, Santiago, Chile", "+56 2 2231 9422", "mzv.cz/santiago", "Apply at the Czech Embassy in Santiago. Long-stay work visa requires advance appointment and application."),
    ("Chile", "Denmark"): ("Royal Danish Embassy, Santiago", "Av. Isidora Goyenechea 3477, Piso 13, Las Condes, Santiago, Chile", "+56 2 2333 0060", "chile.um.dk", "Apply at the Danish Embassy in Santiago. Schengen visa via VFS Global or in person at the embassy."),
    ("Chile", "Hungary"): ("Embassy of Hungary, Santiago", "Av. Nueva Providencia 2116, Of. 1101, Providencia, Santiago, Chile", "+56 2 2232 5516", "santiago.mfa.gov.hu", "Apply at the Hungarian Embassy in Santiago. Long-stay WHV requires in-person application."),
    ("Chile", "Mexico"): ("Embassy of Mexico, Santiago", "Félix de Amesti 128, Las Condes, Santiago, Chile", "+56 2 2583 8400", "sre.gob.mx/chile", "Apply at the Mexican Embassy in Santiago. Check visa requirements at consulmex.sre.gob.mx."),
    ("Chile", "Peru"): ("Embassy of Peru, Santiago", "Av. Andrés Bello 1751, Providencia, Santiago, Chile", "+56 2 2235 6451", "embperu.cl", "Apply at the Peruvian Embassy in Santiago. Check visa requirements at rree.gob.pe."),
    ("Chile", "Poland"): ("Embassy of Poland, Santiago", "General del Canto 35, Piso 9, Providencia, Santiago, Chile", "+56 2 2231 3800", "santiago.msz.gov.pl", "Apply at the Polish Embassy in Santiago. Long-stay work visa requires advance application."),
    ("Chile", "Portugal"): ("Embassy of Portugal, Santiago", "Nueva Tajamar 481, Torre Sur, Piso 22, Las Condes, Santiago, Chile", "+56 2 2203 0542", "santiago.embaixadaportugal.mne.gov.pt", "Apply at the Portuguese Embassy in Santiago. WHV requires in-person application."),
    ("Chile", "Sweden"): ("Embassy of Sweden, Santiago", "11 de Septiembre 2353, Piso 4, Providencia, Santiago, Chile", "+56 2 2940 1700", "swedenabroad.se/chile", "Apply at the Swedish Embassy in Santiago. WHV requires advance application and appointment."),
    ("Chile", "Switzerland"): ("Embassy of Switzerland, Santiago", "Av. Américo Vespucio Sur 100, Piso 14, Las Condes, Santiago, Chile", "+56 2 2928 0100", "eda.admin.ch/chile", "Apply at the Swiss Embassy in Santiago. Long-stay work visa requires advance appointment and application."),

    # Czech Republic as origin
    ("Czech Republic", "Chile"): ("Embassy of Chile, Prague", "Muchova 9, 160 00 Prague 6, Czech Republic", "+420 233 371 380", "chile.gob.cl/czech-republic", "Apply at the Chilean Embassy in Prague. WHV requires in-person application before departure."),

    # Denmark as origin
    ("Denmark", "Argentina"): ("Embassy of Argentina, Copenhagen", "Bernstorffsvej 29, 2900 Hellerup, Copenhagen, Denmark", "+45 3962 1280", "ecope.cancilleria.gob.ar", "Apply at the Argentine Embassy in Copenhagen. Check visa requirements at migraciones.gob.ar."),
    ("Denmark", "Chile"): ("Embassy of Chile, Copenhagen", "Kastelsvej 15, 2100 Copenhagen, Denmark", "+45 3542 2300", "chile.gob.cl/denmark", "Apply at the Chilean Embassy in Copenhagen. WHV requires in-person application before departure."),

    # Finland as origin
    ("Finland", "Chile"): ("Embassy of Chile, Helsinki", "Eteläesplanadi 22A, 00130 Helsinki, Finland", "+358 9 635 311", "chile.gob.cl/finland", "Apply at the Chilean Embassy in Helsinki. WHV requires in-person application before departure."),

    # France as origin
    ("France", "Argentina"): ("Embassy of Argentina, Paris", "6 Rue Cimarosa, 75116 Paris, France", "+33 1 44 05 27 00", "epari.cancilleria.gob.ar", "Apply at the Argentine Embassy in Paris. Check visa requirements at migraciones.gob.ar."),
    ("France", "Brazil"): ("Embassy of Brazil, Paris", "34 Cours Albert 1er, 75008 Paris, France", "+33 1 45 61 63 00", "paris.itamaraty.gov.br", "Apply at the Brazilian Embassy in Paris. Check visa requirements at vfsglobal.com/brazil."),
    ("France", "Chile"): ("Embassy of Chile, Paris", "2 Avenue de la Motte-Picquet, 75007 Paris, France", "+33 1 47 05 46 01", "chile.gob.cl/france", "Apply at the Chilean Embassy in Paris. WHV requires in-person application before departure."),
    ("France", "Colombia"): ("Embassy of Colombia, Paris", "22 Rue de l'Élysée, 75008 Paris, France", "+33 1 42 65 46 08", "paris.embajada.gov.co", "Apply at the Colombian Embassy in Paris. Check visa requirements at cancilleria.gov.co."),
    ("France", "Mexico"): ("Embassy of Mexico, Paris", "9 Rue de Longchamp, 75116 Paris, France", "+33 1 53 70 27 70", "sre.gob.mx/france", "Apply at the Mexican Embassy in Paris. Check visa requirements at consulmex.sre.gob.mx."),
    ("France", "Peru"): ("Embassy of Peru, Paris", "50 Avenue Kléber, 75116 Paris, France", "+33 1 53 70 42 00", "embassyperou.fr", "Apply at the Peruvian Embassy in Paris. Check visa requirements at rree.gob.pe."),
    ("France", "Uruguay"): ("Embassy of Uruguay, Paris", "15 Rue Le Sueur, 75116 Paris, France", "+33 1 45 00 81 37", "uy-paris.mrree.gub.uy", "Apply at the Uruguayan Embassy in Paris. Check visa requirements at consulado.mrree.gub.uy."),

    # Germany as origin
    ("Germany", "Argentina"): ("Embassy of Argentina, Berlin", "Kleiststrasse 23-26, 10787 Berlin, Germany", "+49 30 226 669 0", "eberlin.cancilleria.gob.ar", "Apply at the Argentine Embassy in Berlin. Check visa requirements at migraciones.gob.ar."),
    ("Germany", "Brazil"): ("Embassy of Brazil, Berlin", "Wallstrasse 57, 10179 Berlin, Germany", "+49 30 726 280", "berlin.itamaraty.gov.br", "Apply at the Brazilian Embassy in Berlin. Check visa requirements at vfsglobal.com/brazil."),
    ("Germany", "Chile"): ("Embassy of Chile, Berlin", "Mohrenstrasse 42, 10117 Berlin, Germany", "+49 30 726 209 0", "chile.gob.cl/germany", "Apply at the Chilean Embassy in Berlin. WHV requires in-person application before departure."),
    ("Germany", "Israel"): ("Embassy of Israel, Berlin", "Auguste-Viktoria-Strasse 74-76, 14193 Berlin, Germany", "+49 30 8904 5500", "berlin.mfa.gov.il", "Apply at the Israeli Embassy in Berlin. Check visa requirements at mfa.gov.il."),
    ("Germany", "Mainland China"): ("Embassy of China, Berlin", "Märkisches Ufer 54, 10179 Berlin, Germany", "+49 30 275 880", "de.china-embassy.gov.cn", "Apply at the Chinese Embassy in Berlin. Use the COVA visa portal or VFS Global."),
    ("Germany", "Singapore"): ("Embassy of Singapore, Berlin", "Voßstrasse 17, 10117 Berlin, Germany", "+49 30 226 343 0", "mfa.gov.sg/berlin", "Apply at the Singapore Embassy in Berlin. Check work pass requirements at mom.gov.sg."),
    ("Germany", "USA"): ("Embassy of the USA, Berlin", "Pariser Platz 2, 10117 Berlin, Germany", "+49 30 8305 0", "de.usembassy.gov", "Apply for a US visa at the American Embassy in Berlin. Use ustraveldocs.com for appointment and DS-160 application."),
    ("Germany", "Uruguay"): ("Embassy of Uruguay, Berlin", "Budapester Strasse 39, 10787 Berlin, Germany", "+49 30 263 9016", "alemania.mrree.gub.uy", "Apply at the Uruguayan Embassy in Berlin. Check visa requirements at consulado.mrree.gub.uy."),

    # Hong Kong as origin
    ("Hong Kong", "Hungary"): ("Embassy of Hungary, Hong Kong (via Beijing)", "No. 10, Dongzhimenwai Dajie, Beijing 100600, China", "+86 10 6532 1431", "beijing.mfa.gov.hu", "Hong Kong applicants contact the Hungarian Embassy in Beijing. Long-stay WHV requires in-person application."),
    ("Hong Kong", "Italy"): ("Italian Consulate-General, Hong Kong", "Room 801, Hutchison House, 10 Harcourt Road, Central, Hong Kong", "+852 2522 0033", "conshongkong.esteri.it", "Apply at the Italian Consulate-General in Hong Kong. Long-stay work visa requires appointment and advance application."),
    ("Hong Kong", "Mainland China"): ("Mainland Travel Permit Office / CTS", "China Travel Service, Units G07-08, Star House, 3 Salisbury Road, Tsim Sha Tsui, Hong Kong", "+852 2315 7100", "cts.com.hk", "Hong Kong permanent residents use the Home Return Permit (回乡证). Contact CTS for travel permits and visa assistance."),
    ("Hong Kong", "Netherlands"): ("Consulate-General of Netherlands, Hong Kong", "3601-3608, Tower Two, Lippo Centre, 89 Queensway, Admiralty, Hong Kong", "+852 2522 5127", "netherlands-hongkong.nl", "Apply at the Dutch Consulate-General in Hong Kong. Schengen work visa requires VFS Global appointment."),
    ("Hong Kong", "Sweden"): ("Swedish Consulate-General, Hong Kong", "7/F, Bank of East Asia Building, 10 Des Voeux Road Central, Hong Kong", "+852 2521 1212", "swedenabroad.se/hong-kong", "Apply at the Swedish Consulate in Hong Kong. WHV requires advance application and appointment."),
    ("Hong Kong", "USA"): ("US Consulate-General, Hong Kong", "26 Garden Road, Central, Hong Kong", "+852 2523 9011", "hk.usconsulate.gov", "Apply at the US Consulate-General in Hong Kong. Use ustraveldocs.com for DS-160 and appointment booking."),

    # Hungary as origin
    ("Hungary", "Argentina"): ("Embassy of Argentina, Budapest", "Bimbo ut 22-24, 1022 Budapest, Hungary", "+36 1 326 9023", "ebudapest.cancilleria.gob.ar", "Apply at the Argentine Embassy in Budapest. Check visa requirements at migraciones.gob.ar."),
    ("Hungary", "Chile"): ("Embassy of Chile, Budapest", "Lejtő utca 8, 1121 Budapest, Hungary", "+36 1 214 2110", "chile.gob.cl/hungary", "Apply at the Chilean Embassy in Budapest. WHV requires in-person application before departure."),

    # Ireland as origin
    ("Ireland", "Argentina"): ("Embassy of Argentina, Dublin", "Fitzwilliam House, 3rd Floor, Wilton Place, Dublin 2, Ireland", "+353 1 269 1546", "edublin.cancilleria.gob.ar", "Apply at the Argentine Embassy in Dublin. Check visa requirements at migraciones.gob.ar."),
    ("Ireland", "Chile"): ("Embassy of Chile, Dublin", "44 Wellington Road, Dublin 4, Ireland", "+353 1 667 9901", "chile.gob.cl/ireland", "Apply at the Chilean Embassy in Dublin. WHV requires in-person application before departure."),
    ("Ireland", "USA"): ("Embassy of the USA, Dublin", "42 Elgin Road, Ballsbridge, Dublin 4, Ireland", "+353 1 668 8777", "ie.usembassy.gov", "Apply for a US visa at the American Embassy in Dublin. Use ustraveldocs.com for DS-160 and appointment."),

    # Japan as origin
    ("Japan", "Argentina"): ("Embassy of Argentina, Tokyo", "MG Ichigaya Building, 2-14-14 Kudan Kita, Chiyoda-ku, Tokyo 102-0073", "+81 3 5276 0461", "etkyo.cancilleria.gob.ar", "Apply at the Argentine Embassy in Tokyo. Check visa requirements at migraciones.gob.ar."),
    ("Japan", "Chile"): ("Embassy of Chile, Tokyo", "Nippon Press Center Building, 2-2-1 Uchisaiwaicho, Chiyoda-ku, Tokyo 100-0011", "+81 3 3452 7561", "chile.gob.cl/japan", "Apply at the Chilean Embassy in Tokyo. WHV requires in-person application before departure."),
    ("Japan", "Czech Republic"): ("Embassy of Czech Republic, Tokyo", "2-16-14 Hiroo, Shibuya-ku, Tokyo 150-0012, Japan", "+81 3 3400 8122", "mzv.cz/tokyo", "Apply at the Czech Embassy in Tokyo. Long-stay work visa requires advance appointment and application."),
    ("Japan", "Denmark"): ("Royal Danish Embassy, Tokyo", "29-6 Sarugakucho, Shibuya-ku, Tokyo 150-0033, Japan", "+81 3 3496 3001", "japan.um.dk", "Apply at the Danish Embassy in Tokyo. Schengen visa via VFS Global or in person at the embassy."),
    ("Japan", "Estonia"): ("Embassy of Estonia, Tokyo", "2-6-15 Jingumae, Shibuya-ku, Tokyo 150-0001, Japan", "+81 3 5412 7281", "tokyo.mfa.ee", "Apply at the Estonian Embassy in Tokyo. Long-stay EU work visa requires advance appointment and application."),
    ("Japan", "Hungary"): ("Embassy of Hungary, Tokyo", "2-17-14 Mita, Minato-ku, Tokyo 108-0073, Japan", "+81 3 3798 8801", "tokyo.mfa.gov.hu", "Apply at the Hungarian Embassy in Tokyo. Long-stay WHV requires in-person application."),
    ("Japan", "Iceland"): ("Embassy of Iceland, Tokyo", "3-5-31 Kitashinagawa, Shinagawa-ku, Tokyo 140-0001, Japan", "+81 3 3457 4600", "iceland.is/japan", "Apply at the Icelandic Embassy in Tokyo. WHV requires advance in-person application."),
    ("Japan", "Latvia"): ("Embassy of Latvia, Tokyo", "37-11 Kamiyoga, 3-chome, Setagaya-ku, Tokyo 158-0098, Japan", "+81 3 3467 6888", "tokyo.mfa.gov.lv", "Apply at the Latvian Embassy in Tokyo. Long-stay EU work visa requires advance application."),
    ("Japan", "Lithuania"): ("Embassy of Lithuania, Tokyo", "3-6-12 Kojimachi, Chiyoda-ku, Tokyo 102-0083, Japan", "+81 3 3265 7201", "jp.mfa.lt", "Apply at the Lithuanian Embassy in Tokyo. Long-stay EU work visa requires advance application."),
    ("Japan", "Netherlands"): ("Embassy of Netherlands, Tokyo", "3-6-3 Shiba Koen, Minato-ku, Tokyo 105-0011, Japan", "+81 3 5401 0411", "netherlands.or.jp", "Apply at the Dutch Embassy in Tokyo. Schengen work visa requires VFS Global appointment."),
    ("Japan", "Norway"): ("Royal Norwegian Embassy, Tokyo", "5-12-2 Minami-Azabu, Minato-ku, Tokyo 106-0047, Japan", "+81 3 3440 2611", "norway.no/japan", "Apply at the Norwegian Embassy in Tokyo. WHV requires advance application before departure."),
    ("Japan", "Poland"): ("Embassy of Poland, Tokyo", "2-13-5 Mita, Meguro-ku, Tokyo 153-0062, Japan", "+81 3 5794 7020", "tokyo.msz.gov.pl", "Apply at the Polish Embassy in Tokyo. Long-stay work visa requires in-person appointment and application."),
    ("Japan", "Portugal"): ("Embassy of Portugal, Tokyo", "Olympia Annex 4F, 6-31-21 Jingumae, Shibuya-ku, Tokyo 150-0001, Japan", "+81 3 5212 7322", "tokyo.embaixadaportugal.mne.gov.pt", "Apply at the Portuguese Embassy in Tokyo. WHV requires advance application and appointment."),
    ("Japan", "Slovakia"): ("Embassy of Slovakia, Tokyo", "2-11-33 Moto-Azabu, Minato-ku, Tokyo 106-0046, Japan", "+81 3 3451 2200", "mzv.sk/tokyo", "Apply at the Slovak Embassy in Tokyo. Long-stay work visa requires in-person appointment and application."),
    ("Japan", "Spain"): ("Embassy of Spain, Tokyo", "1-3-29 Roppongi, Minato-ku, Tokyo 106-0032, Japan", "+81 3 3583 8531", "exteriores.gob.es/japan", "Apply at the Spanish Embassy in Tokyo. Long-stay work visa requires appointment and advance application."),
    ("Japan", "Sweden"): ("Embassy of Sweden, Tokyo", "1-10-3-100 Roppongi, Minato-ku, Tokyo 106-0032, Japan", "+81 3 5562 5050", "swedenabroad.se/japan", "Apply at the Swedish Embassy in Tokyo. WHV requires advance application and appointment."),
    ("Japan", "Uruguay"): ("Embassy of Uruguay, Tokyo", "Kowa Building Room 908, 4-12-24 Nishi-Azabu, Minato-ku, Tokyo 106-0031", "+81 3 5454 6070", "japonembajada.mrree.gub.uy", "Apply at the Uruguayan Embassy in Tokyo. Check visa requirements at consulado.mrree.gub.uy."),

    # Mainland China as origin
    ("Mainland China", "USA"): ("Embassy of the USA, Beijing", "55 An Jia Lou Road, Chaoyang District, Beijing 100600, China", "+86 10 8531 4000", "china.usembassy-china.org.cn", "Apply for a US visa at the American Embassy in Beijing or Consulate-General in Shanghai, Guangzhou, Chengdu, or Shenyang. Use ustraveldocs.com."),

    # Netherlands as origin
    ("Netherlands", "Argentina"): ("Embassy of Argentina, The Hague", "Javastraat 20, 2585 AN The Hague, Netherlands", "+31 70 365 0867", "elahe.cancilleria.gob.ar", "Apply at the Argentine Embassy in The Hague. Check visa requirements at migraciones.gob.ar."),
    ("Netherlands", "Uruguay"): ("Embassy of Uruguay, The Hague", "Mauritskade 33, 2514 HD The Hague, Netherlands", "+31 70 365 9032", "lahe.mrree.gub.uy", "Apply at the Uruguayan Embassy in The Hague. Check visa requirements at consulado.mrree.gub.uy."),

    # New Zealand as origin (remaining)
    ("New Zealand", "Argentina"): ("Embassy of Argentina, Wellington", "Reserve Bank Building, Level 14, 2 The Terrace, Wellington 6011, New Zealand", "+64 4 472 8330", "ewellington.cancilleria.gob.ar", "Apply at the Argentine Embassy in Wellington. Check visa requirements at migraciones.gob.ar."),
    ("New Zealand", "Belgium"): ("Embassy of Belgium, Wellington", "Level 8, 88 The Terrace, Wellington 6011, New Zealand", "+64 4 924 6640", "newzealand.diplomatie.belgium.be", "Apply at the Belgian Embassy in Wellington. Long-stay EU work visa requires in-person application."),
    ("New Zealand", "Brazil"): ("Embassy of Brazil, Wellington", "10th Floor, Sovereign Assurance Building, 34 Manners Street, Wellington 6011", "+64 4 473 3516", "wellington.itamaraty.gov.br", "Apply at the Brazilian Embassy in Wellington. Check visa requirements at vfsglobal.com/brazil."),
    ("New Zealand", "Chile"): ("Embassy of Chile, Wellington", "Level 11, 171 Featherston Street, Wellington 6011, New Zealand", "+64 4 471 6270", "chile.gob.cl/new-zealand", "Apply at the Chilean Embassy in Wellington. WHV requires in-person application before departure."),
    ("New Zealand", "Colombia"): ("Embassy of Colombia, Wellington", "Level 7, 55 Featherston Street, Wellington 6011, New Zealand", "+64 4 915 1700", "newzealand.embajada.gov.co", "Apply at the Colombian Embassy in Wellington. Check visa requirements at cancilleria.gov.co."),
    ("New Zealand", "Croatia"): ("Embassy of Croatia, Wellington (via Canberra)", "14 Jindalee Crescent, O'Malley ACT 2606, Australia", "+61 2 6286 6988", "au.mvep.hr", "NZ applicants contact the Croatian Embassy in Canberra. Long-stay work visa requires advance application."),
    ("New Zealand", "Czech Republic"): ("Embassy of Czech Republic, Wellington", "Level 4, HSBC Tower, 195 Lambton Quay, Wellington 6011, New Zealand", "+64 4 477 5481", "mzv.cz/wellington", "Apply at the Czech Embassy in Wellington. Long-stay work visa requires advance appointment and application."),
    ("New Zealand", "Denmark"): ("Royal Danish Embassy, Wellington", "Level 7, 40 Mercer Street, Wellington 6011, New Zealand", "+64 4 471 0520", "newzealand.um.dk", "Apply at the Danish Embassy in Wellington. Schengen visa via VFS Global or in person at the embassy."),
    ("New Zealand", "Estonia"): ("Embassy of Estonia, Wellington (via Canberra)", "Level 6, 60 Marcus Clarke Street, Canberra ACT 2601, Australia", "+61 2 6243 4830", "canberra.veleposlanistvo.si", "NZ applicants contact the Estonian representative office. Long-stay visa requires advance application."),
    ("New Zealand", "Finland"): ("Embassy of Finland, Wellington", "Level 12, 171 Featherston Street, Wellington 6011, New Zealand", "+64 4 499 4599", "finland.org.nz", "Apply at the Finnish Embassy in Wellington. Schengen work visa requires advance application and appointment."),
    ("New Zealand", "Greece"): ("Embassy of Greece, Wellington", "Level 5, 15 Murphy Street, Wellington 6011, New Zealand", "+64 4 473 7775", "mfa.gr/new-zealand", "Apply at the Greek Embassy in Wellington. Long-stay work visa requires in-person appointment and application."),
    ("New Zealand", "Hungary"): ("Embassy of Hungary, Wellington (via Canberra)", "79 Hopetoun Circuit, Yarralumla ACT 2600, Australia", "+61 2 6282 3226", "mfa.gov.hu/kulkepviselet/au", "NZ applicants contact the Hungarian Embassy in Canberra. Long-stay WHV requires in-person application."),
    ("New Zealand", "Italy"): ("Embassy of Italy, Wellington", "34-38 Grant Road, Wellington 6011, New Zealand", "+64 4 473 5339", "ambwellington.esteri.it", "Apply at the Italian Embassy in Wellington. Long-stay work visa requires appointment and advance application."),
    ("New Zealand", "Latvia"): ("Embassy of Latvia, Wellington (via Canberra)", "Level 6, 60 Marcus Clarke Street, Canberra ACT 2601, Australia", "+61 2 6243 4830", "mfa.gov.lv/australia", "NZ applicants contact the Latvian representative office. Long-stay EU work visa requires advance application."),
    ("New Zealand", "Lithuania"): ("Embassy of Lithuania, Wellington (via Canberra)", "Level 6, 60 Marcus Clarke Street, Canberra ACT 2601, Australia", "+61 2 6243 4830", "sg.mfa.lt", "NZ applicants contact the Lithuanian representative. Long-stay EU work visa requires advance application."),
    ("New Zealand", "Luxembourg"): ("Embassy of Luxembourg, Wellington (via Brussels)", "Avenue des Arts 58, 1000 Brussels, Belgium", "+32 2 444 2711", "mae.lu/en", "NZ applicants contact the Luxembourg Embassy in Brussels. Long-stay work visa requires advance application."),
    ("New Zealand", "Mainland China"): ("Embassy of China, Wellington", "2-6 Glenmore Street, Wellington 6011, New Zealand", "+64 4 472 1382", "nz.china-embassy.gov.cn", "Apply at the Chinese Embassy in Wellington. Use COVA visa portal or VFS Global."),
    ("New Zealand", "Malaysia"): ("High Commission of Malaysia, Wellington", "Level 10, 10 Brandon Street, Wellington 6011, New Zealand", "+64 4 473 9898", "kln.gov.my/web/nzl_wellington", "Apply at the Malaysian High Commission in Wellington. Check eVisa at windowmalaysia.my."),
    ("New Zealand", "Malta"): ("High Commission of Malta, Wellington (via Canberra)", "261 La Perouse Street, Red Hill ACT 2603, Australia", "+61 2 6290 1724", "mfa.gov.mt", "NZ applicants contact the Malta High Commission in Canberra. Long-stay EU work visa requires advance application."),
    ("New Zealand", "Mexico"): ("Embassy of Mexico, Wellington", "Level 8, 111 Customhouse Quay, Wellington 6011, New Zealand", "+64 4 472 0555", "sre.gob.mx/new-zealand", "Apply at the Mexican Embassy in Wellington. Check visa requirements at consulmex.sre.gob.mx."),
    ("New Zealand", "Netherlands"): ("Embassy of Netherlands, Wellington", "Investment House, 10th Floor, Cnr Ballance & Featherston St, Wellington 6011", "+64 4 471 6390", "netherlands.org.nz", "Apply at the Dutch Embassy in Wellington. Schengen work visa requires VFS Global appointment."),
    ("New Zealand", "Norway"): ("Royal Norwegian Embassy, Wellington", "Level 7, 40 Mercer Street, Wellington 6011, New Zealand", "+64 4 471 2503", "norway.no/new-zealand", "Apply at the Norwegian Embassy in Wellington. WHV requires advance application before departure."),
    ("New Zealand", "Peru"): ("Embassy of Peru, Wellington", "Level 8, 40 Mercer Street, Wellington 6011, New Zealand", "+64 4 499 8087", "embperu.org.nz", "Apply at the Peruvian Embassy in Wellington. Check visa requirements at rree.gob.pe."),
    ("New Zealand", "Philippines"): ("Embassy of the Philippines, Wellington", "Level 9, 50 Manners Street, Wellington 6011, New Zealand", "+64 4 472 9848", "wellingtonpe.dfa.gov.ph", "Apply at the Philippine Embassy in Wellington. Check visa and work permit requirements at dfa.gov.ph."),
    ("New Zealand", "Poland"): ("Embassy of Poland, Wellington", "17 Upland Road, Kelburn, Wellington 6012, New Zealand", "+64 4 475 9453", "wellington.msz.gov.pl", "Apply at the Polish Embassy in Wellington. Long-stay work visa requires in-person appointment and application."),
    ("New Zealand", "Portugal"): ("Embassy of Portugal, Wellington", "Level 5, 186 Willis Street, Wellington 6011, New Zealand", "+64 4 382 7390", "wellington.embaixadaportugal.mne.gov.pt", "Apply at the Portuguese Embassy in Wellington. WHV requires advance application and appointment."),
    ("New Zealand", "Singapore"): ("High Commission of Singapore, Wellington", "17 Kabul Street, Khandallah, Wellington 6035, New Zealand", "+64 4 470 0850", "mfa.gov.sg/wellington", "Apply at the Singapore High Commission in Wellington. Check work pass requirements at mom.gov.sg."),
    ("New Zealand", "Slovakia"): ("Embassy of Slovakia, Wellington (via Canberra)", "47 Culgoa Circuit, O'Malley ACT 2606, Australia", "+61 2 6290 1516", "mzv.sk/canberra", "NZ applicants contact the Slovak Embassy in Canberra. Long-stay work visa requires in-person application."),
    ("New Zealand", "Slovenia"): ("Embassy of Slovenia, Wellington (via Canberra)", "Level 6, 60 Marcus Clarke Street, Canberra ACT 2601, Australia", "+61 2 6243 4830", "canberra.veleposlanistvo.si", "NZ applicants contact the Slovenian Embassy in Canberra. Long-stay work visa requires advance application."),
    ("New Zealand", "Spain"): ("Embassy of Spain, Wellington", "Level 11, 56 The Terrace, Wellington 6011, New Zealand", "+64 4 802 5665", "exteriores.gob.es/new-zealand", "Apply at the Spanish Embassy in Wellington. Long-stay work visa requires appointment and advance application."),
    ("New Zealand", "Sweden"): ("Embassy of Sweden, Wellington", "Level 9, 142 Featherston Street, Wellington 6011, New Zealand", "+64 4 499 9895", "swedenabroad.se/new-zealand", "Apply at the Swedish Embassy in Wellington. WHV requires advance application and appointment."),
    ("New Zealand", "Thailand"): ("Royal Thai Embassy, Wellington", "2 Cook Street, Karori, Wellington 6012, New Zealand", "+64 4 476 8618", "thaiembassy.org.nz", "Apply at the Thai Embassy in Wellington. Check visa at thaievisa.go.th."),
    ("New Zealand", "USA"): ("Embassy of the USA, Wellington", "29 Fitzherbert Terrace, Thorndon, Wellington 6011, New Zealand", "+64 4 462 6000", "nz.usembassy.gov", "Apply for a US visa at the American Embassy in Wellington. Use ustraveldocs.com for DS-160 and appointment."),
    ("New Zealand", "Uruguay"): ("Embassy of Uruguay, Wellington (via Canberra)", "Level 4, 31 Market Street, Sydney NSW 2000, Australia", "+61 2 9262 6398", "embassyofuruguay.com.au", "NZ applicants contact the Uruguayan Embassy in Sydney. Check visa requirements at consulado.mrree.gub.uy."),
    ("New Zealand", "Vietnam"): ("Embassy of Vietnam, Wellington", "Level 5, 230 Willis Street, Wellington 6011, New Zealand", "+64 4 473 5912", "vietnamembassy-newzealand.org", "Apply at the Vietnamese Embassy in Wellington. Check e-visa at evisa.xuatnhapcanh.gov.vn."),

    # Norway as origin
    ("Norway", "Argentina"): ("Embassy of Argentina, Oslo", "Drammensveien 82B, 0271 Oslo, Norway", "+47 22 55 31 00", "eoslo.cancilleria.gob.ar", "Apply at the Argentine Embassy in Oslo. Check visa requirements at migraciones.gob.ar."),

    # Poland as origin
    ("Poland", "Argentina"): ("Embassy of Argentina, Warsaw", "ul. Bukowinska 24 lok. 3, 02-703 Warsaw, Poland", "+48 22 843 0809", "ewarsz.cancilleria.gob.ar", "Apply at the Argentine Embassy in Warsaw. Check visa requirements at migraciones.gob.ar."),
    ("Poland", "Chile"): ("Embassy of Chile, Warsaw", "ul. Staroscinska 1A, 02-516 Warsaw, Poland", "+48 22 849 0854", "chile.gob.cl/poland", "Apply at the Chilean Embassy in Warsaw. WHV requires in-person application before departure."),

    # Portugal as origin
    ("Portugal", "Argentina"): ("Embassy of Argentina, Lisbon", "Rua do Prior 16, 1350-268 Lisbon, Portugal", "+351 21 394 7400", "elisboa.cancilleria.gob.ar", "Apply at the Argentine Embassy in Lisbon. Check visa requirements at migraciones.gob.ar."),
    ("Portugal", "Chile"): ("Embassy of Chile, Lisbon", "Rua Dom Vasco 1, 1400-128 Lisbon, Portugal", "+351 21 301 7270", "chile.gob.cl/portugal", "Apply at the Chilean Embassy in Lisbon. WHV requires in-person application before departure."),
    ("Portugal", "Peru"): ("Embassy of Peru, Lisbon", "Av. Casal Ribeiro 14, 5th Floor, 1000-092 Lisbon, Portugal", "+351 21 319 6710", "embperu.pt", "Apply at the Peruvian Embassy in Lisbon. Check visa requirements at rree.gob.pe."),

    # Slovakia as origin
    ("Slovakia", "Argentina"): ("Embassy of Argentina, Bratislava (via Vienna)", "Goldschmiedgasse 2/1, 1010 Vienna, Austria", "+43 1 533 8585", "eavie.cancilleria.gob.ar", "Slovak applicants contact the Argentine Embassy in Vienna. Check visa requirements at migraciones.gob.ar."),
    ("Slovakia", "Chile"): ("Embassy of Chile, Bratislava (via Prague)", "Muchova 9, 160 00 Prague 6, Czech Republic", "+420 233 371 380", "chile.gob.cl/slovakia", "Slovak applicants contact the Chilean Embassy in Prague. WHV requires in-person application."),

    # South Korea as origin
    ("South Korea", "Argentina"): ("Embassy of Argentina, Seoul", "11F, Tower B, Lexus Building, 22 Teheran-ro 92-gil, Gangnam-gu, Seoul 06180", "+82 2 568 0243", "eseul.cancilleria.gob.ar", "Apply at the Argentine Embassy in Seoul. Check visa requirements at migraciones.gob.ar."),
    ("South Korea", "Belgium"): ("Embassy of Belgium, Seoul", "Bd Flemish, 6F, 134 Itaewon-ro, Yongsan-gu, Seoul 04401", "+82 2 749 0381", "southkorea.diplomatie.belgium.be", "Apply at the Belgian Embassy in Seoul. Long-stay EU work visa requires in-person application."),
    ("South Korea", "Chile"): ("Embassy of Chile, Seoul", "Namsan Square Building, 13F, 173 Toegye-ro, Jung-gu, Seoul 04554", "+82 2 2711 9800", "chile.gob.cl/south-korea", "Apply at the Chilean Embassy in Seoul. WHV requires in-person application before departure."),
    ("South Korea", "Czech Republic"): ("Embassy of Czech Republic, Seoul", "1-121 Sinmun-ro 2-ga, Jongno-gu, Seoul 03159", "+82 2 725 6765", "mzv.cz/seoul", "Apply at the Czech Embassy in Seoul. Long-stay work visa requires advance appointment and application."),
    ("South Korea", "Denmark"): ("Royal Danish Embassy, Seoul", "5F, Hana Daetoo Securities Building, 23 Eulji-ro, Jung-gu, Seoul 04539", "+82 2 795 4187", "sydkorea.um.dk", "Apply at the Danish Embassy in Seoul. Schengen visa via VFS Global or in person at the embassy."),
    ("South Korea", "Hungary"): ("Embassy of Hungary, Seoul", "2F, 13-11 Hannam-daero 20-gil, Yongsan-gu, Seoul 04418", "+82 2 792 2105", "seoul.mfa.gov.hu", "Apply at the Hungarian Embassy in Seoul. Long-stay WHV requires in-person application."),
    ("South Korea", "Italy"): ("Embassy of Italy, Seoul", "1-398 Hannam-dong, Yongsan-gu, Seoul 04419", "+82 2 796 0491", "ambseoul.esteri.it", "Apply at the Italian Embassy in Seoul. Long-stay work visa requires appointment and advance application."),
    ("South Korea", "Netherlands"): ("Embassy of Netherlands, Seoul", "10F, Jeongdong Building, 21-15 Jeongdong-gil, Jung-gu, Seoul 04518", "+82 2 311 8600", "netherlands.or.kr", "Apply at the Dutch Embassy in Seoul. Schengen work visa requires VFS Global appointment."),
    ("South Korea", "Poland"): ("Embassy of Poland, Seoul", "12F, Mapo Tower, 418 Mapo-daero, Mapo-gu, Seoul 04191", "+82 2 723 9681", "seoul.msz.gov.pl", "Apply at the Polish Embassy in Seoul. Long-stay work visa requires in-person appointment and application."),
    ("South Korea", "Portugal"): ("Embassy of Portugal, Seoul", "2nd Floor, Hannam Bldg, 737-32 Hannam-dong, Yongsan-gu, Seoul 04419", "+82 2 3675 2251", "seoul.embaixadaportugal.mne.gov.pt", "Apply at the Portuguese Embassy in Seoul. WHV requires advance application and appointment."),
    ("South Korea", "Spain"): ("Embassy of Spain, Seoul", "Jeongdong Building, 7F, 21-15 Jeongdong-gil, Jung-gu, Seoul 04518", "+82 2 794 3581", "exteriores.gob.es/south-korea", "Apply at the Spanish Embassy in Seoul. Long-stay work visa requires appointment and advance application."),
    ("South Korea", "Sweden"): ("Embassy of Sweden, Seoul", "8th Floor, Jeongdong Building, 21-15 Jeongdong-gil, Jung-gu, Seoul 04518", "+82 2 3703 3700", "swedenabroad.se/south-korea", "Apply at the Swedish Embassy in Seoul. WHV requires advance application and appointment."),
    ("South Korea", "USA"): ("Embassy of the USA, Seoul", "188 Sejong-daero, Jongno-gu, Seoul 03141", "+82 2 397 4114", "kr.usembassy.gov", "Apply for a US visa at the American Embassy in Seoul. Use ustraveldocs.com for DS-160 and appointment."),

    # Spain as origin
    ("Spain", "Philippines"): ("Embassy of the Philippines, Madrid", "Calle Hermanos Bécquer 7, 28006 Madrid, Spain", "+34 91 782 3830", "madridpe.dfa.gov.ph", "Apply at the Philippine Embassy in Madrid. Check visa and Special Work Permit requirements at dfa.gov.ph."),

    # Sweden as origin
    ("Sweden", "Argentina"): ("Embassy of Argentina, Stockholm", "Tyrgatan 10, 114 27 Stockholm, Sweden", "+46 8 663 2585", "estocolmo.cancilleria.gob.ar", "Apply at the Argentine Embassy in Stockholm. Check visa requirements at migraciones.gob.ar."),
    ("Sweden", "Chile"): ("Embassy of Chile, Stockholm", "Birger Jarlsgatan 37, 111 45 Stockholm, Sweden", "+46 8 440 3420", "chile.gob.cl/sweden", "Apply at the Chilean Embassy in Stockholm. WHV requires in-person application before departure."),
    ("Sweden", "Uruguay"): ("Embassy of Uruguay, Stockholm", "Ingmar Bergmans gata 6, 114 34 Stockholm, Sweden", "+46 8 667 0760", "estocolmo.mrree.gub.uy", "Apply at the Uruguayan Embassy in Stockholm. Check visa requirements at consulado.mrree.gub.uy."),

    # Taiwan as origin (remaining)
    ("Taiwan", "Belgium"): ("Taipei Representative Office, Brussels", "Rue Guillaume Stocq 2, 1050 Brussels, Belgium", "+32 2 511 0687", "roc-taiwan.org/be_en", "Apply for a Belgian visa at the Belgian Embassy in Taipei. The Taipei Representative Office in Brussels provides consular support."),
    ("Taiwan", "Czech Republic"): ("Taipei Economic and Cultural Office, Prague", "Korunní 110/2588, 101 00 Prague 10, Czech Republic", "+420 257 531 798", "roc-taiwan.org/cz_en", "Apply for a Czech visa at the Czech Institute in Taipei. The TECO in Prague provides consular support."),
    ("Taiwan", "Hungary"): ("Taipei Representative Office, Budapest", "Bajcsy-Zsilinszky út 12, 2nd Floor, 1051 Budapest, Hungary", "+36 1 266 2884", "roc-taiwan.org/hu_en", "Apply for a Hungarian visa at the Hungarian Trade Office in Taipei. TECO in Budapest provides consular support."),
    ("Taiwan", "Mainland China"): ("Straits Exchange Foundation (SEF)", "No. 65, Hangzhou South Road, Sec. 1, Zhongzheng District, Taipei 10065", "+886 2 2396 5000", "sef.org.tw", "Cross-strait travel uses special arrangements. Contact the SEF for residency and travel permit enquiries."),
    ("Taiwan", "Netherlands"): ("Netherlands Office, Taipei", "5F, No. 133 Minsheng East Road, Sec. 3, Zhongshan District, Taipei 10544", "+886 2 2713 5110", "roc-taiwan.org/nl_en", "Apply for a Dutch visa at the Netherlands Office in Taipei. Schengen work visa requires VFS Global appointment."),
    ("Taiwan", "Poland"): ("Taipei Representative Office, Warsaw", "Szucha Avenue 17/2, 00-580 Warsaw, Poland", "+48 22 625 2483", "roc-taiwan.org/pl_en", "Apply for a Polish visa at the Polish Institute in Taipei. TECO in Warsaw provides consular support."),
    ("Taiwan", "Slovakia"): ("Taipei Economic and Cultural Office, Bratislava", "Dunajská 4, 811 08 Bratislava, Slovakia", "+421 2 5296 2871", "roc-taiwan.org/sk_en", "Apply for a Slovak visa via the Slovak Embassy covering Taiwan. TECO in Bratislava provides consular support."),
    ("Taiwan", "USA"): ("Taipei Economic and Cultural Representative Office (TECRO), Washington D.C.", "4201 Wisconsin Avenue NW, Washington, DC 20016, USA", "+1 202 895 1800", "roc-taiwan.org/us_en", "Apply for a US visa at the American Institute in Taiwan (AIT). TECRO in Washington handles Taiwan consular matters."),

    # USA as origin (remaining)
    ("USA", "Mainland China"): ("Embassy of China, Washington D.C.", "3505 International Place NW, Washington, DC 20008, USA", "+1 202 495 2266", "us.china-embassy.gov.cn", "Apply at the Chinese Embassy in Washington D.C. or a Chinese Consulate-General. Use the COVA visa portal."),
    ("USA", "Singapore"): ("Embassy of Singapore, Washington D.C.", "3501 International Place NW, Washington, DC 20008, USA", "+1 202 537 3100", "mfa.gov.sg/washington", "Apply at the Singapore Embassy in Washington D.C. Check work pass requirements at mom.gov.sg."),

    # United Kingdom as origin (remaining)
    ("United Kingdom", "Andorra"): ("Andorra Delegation in London", "63 Westover Road, London SW18 2RF, United Kingdom", "+44 20 8874 4806", "exteriors.ad", "Andorra has no formal embassy in the UK. Contact the Andorran delegation for visa and residency enquiries."),
    ("United Kingdom", "Iceland"): ("Embassy of Iceland, London", "2A Hans Street, London SW1X 0JE, United Kingdom", "+44 20 7259 3999", "iceland.org.uk", "Apply at the Icelandic Embassy in London. WHV requires advance in-person application before departure."),
    ("United Kingdom", "India"): ("High Commission of India, London", "India House, Aldwych, London WC2B 4NA, United Kingdom", "+44 20 7836 8484", "hcilondon.gov.in", "Apply for an Indian visa via the Indian Visa Application Centre (VFS Global). E-visa available at indianvisaonline.gov.in."),
    ("United Kingdom", "Mainland China"): ("Embassy of China, London", "49-51 Portland Place, London W1B 1JL, United Kingdom", "+44 20 7299 4049", "chinese-embassy.org.uk", "Apply at the Chinese Embassy in London. Use COVA visa portal or VFS Global for applications."),
    ("United Kingdom", "Monaco"): ("Monaco Consulate, London", "7 Upper Grosvenor Street, London W1K 2LX, United Kingdom", "+44 20 7318 3760", "gouv.mc", "Apply at the Monaco Consulate in London. Monaco follows French Schengen visa rules for short stays."),
    ("United Kingdom", "San Marino"): ("Embassy of Italy, London (covers San Marino)", "14 Three Kings Yard, London W1K 4EH, United Kingdom", "+44 20 7312 2200", "amblondra.esteri.it", "San Marino has no formal embassy in the UK. Contact the Italian Embassy in London which covers San Marino matters."),
    ("United Kingdom", "Singapore"): ("High Commission of Singapore, London", "9 Wilton Crescent, London SW1X 8SP, United Kingdom", "+44 20 7235 8315", "mfa.gov.sg/london", "Apply at the Singapore High Commission in London. Check work pass requirements at mom.gov.sg."),
    ("United Kingdom", "USA"): ("Embassy of the USA, London", "33 Nine Elms Lane, London SW11 7US, United Kingdom", "+44 20 7499 9000", "uk.usembassy.gov", "Apply for a US visa at the American Embassy in London. Use ustraveldocs.com for DS-160 and appointment booking."),
}

HTML_TEMPLATE = '''            <!-- Authority Contact -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="embassy-card p-4 rounded bg-light border">
                        <h5 class="mb-3"><i class="fa fa-building-columns mr-3 text-primary"></i>{name}</h5>
                        <p class="mb-2"><strong>Address:</strong> {address}</p>
                        <p class="mb-2"><strong>Phone:</strong> {phone}</p>
                        <p class="mb-2"><strong>Website:</strong> <a href="https://{website}" target="_blank">{website}</a></p>
                        <p class="small mb-0 text-muted"><strong>Application Note:</strong> {note}</p>
                    </div>
                </div>
            </div>'''

import re, os

OLD_BLOCK_PATTERN = re.compile(
    r'            <!-- Authority Contact -->.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)

def parse_filename(fname):
    name = fname.replace('.html', '')
    parts = name.split('-to-')
    if len(parts) == 2:
        origin = parts[0].replace('-', ' ')
        dest = parts[1].replace('-', ' ')
        return origin, dest
    return None, None

updated = 0
skipped = 0

for fname in os.listdir(BASE):
    if not fname.endswith('.html'):
        continue
    origin, dest = parse_filename(fname)
    if not origin or not dest:
        continue
    key = (origin, dest)
    if key not in EMBASSIES:
        skipped += 1
        continue

    name, address, phone, website, note = EMBASSIES[key]
    new_block = HTML_TEMPLATE.format(name=name, address=address, phone=phone, website=website, note=note)

    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = OLD_BLOCK_PATTERN.sub(new_block, content)
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated += 1
    else:
        skipped += 1

print(f"Updated: {updated}")
print(f"Skipped: {skipped}")
