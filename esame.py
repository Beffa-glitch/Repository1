class ExamException(Exception):
    
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name=name

    def get_data(self):
        
        #verifica che il nome del file inserito sia una stringa
        if not isinstance(self.name, str):
            raise ExamgitException("non è stato inserito un nome di un file")

        #controllo esistenza del file

        try:
            
            open(self.name,"r")

        except:
            
            raise ExamException("file non esistente")

        file_origin=open(self.name,"r")
        
        valori=[]
        
        file=file_origin.readlines()
        
        for linea in file:
            elemento=linea.split(',')
            
            if elemento[0]!='epoch':

                data=elemento[0]

                #conversione del tempo epoch e della temperatura rispettivamente in variabili di tipo int e float

                if type(data) is str:

                    try:

                        data=float(data)

                        data=int(data)

                    except:

                        pass

                if type(data) is float:

                    data=int(data)                
            
                    
                numero=elemento[1]

                #controllo della validità del dato per operazioni e calcoli di minimo, massimo e media giornaliera

                if((type(data) is int or (type(numero) is int or type(numero) is float)) and data>=0):
                    
                    try:
                        valori.append([int(data),float(numero)])

                    except:
                        
                        pass       
                
                else:
                                   
                    pass

        return valori

def daily_stats(time_series):
    temperature=[]
    massimo=time_series[0][1]
    minimo=time_series[0][1]
    media=0
    #n rappresenta il numero di dati appartenente ad uno stesso giorno
    n=1

    print("\n\n")

    for i in range(len(time_series)-1):
        data=time_series[i][0]-time_series[i][0]%86400

        #verifica della crescenza in senso stretto degli epoch

        if(time_series[i+1][0]<=time_series[i][0]):
            raise ExamException("lista dati non ordinata")

        #riassegnamento di massimo e minimo a seconda dell'esito del loro confronto col dato

        if(time_series[i][1]<minimo):
            minimo=time_series[i][1]

        if(time_series[i][1]>massimo):
            massimo=time_series[i][1]

        #riassegnamento di massimo e minimo (esclusivamente nell'ultimo giorno) a seconda dell'esito del loro confronto con l'ultimo valore della lista, non considerato dal ciclo


        if(time_series[len(time_series)-1][0]-time_series[len(time_series)-1][0]%86400 == data):

            if(time_series[len(time_series)-1][1]>massimo):

                massimo=time_series[len(time_series)-1][1]

            if(time_series[len(time_series)-1][1]<minimo):
                
                minimo=time_series[len(time_series)-1][1]

        #incremento somma giornaliera, per il calcolo della media

        media+=time_series[i][1]

        #calcolo statistiche giornaliere quando si riscontra che il successivo apparterra' al giorno seguente

        if(time_series[i+1][0]-time_series[i+1][0]%86400 != data):

            media=media/n
            temperature.append([minimo, massimo, media])
            massimo=time_series[i+1][1]
            minimo=time_series[i+1][1]
            media=0
            n=0

        #calcolo statistiche giornaliere dell'ultimo giorno, sapendo che ha almeno 2 dati

        elif(time_series[len(time_series)-1][0]-time_series[len(time_series)-1][0]%86400 == time_series[len(time_series)-2][0]-time_series[len(time_series)-2][0]%86400 and i==len(time_series)-2):

            media=(media+time_series[len(time_series)-1][1])/(n+1)
            temperature.append([minimo, massimo, media])

        n+=1

    #calcolo statistiche dell'ultimo giorno sapendo che e' rappresentato da una e una sola rilevazione

    if(time_series[len(time_series)-1][0]-time_series[len(time_series)-1][0]%86400 != time_series[len(time_series)-2][0]-time_series[len(time_series)-2][0]%86400):
        temperature.append([time_series[len(time_series)-1][1], time_series[len(time_series)-1][1], time_series[len(time_series)-1][1]])
    
    return temperature

time_series_file = CSVTimeSeriesFile(name='data.csv')

time_series = time_series_file.get_data()

#stampa valori nel file considerati accettabili dalle specifiche
print("dati: \n")
for line in time_series:
    print(line, "\n")


stats = daily_stats(time_series)

print("statistiche giornaliere [minimo, massimo, media]: \n")

#stampa statistiche giornaliere
for line in stats:
    print(line, "\n")

