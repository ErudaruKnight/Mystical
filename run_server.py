импорт http.сервера
импорт сокетсервера
импорт веб-браузера
импортировать pathlib
импортировать систему

ПОРТ = 8000
если len (sys.argv) > 1 :
 
    пытаться :
        ПОРТ = int (sys.argv[ 1 ])
    за исключением ValueError:
        проходить

DIR = pathlib.Path(__file__).resolve().parent / "rune_circle"

Обработчик класса (http.server.SimpleHTTPRequestHandler):
 
    def __init__ ( self, *args, **kwargs ):
 
        super ().__init__(*args, directory= str (DIR), **kwargs)


def main () -> Нет :
 
    url = f"http://localhost: {PORT} /index.html"
    пытаться :
        с socketserver.TCPServer(( "" , PORT), Handler) в качестве httpd:
            print ( f"Обслуживание {DIR} по адресу {url} " )
            пытаться :
                веб-браузер. открыть (url)
            за исключением Исключение:
                проходить
            httpd.serve_forever()
    за исключением OSError , как exc:
        print ( f"Не удалось запустить сервер на порту {PORT} : {exc} " )
        sys.выход( 1 )


если __name__ == "__main__" :
    основной()