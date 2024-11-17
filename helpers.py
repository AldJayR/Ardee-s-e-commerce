from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_base_url():
    hostname = request.host.split(':')[0]
    port = request.host.split(':')[1]
    return f"http://{hostname}:{port}"

