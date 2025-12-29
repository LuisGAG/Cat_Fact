import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

import requests


DEFAULT_BASE_URL = "https://cat-fact.herokuapp.com"  # conforme docs oficiais
DEFAULT_ENDPOINT = "/facts/random"


def _ensure_list(payload: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    return [payload]


def default_output_path() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return os.path.join("data", f"cat_facts_{ts}.csv")


def flatten_fact(f: Dict[str, Any], source_api: str) -> Dict[str, Any]:
    """
    Normaliza o JSON para uma linha "flat" no CSV.
    Mantém chaves comuns da API do Heroku quando existirem.
    """
    status = f.get("status") or {}
    user = f.get("user") or {}

    return {
        "id": f.get("_id") or f.get("id"),
        "text": f.get("text") or f.get("fact"),
        "type": f.get("type"),
        "created_at": f.get("createdAt"),
        "updated_at": f.get("updatedAt"),
        "deleted": f.get("deleted"),
        "status_verified": status.get("verified"),
        "status_sentCount": status.get("sentCount"),
        "user_id": user.get("_id"),
        "user_name": user.get("name"),
        "source": f.get("source"),
        "used": f.get("used"),
        "api_source": source_api,
        "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def write_csv(rows: List[Dict[str, Any]], out_path: str) -> None:
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    if not rows:
        raise ValueError("Nenhuma linha para escrever no CSV.")

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def request_with_retry(
    url: str,
    params: Dict[str, Any],
    timeout_s: int,
    max_retries: int,
    backoff_s: float,
) -> requests.Response:
    """
    Faz GET com retry/backoff.
    - Em 429/503/5xx: tenta novamente
    - Respeita Retry-After quando existir
    """
    last_exc: Optional[Exception] = None

    for attempt in range(0, max_retries + 1):
        try:
            resp = requests.get(url, params=params, timeout=timeout_s)

            # Sucesso
            if 200 <= resp.status_code < 300:
                return resp

            # Re-tentáveis
            if resp.status_code in (429, 503) or 500 <= resp.status_code <= 599:
                if attempt == max_retries:
                    resp.raise_for_status()

                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    try:
                        sleep_s = float(retry_after)
                    except ValueError:
                        sleep_s = backoff_s * (2 ** attempt)
                else:
                    sleep_s = backoff_s * (2 ** attempt)

                time.sleep(sleep_s)
                continue

            # Não re-tentável
            resp.raise_for_status()
            return resp

        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            last_exc = e
            if attempt == max_retries:
                raise
            time.sleep(backoff_s * (2 ** attempt))

    raise RuntimeError(f"Falha inesperada em request_with_retry. Último erro: {last_exc}")


def fetch_from_heroku(amount: int, animal_type: str, timeout_s: int, max_retries: int, backoff_s: float) -> List[Dict[str, Any]]:
    url = f"{DEFAULT_BASE_URL}{DEFAULT_ENDPOINT}"
    params = {"animal_type": animal_type, "amount": amount}

    resp = request_with_retry(url, params=params, timeout_s=timeout_s, max_retries=max_retries, backoff_s=backoff_s)
    return _ensure_list(resp.json())


def fetch_from_catfact_ninja(amount: int, timeout_s: int, max_retries: int, backoff_s: float) -> List[Dict[str, Any]]:
    """
    Fallback opcional quando a API do Heroku está fora.
    Retorna lista de dicts no formato padronizado (usando key 'fact').
    """
    facts: List[Dict[str, Any]] = []
    for _ in range(amount):
        url = "https://catfact.ninja/fact"
        resp = request_with_retry(url, params={}, timeout_s=timeout_s, max_retries=max_retries, backoff_s=backoff_s)
        payload = resp.json()
        facts.append(payload)
    return facts


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrai cat facts e salva em CSV local.")
    parser.add_argument("--amount", type=int, default=10, help="Quantidade de fatos")
    parser.add_argument("--animal-type", type=str, default="cat", help="animal_type (para API heroku)")
    parser.add_argument("--out", type=str, default=None, help="Caminho do CSV de saída (default: data/cat_facts_<ts>.csv)")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout (segundos)")
    parser.add_argument("--retries", type=int, default=5, help="Número de retries em erros temporários (503/5xx/429)")
    parser.add_argument("--backoff", type=float, default=1.0, help="Backoff base (segundos), exponencial por tentativa")
    parser.add_argument(
        "--fallback-ninja",
        action="store_true",
        help="Se a API do Heroku falhar, tenta catfact.ninja para conseguir gerar o CSV",
    )

    args = parser.parse_args()
    out_path = args.out or default_output_path()

    # 1) Tenta Heroku (API oficial do desafio)
    try:
        raw = fetch_from_heroku(args.amount, args.animal_type, args.timeout, args.retries, args.backoff)
        rows = [flatten_fact(f, source_api="cat-fact.herokuapp.com") for f in raw]
        write_csv(rows, out_path)
        print(f"OK: {len(rows)} fatos salvos em {out_path}")
        return
    except Exception as e:
        print(f"ATENÇÃO: falha ao consultar cat-fact.herokuapp.com (provável indisponibilidade 503). Erro: {e}", file=sys.stderr)

    # 2) Fallback opcional
    if args.fallback_ninja:
        raw = fetch_from_catfact_ninja(args.amount, args.timeout, args.retries, args.backoff)
        rows = [flatten_fact(f, source_api="catfact.ninja") for f in raw]
        write_csv(rows, out_path)
        print(f"OK (fallback): {len(rows)} fatos salvos em {out_path}")
        return

    # Sem fallback: falha controlada
    print("Falhou sem fallback. Rode novamente com --fallback-ninja ou tente mais tarde.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()