from flask import Flask, render_template

def page_not_found(e):
    return render_template('404.html'), 404

def unauthorized(e):
    return render_template('401.html'), 401

