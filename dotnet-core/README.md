# Web API rund um das Bimaru-Universum

Hier sollen die Lösungen für verschiedene Bimaru-Aufgabenstellungen gefunden und retour geliefert werden.

## Voraussetzungen

Sicherstellen dass DotNet und Docker laufen.

```ps
dotnet --version
docker -v
```

Depencendies laden.

```ps
dotnet restore
```

## Erstellung eines neuen Builds, separate Ausführung der Tests und Start der Anwendung 

```ps
dotnet clean
dotnet build
dotnet test
dotnet run --project BimaruApi/BimaruApi.csproj
```

Die Anwendung ist nun unter http://localhost:5033 erreichbar.

## Docker

Docker-Image bauen und Container starten:

```ps
docker build -t bimaru-api .
docker run -p 8080:8080 bimaru-api
```
