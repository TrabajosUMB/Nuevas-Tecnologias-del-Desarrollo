"""Servidor web local del laboratorio (equivale a Live Server de VS Code): sirve una carpeta en http://localhost:PUERTO.

Envía «Cache-Control: no-store» para que la caché HTTP del navegador nunca oculte lo que hace (o no hace) el Service Worker.
Usa 127.0.0.1 y no lee nada fuera de la carpeta indicada. Uso: py servidor.py PUERTO CARPETA
"""
import functools
import http.server
import sys


class ManejadorSinCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, formato: str, *args) -> None:  # sin ruido en la consola
        pass


def main() -> None:
    puerto = int(sys.argv[1])
    carpeta = sys.argv[2]
    manejador = functools.partial(ManejadorSinCache, directory=carpeta)
    with http.server.ThreadingHTTPServer(("127.0.0.1", puerto), manejador) as servidor:
        servidor.serve_forever()


if __name__ == "__main__":
    main()
