import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from flask import Flask, request, jsonify
import os


# Use a service account


def init_db():

    DIR = os.getcwd()
    cred = credentials.Certificate(DIR+'/admin-sdk.key.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db


def create(db, collection, data):
    try:
        doc_ref = db.collection(collection).document()
        doc_ref.set(data, merge=True)
        return jsonify({"success": True})
    except:
        return "an error occurred"
