from flask import Flask, render_template, session, redirect, url_for, flash,request, jsonify
import random
import os
import requests
from ast import literal_eval
import ast, json, urllib2

app = Flask(__name__)

@app.route('/')
def root_route():
    return "home.html"

if __name__ == "__main__":
    app.debug = True
    app.run()
