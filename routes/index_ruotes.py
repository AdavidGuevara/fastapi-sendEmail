from fastapi import APIRouter, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import typing
import os

load_dotenv()


def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []


home = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@home.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@home.post("/submit")
def submit(
    request: Request,
    name: str = Form(),
    emailAddress: str = Form(),
    message: str = Form(),
):
    msg = EmailMessage()
    msg["Subject"] = "Email subject test"
    msg["From"] = os.environ["EMAIL"]
    msg["To"] = emailAddress
    msg.set_content(
        f"""\
    Name : {name}
    Email : {emailAddress}
    Message : {message}    
    """,
    )
    # send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.environ["EMAIL"], os.environ["PASSWORD"])
        smtp.send_message(msg)
        flash(request, "The email was sent successfully", "danger")
        
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
