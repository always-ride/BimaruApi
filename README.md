# Web API rund um das Bimaru-Universum

Hier sollen die Lösungen für verschiedene Bimaru-Aufgabenstellungen gefunden und retour geliefert werden.

## Voraussetzungen

Sicherstellen dass Java, Maven und Docker laufen.

```ps
java -version
mvn -v
docker -v
```

Depencendies laden.

```ps
mvn clean install
```

## Erstellung eines neuen Builds, separate Ausführung der Tests und Start der Anwendung 

```ps
mvn clean package
mvn test
mvn spring-boot:run
```

Die Anwendung ist nun unter http://localhost:8080 erreichbar.

## Docker

Docker-Image bauen und Container starten:

```ps
docker build -t bimaru-api .
docker run -p 8080:8080 bimaru-api
```

## Deployment

Unter [bimaruapi.fly.dev/api/](https://bimaruapi.fly.dev/api/) kann das Projekt eingesehen werde.
