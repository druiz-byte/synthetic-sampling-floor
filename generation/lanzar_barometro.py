# -*- coding: utf-8 -*-
"""Lanza el "Barómetro digital" completo (réplica del Deustobarómetro verano
2026, 141 preguntas en 6 bloques) a las 1.000 Personas del panel.

Ejecuta los 6 bloques en secuencia con Claude Haiku (necesita ANTHROPIC_API_KEY
en .env y GEMINI_API_KEY/GROQ_API_KEY comentadas). Cada bloque se guarda como
un archivo propio en resultados/, etiquetado con el nombre de la plantilla.

Uso:    python lanzar_barometro.py            → los 6 bloques, 1.000 Personas
        python lanzar_barometro.py 3          → solo el bloque 3
        python lanzar_barometro.py --muestra 50   → prueba con 50 Personas
Coste orientativo con Haiku: ~15-20 $ y ~30-45 min para la tanda completa.
"""
import json
import sys
import threading
import time
from pathlib import Path

import server  # carga .env, las Personas y el motor de encuesta

BASE = Path(__file__).parent
BLOQUES = sorted((BASE / 'encuestas').glob('barometro_digital_*.json'))


def lanzar_bloque(path, subset):
    doc = json.loads(path.read_text(encoding='utf-8'))
    preguntas = doc['preguntas']
    print(f"\n══ {doc['titulo']} — {len(preguntas)} preguntas, {len(subset)} Personas ══")

    with server._survey_lock:
        server._survey['definition'] = preguntas

    # monitor de progreso
    stop = threading.Event()
    def monitor():
        while not stop.wait(30):
            with server._survey_lock:
                done, total = server._survey['done'], server._survey['total']
                err = server._survey.get('last_error')
            print(f"   … {done}/{total}" + (f"  (último aviso: {err})" if err else ''))
    t = threading.Thread(target=monitor, daemon=True)
    t.start()

    t0 = time.time()
    server._survey_worker(preguntas, subset)   # bloqueante; guarda en resultados/
    stop.set()

    with server._survey_lock:
        fname = server._survey.get('saved_file')
        results = server._survey['results']
    vacias = sum(1 for r in results if not r.get('resps'))
    sin_parsear = sum(1 for r in results if r.get('raw_sin_parsear'))
    print(f"   ✔ {len(results)} Personas en {time.time()-t0:.0f}s · "
          f"vacías: {vacias} · sin parsear: {sin_parsear} · → resultados/{fname}")

    # etiquetar el archivo con la plantilla de origen
    if fname:
        fpath = BASE / 'resultados' / fname
        data = json.loads(fpath.read_text(encoding='utf-8'))
        data['plantilla'] = path.name
        data['titulo'] = doc['titulo']
        fpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    return fname


def main():
    args = [a for a in sys.argv[1:]]
    muestra = None
    if '--muestra' in args:
        i = args.index('--muestra')
        muestra = int(args[i + 1])
        del args[i:i + 2]
    solo = {int(a) for a in args} if args else None

    if not server.ANTHROPIC_API_KEY:
        sys.exit('✗ Falta ANTHROPIC_API_KEY en .env')
    if server.GEMINI_API_KEY or server.GROQ_API_KEY:
        sys.exit('✗ Comenta GEMINI_API_KEY/GROQ_API_KEY en .env para usar Claude Haiku')
    if not server.agents:
        sys.exit('✗ No se cargaron las Personas (pv_agentes.json)')

    subset = server.agents
    if muestra:
        import random
        subset = random.sample(server.agents, min(muestra, len(server.agents)))

    pendientes = [(i + 1, p) for i, p in enumerate(BLOQUES) if not solo or (i + 1) in solo]
    print(f"Barómetro digital: {len(pendientes)} bloque(s) × {len(subset)} Personas · modelo claude-haiku-4-5")
    guardados = []
    for n, path in pendientes:
        fname = lanzar_bloque(path, subset)
        guardados.append((n, fname))

    print('\n══ Resumen ══')
    for n, fname in guardados:
        print(f'  Bloque {n}: resultados/{fname}')
    print('\nContraste con los datos reales:')
    for n, fname in guardados:
        print(f'  python comparar_deustobarometro.py resultados/{fname} > resultados/contraste_bloque{n}.md')


if __name__ == '__main__':
    main()
