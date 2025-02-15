# 1. Offizielles OpenJDK Image als Basis verwenden
FROM openjdk:23-jdk-slim

# 2. Arbeitsverzeichnis setzen
WORKDIR /app

# 3. Abhängigkeiten hinzufügen
COPY target/*.jar app.jar

# 4. Port freigeben (optional)
EXPOSE 8080

# 5. Startbefehl definieren
CMD ["java", "-jar", "app.jar"]
