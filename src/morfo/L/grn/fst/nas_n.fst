# Regla de nasalización para j/ñ (W) y d/nd (D) en prefijo. Puede ocurrir una vez nomas.

-> start

# Si no aparece W, no se aplica la regla; no hacer nada salvo eliminar %
start -> start       [.-W,D,%;:%]

# Solo ocurre al inicio?
start -> nasalize    [ñ:W;n:D]
start -> nonnas      [j:W;nd:D]

# Raíz sin nasal(es)
nonnas -> nonnas     [@x]
# Fin de la raíz
nonnas -> end        [:%]

# Raíz con nasal(es)
nasalize -> nasalize [@x]
# Segmento nasal
nasalize -> nas      [@m]
nas -> nas           [.-%]
# Fin de la raíz
nas -> end           [:%]

# Después de fin de raíz
end -> end           [.]

# nas ->
# nonnas ->
start ->
end ->
