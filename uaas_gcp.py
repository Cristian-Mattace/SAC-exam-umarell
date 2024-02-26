from google.cloud import firestore
from google.cloud import pubsub_v1
from google.cloud.firestore_v1.base_query import FieldFilter
import json

publisher = pubsub_v1.PublisherClient()
project_id = "cmgeneralsac"
topic_name = "new_cantiere"
project_path = f"projects/{project_id}"
topic_path=publisher.topic_path(project_id, topic_name)


class Uaas(object):
    def __init__(self):
        self.db = firestore.Client()
    

    def check_cap(self, cantiere):
        try:
            if cantiere['cap'] < 0 or cantiere['cap'] > 99999:
                return False
            else:
                return True
        except:
            return False
    
    def check_indirizzo(self, cantiere):
        try:
            if cantiere['indirizzo']:
                return True
        except:
            return False
    
    def check_dati_umarell(self, umarell):
        try:
            if umarell['nome'] and umarell['cognome']:
                return True
        except:
            return False




    def add_cantiere(self, idCantiere, cantiere):
        
        if not self.check_cap(cantiere):
            return None, 400
        
        if not self.check_indirizzo(cantiere):
            return None, 400
        
        
        if self.db.collection('cantiere').document(idCantiere).get().exists:
            return None, 409
        else:
            self.db.collection('cantiere').document(idCantiere).set(cantiere)

            res = publisher.publish(topic_path, json.dumps(cantiere).encode('utf-8'))
            print(cantiere, res.result())

        return cantiere, 201


    def clean(self):
        for docs in self.db.collection('cantiere').stream():
            doc_ref = docs.reference
            doc_ref.delete()
        for docs in self.db.collection('umarell').stream():
            doc_ref = docs.reference
            doc_ref.delete()

    
    def get_cantiere(self, idCantiere):

        cantiere = self.db.collection('cantiere').document(idCantiere).get()
        if not cantiere.exists:
            return None, 404
        else:
            return cantiere.to_dict(), 200
    

    def get_cantieri_by_cap(self, cap):
        cantieri = []
        cap = int(cap)
        
        for cantiere in self.db.collection('cantiere').where(filter=FieldFilter("cap", "==", cap)).stream():
            cantieri.append(cantiere.to_dict()['indirizzo'])
        
        return cantieri
        
    def add_umarell(self, idUmarell, umarell):
        
        if not self.check_cap(umarell):
            return None, 400
        
        if not self.check_dati_umarell(umarell):
            return None, 400
        
        if self.db.collection('umarell').document(idUmarell).get().exists:
            return None, 409
        else:
            self.db.collection('umarell').document(idUmarell).set(umarell)

        return umarell, 201
    
    def get_umarell(self, idUmarell):

        umarell = self.db.collection('umarell').document(idUmarell).get()
        if not umarell.exists:
            return None, 404
        else:
            return umarell.to_dict(), 200
    

    def get_umarell_by_cap(self, cap):
        umarells = []
        cap = int(cap)
        
        for umarell in self.db.collection('umarell').where(filter=FieldFilter("cap", "==", cap)).stream():
            print(umarell)
            identita = umarell.to_dict()['nome'] + " " + umarell.to_dict()['cognome']
            umarells.append(identita)
        
        return umarells

