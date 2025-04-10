# app/routes/database.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from ..utils import login_required
from ..mongodb import mongo


database_bp = Blueprint("database", __name__, template_folder="../templates")


@database_bp.route("/database", methods=["GET"])
@login_required
def show_database():
    """
    Retrieve all documents from a specific collection.
    Adjust 'documents' below to match your collection name.
    """
    documents = list(mongo.db.complaints.find())
    return render_template("database.html", documents=documents)


"""@database_bp.route("/database/add", methods=["POST"])
def add_document():
    """
    #Get document text from the form and add it to the collection.
"""
    doc_text = request.form.get("doc_text")
    if not doc_text:
        flash("Document text is required.", "error")
    else:
        new_doc = {"text": doc_text}
        result = mongo.db.documents.insert_one(new_doc)
        flash("Document added successfully!")
    return redirect(url_for("database.show_database"))

    
@database_bp.route("/database/delete/<doc_id>", methods=["POST"])
def delete_document(doc_id):
    """
    #Delete a document based on its ObjectId.
"""
    mongo.db.documents.delete_one({"_id": ObjectId(doc_id)})
    flash("Document removed successfully!")
    return redirect(url_for("database.show_database"))
"""