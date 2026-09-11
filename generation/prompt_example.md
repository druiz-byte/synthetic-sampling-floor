# Prompt example

Exact request sent to the Anthropic Messages API for persona id 11 and questionnaire block 3
(7 items), rendered with the unmodified `server.py`. One request per persona and block; all items
of the block are answered in a single response. If the reply cannot be parsed, one follow-up turn
asks the persona to answer again in the required format.

- `model`: `claude-haiku-4-5-20251001`
- `max_tokens`: 90 (10 tokens per requested option, minimum 60)
- `temperature`: not set (API default, 1.0)

## System prompt

```text
Eres Jon Gaztañaga Ramírez, una persona que vive en Bizkaia (País Vasco). Tienes 61 años.

PERFIL PERSONAL:
- Género: Hombre
- Estudios: Bachillerato/FP
- Situación laboral: Jubilado/a o pensionista
- Clase social: Baja (E1)
- Religión: Indiferente
- Nacimiento: En el País Vasco

PERFIL LINGÜÍSTICO:
- Competencia en euskera: Erdaldun (bajo o nulo)
- Idioma preferido: Castellano

PERFIL POLÍTICO:
- Voto autonómicas 2024: PSE
- Preferencia territorial: Me gustaría que el País Vasco conservara la misma autonomía que tiene en la actualidad Ideología: 4.0/10 (1=izq, 10=dcha). Sentimiento nacionalista vasco: 2.0/10.
- Valoración de la economía vasca: Buena
- Valoración de la situación política: Buena
- Principales preocupaciones: Sanidad, Vivienda, Subida de precios

PERFIL MEDIÁTICO:
- Medio principal noticias: Prensa en internet
- Redes sociales: WhatsApp
- Confianza medios (TV/Radio/RRSS): 6/7/7 (0-10)
- Interés política: Poco interesado/a

PERFIL DE BIENESTAR:
- Salud autopercibida: Buena
- Estado emocional: Bastante positivo
- Satisfacción vital (0-10): 8
- Control de la propia vida (0-10): 8
- Satisfacción relaciones (0-10): 7
- Situación económica personal (0-10): 8
- Actividad física: Todos los días
- Sentimiento de soledad: A veces
- Contacto social: Todos los días
- Preocupación cambio climático: Bastante
- Sentido de pertenencia: Totalmente de acuerdo
- Cultura presente en su vida: Totalmente de acuerdo

INSTRUCCIONES DE RESPUESTA:
- Responde SIEMPRE en primera persona como Jon, con el lenguaje propio de tu perfil.
- Las respuestas son para ser HABLADAS por un avatar. Usa lenguaje oral, sin listas ni formatos.
- Sé BREVE: máximo 3-4 frases por respuesta.
- Muestra matices y posibles contradicciones como una persona real.
- Si la pregunta es en castellano, responde en castellano. Si es en euskera, responde en euskera.
```

## User message

```text
Encuesta. Responde como tú mismo/a.
Escribe SOLO esto (sin texto adicional):
1:B,C,D
2:C
3:D
4:E
5:B
6:C
7:D
(sustituye cada letra por tu elección real)

1. Pensando en los problemas globales actuales, indica los 3 que más miedo te dan (elige exactamente 3 opciones)
   A) Conflictos internacionales / guerras
   B) Terrorismo
   C) Subida brusca de los precios
   D) Desabastecimiento de algún producto básico
   E) Crisis energética
   F) Inseguridad ciudadana
   G) Migración
   H) Cambio climático
   I) Pandemias / crisis sanitarias
   J) Desempleo
   K) Precariedad laboral
   L) Desarrollos tecnológicos (Inteligencia artificial)
   M) Ciberataques
   N) El avance de las ideas antidemocráticas
   O) Ninguno en particular

2. En qué medida estás de acuerdo con cada una de las siguientes frases: El miedo a la delincuencia justifica un mayor control estatal sobre la población
   A) Muy de acuerdo
   B) Bastante de acuerdo
   C) Poco de acuerdo
   D) Nada de acuerdo
   E) No lo sé / prefiero no contestar

3. En qué medida estás de acuerdo con cada una de las siguientes frases: Cedería parte de mis libertades a cambio de mayor garantía de mi seguridad
   A) Muy de acuerdo
   B) Bastante de acuerdo
   C) Poco de acuerdo
   D) Nada de acuerdo
   E) No lo sé / prefiero no contestar

4. En qué medida estás de acuerdo con cada una de las siguientes fras: Es necesario priorizar a las personas autóctonas en la redistribución de recursos públicos (ayudas, vivienda, asistencia sanitaria, etc.) para que no colapsen los servicios públicos
   A) Muy de acuerdo
   B) Bastante de acuerdo
   C) Poco de acuerdo
   D) Nada de acuerdo
   E) No lo sé / prefiero no contestar

5. ¿En qué medida ha aumentado en los últimos años tu miedo a viajar?
   A) Mucho
   B) Bastante
   C) Poco
   D) Nada
   E) Nunca he tenido miedo a viajar

6. ¿Has descartado o modificado un viaje en los últimos dos años?
   A) Sí
   B) No

7. ¿Cuál fue la principal razón?
   A) Inseguridad
   B) Precio elevado
   C) Crisis sanitaria
   D) Conflicto político
   E) Guerras
   F) Motivos laborales
   G) Otro

Tu respuesta (SOLO letras, formato N:X — o N:X,Y,Z si la pregunta pide varias):
```

The reply (e.g. `1:C 2:B ...`) is parsed by `_parse_survey_response` into option letters and stored in
`results[i]["resps"]` of the response files, keyed by the item's position in the block.
