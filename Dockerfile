# 1. Basis-Image mit .NET SDK für den Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# 2. Kopiere die Projektdateien aus dem Unterordner
COPY BimaruApi/*.csproj BimaruApi/
WORKDIR /app/BimaruApi
RUN dotnet restore

# 3. Kopiere den restlichen Code und baue das Projekt
COPY BimaruApi/. .
RUN dotnet publish -c Release -o /out

# 4. Erstelle ein schlankes Laufzeit-Image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /out .

# 5. Port für den Container freigeben
EXPOSE 8080

# 6. ASP.NET Core auf Port 8080 setzen
ENV ASPNETCORE_URLS=http://+:8080

# 7. Setze den Startbefehl
ENTRYPOINT ["dotnet", "BimaruApi.dll"]
