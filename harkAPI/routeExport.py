from flask import Blueprint, request
import harkDB
from FusedDL import FusedDownloader
import json

from harkExporter import PDF_ARTICLE

routeExport_blueprint = Blueprint('routeExport', __name__)

@routeExport_blueprint.route('/export')
def index_exporter():
    return "/pdf"

@routeExport_blueprint.route('/export/pdf')
def export_pdf():
    PDF_ARTICLE.RUN_DOUBLE_CATEGORY_SUMMARY("stocks", "crypto")
    return "Exported PDF to Google Drive"