================================TEMA 1 ASC==============================

Abordare generala:
    pentru a memora informatiile utile din CSV am folosit un dictionar in care cheile sunt 
intrebarile si valorile sunt liste ce contin dictionare formate din numele statelor(cheie)
si o lita de valori(DATA_VALUES) ce reprezinta values.
    pentru requesturile care necesitau si categoriile am folosit alt dictionar.Implenetarea este
aproximativ aceeasi,singura diferneta este ca in loc sa pun numele statului ca si cheie,am pus
un tuplu de 3 elemente ca si cheie(nume_stat,stratificaton,stratificatonCategory)
    pentru fiecare request,verific sa vad daca trebuiesc facute calcule si daca da,adaug
job ul in coada.
    In treadpool de task_runner, scot cate un job din coada,calculez operatiile cerute si scriu
rezultatele in fisier.
    Implementarea este naiva,deoarece nu retin calculele facute,si altfel,pentru fiecare request
trebuie sa calculez de fiecare data.
    Tema a fost utila deoarece am aprofundat notiunile noi de pytohn.

Data_ingestor:
    am folosit o functie in care verific de care tip trebuie sa fie dicitonarul
    citesc linie cu linie din CSV si extrag campurile necesare(intrebare,stat,valoare/valori)
    daca nu gasesc o intrebare in dictionar,o adaug ca si cheie si aloc o lista pentru valori
    adaug statul la cheia care contine intrebarea de pe linia citita
    adaug valoarea la statul si la intrebarea corespunzatoare

MyLogging:
    am creat un logger pentru a afisa informatiile de la nivelul info
    am folosit RotatingFileHandler cu maxim 5 fisiere de backup
    pentru a afisa data si ora in formatul cerut am folosit functia formatTime(m am folosit de CHATGPT)

Routes:
    pentru ficare ruta de post m am folosit de o functie ajutatoare pentru a adauga job ul in coada
            functia "complete_request"
    pentru fiecare endpoint,notez in log inatrea si iesirea
    ma folosesc de o lista de dictionare in care notez statusul pentru fiecare job
    pentru a extrage numarul de job uri ramase,am o variabila in care retin numarul de job uri terminate

Complete_request:
    primesc ca si parametri endpointul si datele din request
    Folosesc o varibila event pentru a vedea daca s a apelat graceful_shutdown
    in functie de endpointul dat ca paramentru adaug informatiile necesare in coada:
        trimit id ul,datele din request,tipul de calcul si datele parsate din CSV
        (trimit doar valorile din dictonar care corespund cu intrebarea aleasa)(data[question])
    pentru cazurile best sau worst,am luat o lista de intrebari care sunt ,,pe dos,, cu valorile
si in functie de intrebare pun in coada tipul de calcul(best sau worst)
    adaug in dictionarul de status id ul job ului si statusul job ului curent

Threadpool:
    verific existenta directorului results,iar in caz negativ il creez
    creez variabilele necesare: coada,event ul de stop,nr de job uri terminate,lista de status
    creez threadurile TaskRunner si le pornesc

TaskRunner:
    fiecare thread din pool astepata pana exista job uri in coada.Fiecare thread verifica
tipul taskului si apeleaza functia de calculare a operatiei
    dupa terminarea functiei de calcul,rezultatul intors este dat ca parametru functiei
pentru a scrie rezulatul in fisier
    dupa termniarea de scris in fisier,se marcheaza statusul job ului  cu DONE
    la unele functii de calcul am folosit CHATGPT


Implementare:
    intregul enunt al temei este implementat
    nu am intampinat dificultati
    lucruri interesnate: lucrul cu thread uri,CSV

Git:
https://github.com/StefanIv21/LE_Stats_Sportif


        
        



    



    



