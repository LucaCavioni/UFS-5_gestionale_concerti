import json
from tkinter.messagebox import NO
from colorama import deinit
from matplotlib import artist
# from pymongo import MongoClient
from bson import ObjectId, objectid as bid
from pymongo import MongoClient

# inserire di defolt il prjc dei campi in comune con il ticket
# db.COLLECTION_NAME.find().sort({KEY:1}) da implemetare?


class GestioneConcerti:
    def __init__(self, mongoConnectio="mongodb://localhost:27017", tkt_len=8):
        self.len_ticket = tkt_len
        self.client = MongoClient(mongoConnectio)

    def getConcerto(self, query={}, prjc=None, limiti_=None):
        if limiti_ != None:
            res = self.client['UFS-5']['Concert'].find(
                filter=query, projection=prjc, limit=limiti_)
        else:
            res = self.client['UFS-5']['Concert'].find(
                filter=query, projection=prjc)

        return res

    def nearConcerto(self, pos=[0, 0], max=None, min=None):
        quary = {
            "luogo.posizione": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        'coordinates': pos
                    }
                }
            }
        }
        if(max != None):
            quary["luogo.posizione"]["$near"]['$maxDistance'] = max
        if(min != None):
            quary["luogo.posizione"]["$near"]['$maxDistance'] = min
        temp = self.client['UFS-5']['Concert'].find(quary)
        lista = []
        for e in temp:
            lista.append(e)
        return lista

    def setConcerto(self, mydict, new=False):
        if type(mydict) is dict:
            mydict = [mydict]
        if new:
            return self.client['UFS-5']['Concert'].insert_many(mydict)
        else:
            updated = []
            for e in mydict:
                myquery = {"_id": e.pop('_id')}
                updated.append(
                    self.client['UFS-5']['Concert'].update_one(myquery, {"$set": e}))
                return updated

    def removeConcerto(self, toDelete={'_id': None}):
        delited = []
        if type(toDelete) is dict:
            if toDelete['_id'] == None:
                return self.client['UFS-5']['Concert'].delete_many({})
            toDelete = [toDelete]
        for e in toDelete:
            delited.append(self.client['UFS-5']['Concert'].delete_one(e))
            return delited

    def getTicket(self, query={}, prjc=None, limiti_=None):
        if limiti_ != None:
            res = self.client['UFS-5']['Ticket'].find(
                filter=query, projection=prjc, limit=limiti_)
        else:
            res = self.client['UFS-5']['Ticket'].find(
                filter=query, projection=prjc)
        return res

    # inserire la get del concerto con la query per trovare il concerto desiderato
    # creazione nuovo ticket con formato nserie = ZZ-00000000
    # controllo duplicati posti
    # creazione posto random
    def setTicket(self, mydict, new=False):
        update = []
        if type(mydict) is dict:
            mydict = [mydict]
        self.len_ticket
        if new:
            for i in mydict:
                zona_Posti = self.getConcerto(
                    {"_id": ObjectId(i['concerto'])}, {'posti': 1, 'data': 1})
                for e in zona_Posti[0]['posti']:
                    if e['area'] == i['posti']['area']:
                        prezzo = e['prezzo']
                        area = e['area']
                        nPostorim = e['n_postiRimasti']-1
                        nPostotot = e['n_postiTotali']
                        break

                data = zona_Posti[0]['data']
                print(self.setConcerto({"_id": ObjectId(i['concerto']), 'posto': {
                    'n_postiRimasti': nPostorim}})[0])
                if nPostorim < 0:
                    # ahah, scemo! = errore posti finiti
                    return 'ahah, scemo!'
                nPosto = nPostotot-nPostorim
                nPosto = str(nPosto)
                zeroLen = self.len_ticket-len(nPosto)
                n_serie = area[:2]+'0'*zeroLen+nPosto
                i['nserie'] = n_serie
                i['prezzo'] = prezzo
                i['data'] = data
            print(mydict)
            return self.client['UFS-5']['Ticket'].insert_many(mydict)
        else:
            for i in mydict:
                myquery = {"_id": i.pop('_id')}
                update.append(
                    self.client['UFS-5']['Ticket'].update_one(myquery, {"$set": i}))
                return update

    def removeTicket(self, toDelete={'_id': None}):
        delited = []
        if type(toDelete) is dict:
            if toDelete['_id'] == None:
                return self.client['UFS-5']['Ticket'].delete_many({})
            toDelete = [toDelete]
        for e in toDelete:
            delited.append(self.client['UFS-5']['Ticket'].delete_one(e))
            return delited


