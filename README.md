# Web API rund um das Bimaru-Universum

Für verschiedene Bimaru-Aufgabenstellungen können hier die Lösungen generiert werden.

## Code

Es gibt zwei gleichwertige Implementationen in unterschiedlichen Technologien:

1. [Java/Spring-Version](./java-spring/README.md)
2. [.NET/C#-Version](./dotnet-core/README.md)

## API-Testing auf bestehendem Deployment

Die API steht via [bimaruapi.fly.dev](https://bimaruapi.fly.dev/api/home) zur Verfügung.

Anfragen können via [requests](./requests/) abgesetzt werden, z.B.

```sh
./solve_request_2.sh
```

Auch via Postman können Anfragen ans API geschickt werden:

- [home-returns-greeting-text](https://www.postman.com/martian-desert-485182/bimaru/request/j9z1868/home-returns-greeting-text)
- [solve-returns-single-solution](https://www.postman.com/martian-desert-485182/bimaru/request/u0mkfsc/solve-returns-single-solution)
- [solve-returns-many-solutions](https://www.postman.com/martian-desert-485182/bimaru/request/hu26azu/solve-returns-many-solutions)

**Achtung**: Zunächst von `No environment` auf `Fly` wechseln damit es funktioniert 😉👍

## Eigenes Deployment einrichten

Sicherstellen, dass das Fly CLI läuft:

```sh
fly version
```

Fly App erstellen (nur einmal erforderlich):

```sh
fly launch --name bimaruapi
```

Entscheiden, welche Version bereitgestellt werden soll:

```sh
cd java-spring && fly deploy && cd ..
cd dotnet-core && fly deploy && cd ..
```

Endpunkt bleibt immer gleich, unabhängig davon, ob die API gerade mit Java oder .NET läuft.
