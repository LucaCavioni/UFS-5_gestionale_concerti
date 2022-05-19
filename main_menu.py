import mongoTest 


gestione_concerti= mongoTest.GestioneConcerti()

while True:
    print("""
          
Cosa vuoi fare?
    # 1. Gestire concerti
    # 2. Gestire biglietti
    # 3. Termina sessione

          """)
    try:
        risp= int(input("Inserisci il numero della tua scelta: "))
        if risp == 1:
            while True:
                print("""
                      
Cosa vuoi fare?
    # 1. Inserisci concerto
    # 2. Modifica concerto
    # 3. Elimina concerto
    # 4. Termina sessione
    
    """)
                try:
                    scelta = int(input("Inserisci il numero della tua scelta: "))
                    if scelta == 1:
                        lista_concerti=[]
                        while True:
                            new_concerto={}
                            
                    
                    elif scelta == 2:
                        gestione_concerti.nearConcerto()
                    elif scelta == 3:
                        gestione_concerti.setConcerto()
                    elif scelta == 4:
                        break
                    else:
                        print("Questo numero non esiste")
                except:
                    print("Devi inserire un numero")
        elif risp == 2:
            while True:
                print("""
                      
Cosa vuoi fare?
    # 1. Get Ticket
    # 2. Set Ticket
    # 3. Remove Ticket
    # 4. Esci
    
    """)
                try:
                    scelta = int(input("Inserisci il numero della tua scelta: "))
                    if scelta == 1:
                        
                        gestione_concerti.getTicket()
                    elif scelta == 2:
                        gestione_concerti.setTicket()
                    elif scelta == 3:
                        gestione_concerti.removeTicket()
                    elif scelta == 4:
                        break
                    else:
                        print("Inserisci un numero tra 1 e 4")
                except:
                    print("Devi inserire un numero")
        elif risp == 3:
            break
        else:
            print("Inserisci un numero da 1 a 3")
    except:
        print("Devi inserire un numero che corrisponde ad una scelta")
    



