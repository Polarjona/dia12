import asyncio
import aiohttp
import time
import psutil
import pandas as pd

MODEL = "gemma4:e4b"
URL = "http://localhost:11434/api/generate"

PROMPT = "Explica qué es Docker brevemente."

SCENARIOS = [1, 2, 3]


async def send_request(session):
    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False
    }

    start = time.time()

    try:
        async with session.post(URL, json=payload) as response:
            data = await response.json()

        latency = time.time() - start

        eval_count = data.get("eval_count", 0)
        eval_duration = data.get("eval_duration", 1)

        tokens_per_second = (
            eval_count / (eval_duration / 1_000_000_000)
            if eval_duration > 0
            else 0
        )

        return {
            "success": True,
            "latency": latency,
            "tokens_per_second": tokens_per_second
        }

    except Exception as e:
        print("\nERROR DETECTADO")
        print(type(e).__name__)
        print(e)

        return {
            "success": False,
            "latency": 0,
            "tokens_per_second": 0
        }


async def run_scenario(users):

    print(f"\nEjecutando escenario de {users} usuarios...")

    cpu_before = psutil.cpu_percent(interval=1)
    ram_before = psutil.virtual_memory().percent

    start_total = time.time()

    timeout = aiohttp.ClientTimeout(total=600)

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:

        tasks = [
            send_request(session)
            for _ in range(users)
        ]

        results = await asyncio.gather(*tasks)

    total_time = time.time() - start_total

    cpu_after = psutil.cpu_percent(interval=1)
    ram_after = psutil.virtual_memory().percent

    successes = sum(r["success"] for r in results)
    errors = users - successes

    avg_latency = sum(r["latency"] for r in results) / len(results)

    avg_tokens = (
        sum(r["tokens_per_second"] for r in results) /
        len(results)
    )

    return {
        "usuarios": users,
        "peticiones_ok": successes,
        "errores": errors,
        "latencia_media_s": round(avg_latency, 2),
        "tokens_s": round(avg_tokens, 2),
        "tiempo_total_s": round(total_time, 2),
        "cpu_inicio": cpu_before,
        "cpu_fin": cpu_after,
        "ram_inicio": ram_before,
        "ram_fin": ram_after
    }


async def main():

    resultados = []

    for users in SCENARIOS:
        resultado = await run_scenario(users)
        resultados.append(resultado)

    df = pd.DataFrame(resultados)

    print("\nRESULTADOS")
    print(df)

    df.to_csv("before.csv", index=False)

    print("\nResultados guardados en before.csv")


if __name__ == "__main__":
    asyncio.run(main())