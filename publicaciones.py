#!/usr/bin/env python3
"""Actualiza data/publicaciones.json desde ORCID (qué DOI hay) y Crossref (datos de cada DOI).
Uso: python3 publicaciones.py && python3 build.py

Los ORCID se toman de DIRECTOR y MEMBERS en build.py (campo "orcid").
Si alguna consulta falla, no se toca el JSON anterior."""
import html, json, os, sys, urllib.parse, urllib.request

from build import DIRECTOR, MEMBERS

DESDE = 2025          # solo trabajos del semillero; los ORCID incluyen producción anterior
EXCLUIR = set()       # DOI que no deben aparecer, en minúsculas
EXTRA_DOIS = []       # DOI que no están en ningún ORCID

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(_HERE, "data", "publicaciones.json")
UA = "ChipLabUN-web (https://github.com/ChipLabUN/chiplabun-web)"


def get_json(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean(s):
    # Crossref a veces devuelve entidades escapadas dos veces ("&amp;amp;")
    prev = None
    while s != prev:
        prev, s = s, html.unescape(s)
    return " ".join(s.split())


def dois_orcid(orcid):
    data = get_json(f"https://pub.orcid.org/v3.0/{orcid}/works")
    out = []
    for g in data.get("group", []):
        for e in (g.get("external-ids") or {}).get("external-id", []):
            if e["external-id-type"] == "doi":
                out.append(e["external-id-value"].lower())
                break
    return out


def crossref(doi):
    m = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    fecha = (m.get("issued") or {}).get("date-parts", [[None]])[0] + [0, 0]
    return dict(
        doi=m["DOI"].lower(),
        titulo=clean(m["title"][0]),
        autores=[[clean(a.get("given", "")), clean(a.get("family", ""))] for a in m.get("author", [])],
        venue=clean((m.get("container-title") or [""])[0]),
        fecha=fecha[:3],
        url=(m.get("resource") or {}).get("primary", {}).get("URL") or "https://doi.org/" + m["DOI"],
    )


def main():
    gente = [p for p in [DIRECTOR] + MEMBERS if p.get("orcid")]
    try:
        dois = []
        for p in gente:
            print(f"ORCID {p['orcid']} ({p['name']})")
            dois += dois_orcid(p["orcid"])
        dois = list(dict.fromkeys(dois + [d.lower() for d in EXTRA_DOIS]))
        pubs = []
        for d in dois:
            if d in EXCLUIR:
                continue
            w = crossref(d)
            if (w["fecha"][0] or 0) >= DESDE:
                pubs.append(w)
                print(f"  + {w['fecha'][0]}  {w['titulo'][:70]}")
    except Exception as e:  # red caída, ORCID o Crossref sin responder
        sys.exit(f"Error consultando ORCID/Crossref: {e}\nNo se modificó {OUT}")
    pubs.sort(key=lambda w: w["fecha"], reverse=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(pubs, f, ensure_ascii=False, indent=1)
    print(f"{len(pubs)} publicaciones → {os.path.relpath(OUT, _HERE)}")


if __name__ == "__main__":
    main()
