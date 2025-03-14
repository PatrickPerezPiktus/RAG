# Konzeption und Implementierung eines Wissensmanagementsystems basierend auf Retrieval-Augmented Generation
## Quellcode zur Bachelorarbeit 
### Abstract 
Das Ziel dieser Arbeit ist die Modellierung und Implementierung eines KI basiertem Assistent-Systems für die Handhabung von internem Wissen. Konkrete Methodik, welche dabei genutzt werden soll, ist Retrieval-Augmented Generation. Im theoretischen Teil werden die grundlegenden damit verbundene Themen erklärt und eingeordnet. Der Modellierungsteil der Arbeit beschäftigt sich mit der Evaluation und Auswahl von notwendigen Technologien, die bei der Entwicklung verwendet werden sollen. Anschließend wird das zu implementierende Wissensmanagementsystem geplant und modelliert. Im Umsetzungsteil wird das vorangegangene geplante System umgesetzt und dabei anfallende Abweichungen beschrieben und begründet. Abschließend wird ein Fazit aus den gewonnenen Erkenntnissen, die während der Entwicklung angefallen sind, gezogen. Somit zeigt dieses Projekt die Machbarkeit und den damit einhergehenden Mehrwert für KI basierte Systeme.


### Ausführen auf VM-Instanz

Ports öffnen (siehe docker-compose)

sudo apt update
sudo apt install -y docker.io

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt install -y git
git clone https://github.com/PatrickPerezPiktus/RAG.git

cd RAG
nano rag-poc/.env

// env vars setzen 
LANGCHAIN_API_KEY=
LANGCHAIN_TRACING_V2=
OPENAI_API_KEY=
JWT_SECRET_KEY=
CONFLUENCE_SECRET_KEY=
COHERE_API_KEY=
SQL_SERVER=db
SQL_PW=password
SQL_USER=user
CHROMA_SERVER=chromadb 

im Frontend muss die URL des backend in axios configuriert werden (aktuell localhost)

sudo docker-compose up -d 

je nach performance kann es sein, dass das backend versucht wird zu starten obwohl Abhängigkeiten noch nicht vorhanden sind. Ein Nachträgliche Starten hilft

sudo docker-compose up -d backend
