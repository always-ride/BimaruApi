# Java/Spring-Version

## Voraussetzungen

Sicherstellen dass Java, Maven und Docker laufen.

```powershell
java -version
mvn -v
docker -v
```

Depencendies laden.

```powershell
mvn clean install
```

## Erstellung eines neuen Builds, separate Ausführung der Tests und Start der Anwendung 

```powershell
mvn clean package
mvn test
mvn spring-boot:run
```

Die Anwendung ist nun unter http://localhost:8080 erreichbar.

## API-Testing

Anfragen können via [BimaruApi.http](./BimaruApi.http) abgesetzt werden.

## Docker

Docker-Image bauen und Container starten:

```powershell
docker build -t bimaru-api-js .
docker run -p 8080:8080 bimaru-api-js
```
