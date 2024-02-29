from litestar import Litestar, get


@get("/")
def index() -> str:
    return "Hello World!"


app: Litestar = Litestar([index])
