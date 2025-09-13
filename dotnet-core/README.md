# .NET/C#-Version

## Voraussetzungen

Sicherstellen dass DotNet und Docker laufen.

```powershell
dotnet --version
docker -v
```

Depencendies laden.

```powershell
dotnet restore
```

## Erstellung eines neuen Builds, separate Ausführung der Tests und Start der Anwendung 

```powershell
dotnet clean
dotnet build
dotnet test
dotnet run --project BimaruApi/BimaruApi.csproj
```

Die Anwendung ist nun unter http://localhost:5033 erreichbar.

## API-Testing

Der Request-Body der `solve`-Operation kann via http://localhost:5033/swagger nicht gesetzt werden. Stattdessen können Anfragen via [BimaruApi.http](./BimaruApi/BimaruApi.http) abgesetzt werden.

## Docker

Docker-Image bauen und Container starten:

```powershell
docker build -t bimaru-api-dc .
docker run -p 8080:8080 bimaru-api-dc
```
