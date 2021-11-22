## Registry

- Autenticación 
- Auditoría

Cifrados reversibles e irreversibles
- Reversible -> simetrico/asimétrico


1 Cifrar

Guardar contraseña -> Cifrado **irreversible** (Hash)
Comparar cifrados -> Si son iguales entonces es la misma contraseña

La contraseña cifrada NO es un token

2 Proteger canal (https)

Usando sistema de clave asimetricas

## Visitante-Engine

Cifrar Kafka -> Cifrar con algo que no ofrezca Kafka -> Elegir un algoritmo

Simetrico emisor y receptor usan la misma clave -> Triple Des

Proteger la **clave** 

Guardar la clave en un certificado -> Somos pobres guardarlas en un archivo

## Logs

Logs estructurados en Engine (SIEM)

## Visitante 

Opción para conectarse mediante API / Empezar desde 0