if __name__ == "__main__":

    temp = GestioneConcerti()
    with open('concerti.json') as json_file:
        new_concerto = json.load(json_file)
    while True:
        print("""      
            Cosa vuoi fare?
# 1. Inserisci concerto massivo
# 2. Inserisci un concerto
# 3. Modifica concerto
# 4. Cerca concerto vicino a milano
# 5. Stampa tutti i concerti
# 6. Elimina tutti concerti
# 7. Inserisci ticket
# 8. Modifica ticket
# 9. Stampa tutti i ticket
# 10. Elimina tutti ticket
# 11. Elimina tuttoù
# 0. Termina sessione
            
            # 0. Termina sessione
            """)

        try:
            scelta = int(input("Inserisci il numero della tua scelta: "))

            if scelta == 0:
                print("Alla prossima")
                break

            elif scelta == 1:
                a = temp.setConcerto(new_concerto, True)
                for e in a.inserted_ids:
                    print('ID Inserito     -----  '+str(e))

            elif scelta == 2:
                print(new_concerto[4])
                a2=temp.setConcerto(new_concerto[4], True)
                for e in a2.inserted_ids:
                    print('ID Inserito     -----  '+str(e))

            elif scelta == 3:
                titolo = input('dammi il nome di un concerto che ti piace <3')
                found_concert = temp.getConcerto(prjc={'artisti': 1, '_id': 1})
                found_concert[0]['tour'] = titolo
                a = temp.setConcerto(found_concert[0])
                print(a)

            elif scelta == 4:
                near = temp.nearConcerto([45.48307873172699, 9.13053663872388])
                print(near)

            elif scelta == 5:
                for a in temp.getConcerto():
                    print(a)
            elif scelta == 6:
                temp.removeConcerto()

            elif scelta == 7:
                found_concert = temp.getConcerto(prjc={'artisti': 1, '_id': 1})
                name= input("Nome:")
                surname= input("Cognome:")
                nome_conc = input("Nome del concerto:").lower()
                try:
                    while True:
                        acquir= int(input('''L'acquirente sei tu?
                        # 1. Sì
                        # 2. No
                        '''))
                        if acquir == 1:
                            acquirente= f"{name} {surname}"
                            break
                        elif acquir == 2:
                            acquirente= input("Inserisci nome e cognome dell'acquirente")
                            break
                        else:
                            print("Inserisci un numero tra quelli indicati")
                while True:            
                    zona= input("In che zona del luogo vuoi prenotare?")
                    if zona in new_concerto["posti"]["area"]:
                        if new_concerto["titolo"] == nome_conc or new_concerto["tour"] == nome_conc:
                            break
                        else:
                            print("Il concerto non esiste")
                    else:
                        print("La zona non esiste")


                    
                    
                except:
                    print("Inserisci un numero")
                
                new_ticket = {
                    "concerto": str(found_concert[0]['_id']),
                    "nome": name,
                    "cognome": surname,
                    "acquirente": acquirente,
                    "posti": {
                        "area": "prato gold",
                    }
                }
                temp.setTicket(new_ticket, True)

            elif scelta == 8:
                found_ticket = temp.getTicket()
                if len(found_ticket) > 0:
                    acquirente = input(
                        'inserisci il nome di un acquirente a che ti piace <3')
                    found_ticket[0]['acquirente'] = acquirente
                    print(temp.setTicket(found_ticket[0]))

            elif scelta == 9:
                for a in temp.getTicket():
                    print(a)

            elif scelta == 10:
                temp.removeTicket()

            elif scelta == 11:
                temp.removeConcerto()
                temp.removeTicket()
            else:
                print("Inserisci un numero tra quelli indicati")
            

        except:
            print("Devi inserire un numero")
        try:          
            again= int(input('''Vuoi eseguire altre operazioni?
            # 1. Sì
            # Altri numeri: No
            ''')
            if again == 1:
                pass
            else:
                break               
      
                       
        except:
              print("Inserisci un numero")
                   
