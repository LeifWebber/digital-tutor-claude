#!/usr/bin/env python3
"""Render the B-EN / B-ID test paragraphs with Anam's Avatar Videos API.

Usage (from the project root):
    export ANAM_API_KEY=...            # or put it in .env as ANAM_API_KEY=...
    python3 scripts/anam_video.py                 # both languages, stock Layla
    python3 scripts/anam_video.py --lang id       # only Indonesian
    python3 scripts/anam_video.py --avatar-id <your one-shot avatar id> --tag me
    python3 scripts/anam_video.py --lang id --voice-id <voice id> --tag layla-mia

Videos land in 测试结果/anam/. The script prints wall-clock render time and
the reported duration so you can fill 测试记录.csv.
"""
import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
import uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "测试结果" / "anam"
API = "https://api.anam.ai/v1/avatar-videos"

# Same ids the product uses (maic-avatar lib/avatar/personas.ts).
LAYLA = "ae2ea8c1-db28-47e3-b6ea-493e4ed3c554"
VOICES = {
    "en": "df2aec93-4b4e-41f2-8d02-b2d615ce184a",  # Mia, Cartesia sonic-3.6
    "id": "e7a81088-5558-4c7e-8c02-6dac0adf1053",  # Citra, ElevenLabs (imported)
}
SCRIPTS = {
    "en": (
        "Let's look at a classic example. Imagine a right triangle with sides of three and four "
        "centimeters. How long is the third side? First, we square both sides: three squared is "
        "nine, and four squared is sixteen. Then we add them together: nine plus sixteen equals "
        "twenty-five. Finally, we take the square root of twenty-five, which is five. So the "
        "longest side, the hypotenuse, is five centimeters. Now it's your turn: can you find "
        "another set of three whole numbers that works the same way?"
    ),
    "id": (
        "Mari kita lihat sebuah contoh klasik. Bayangkan sebuah segitiga siku-siku dengan sisi "
        "tiga dan empat sentimeter. Berapa panjang sisi ketiganya? Pertama, kita kuadratkan kedua "
        "sisi: tiga kuadrat adalah sembilan, dan empat kuadrat adalah enam belas. Lalu kita "
        "jumlahkan: sembilan ditambah enam belas sama dengan dua puluh lima. Terakhir, kita ambil "
        "akar kuadrat dari dua puluh lima, yaitu lima. Jadi sisi terpanjang, yaitu hipotenusa, "
        "panjangnya lima sentimeter. Sekarang giliran kalian: bisakah kalian menemukan tiga "
        "bilangan bulat lain yang juga berlaku seperti ini?"
    ),
}


def api_key() -> str:
    key = os.environ.get("ANAM_API_KEY")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("ANAM_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        sys.exit("ANAM_API_KEY not set (export it or add it to .env)")
    return key


def call(method: str, url: str, key: str, body=None, extra_headers=None):
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    headers.update(extra_headers or {})
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {url} -> HTTP {e.code}: {e.read().decode(errors='replace')}")


def render(lang: str, avatar_id: str, model: str, tag: str, key: str, voice_id=None) -> None:
    body = {
        "script": SCRIPTS[lang],
        "avatarId": avatar_id,
        "voiceId": voice_id or VOICES[lang],
        "avatarModel": model,
        "languageCode": lang,
        "videoWidth": 1152,
        "videoHeight": 768,
    }
    if model.startswith("cara-3"):
        body["videoWidth"], body["videoHeight"] = 720, 480
    start = time.time()
    job = call("POST", API, key, body, {"Idempotency-Key": f"b-{lang}-{tag}-{uuid.uuid4()}"})
    vid = job["id"]
    print(f"[{lang}] submitted {vid}")
    while True:
        time.sleep(5)
        job = call("GET", f"{API}/{vid}", key)
        status = job.get("status")
        print(f"[{lang}] {status} ({time.time() - start:.0f}s)")
        if status == "completed" and job.get("content", {}).get("available"):
            break
        if status in ("failed", "cancelled"):
            sys.exit(f"[{lang}] {status}: {json.dumps(job, ensure_ascii=False)}")
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"anam-{tag}-B-{lang.upper()}.mp4"
    urllib.request.urlretrieve(job["content"]["url"], dest)
    print(
        f"[{lang}] saved {dest.relative_to(ROOT)} | render {time.time() - start:.0f}s | "
        f"truncated={job.get('truncated')} | cap={job.get('effectiveMaxDurationSeconds')}s"
    )
    (OUT / f"anam-{tag}-B-{lang.upper()}.json").write_text(json.dumps(job, ensure_ascii=False, indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--lang", choices=["en", "id", "both"], default="both")
    p.add_argument("--avatar-id", default=LAYLA)
    p.add_argument("--model", default="cara-4-latest")
    p.add_argument("--tag", default="layla")
    p.add_argument("--voice-id", help="override the per-language voice id")
    a = p.parse_args()
    key = api_key()
    for lang in (["en", "id"] if a.lang == "both" else [a.lang]):
        render(lang, a.avatar_id, a.model, a.tag, key, a.voice_id)


if __name__ == "__main__":
    main()
