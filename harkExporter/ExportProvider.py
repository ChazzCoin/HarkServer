from FSON import DICT
from FArt import artSort
from Jarticle import jArticleProvider as jap
from PdfArticle import PDF_ARTICLE
from FDate import DATE
import uuid
TIMESTAMP = DATE.get_now_date_dt()
ID = str(uuid.uuid4())


def get_pdf(name, articles):
    pdf = PDF_ARTICLE()
    pdf.setup_name_and_file(name)
    pdf.add_articles(articles)
    return pdf

def create_export_pdf(pdf):
    pdf.create_pdf_of_articles()
    pdf.outputPdf()

def create_export_pdf_sorted_by_date(pdf):
    pdf.create_pdf_of_articles_sorted_by_date(summaryOnly=True)
    pdf.outputPdf()

def create_name(name, nameExtras):
    official = f"{TIMESTAMP}:{name}:{ nameExtras if nameExtras else '' }:{ID[-2:]}"
    return official

""" MASTER HELPER """
def main(name, articles, nameExtras=False):
    official_name = create_name(name, nameExtras)
    pdf_ready = get_pdf(official_name, articles)
    create_export_pdf(pdf_ready)

###################################################################################

def export_category_summary(*categories):
    _sorted = jap.get_categories(categories)
    main(name=categories, articles=_sorted, nameExtras="SUMMARY")


def RUN_REDDIT_POSTS():
    reddit_articles = jap.get_reddit_days_back(1)
    pdf_ready = get_pdf("New-Testing", reddit_articles)
    create_export_pdf(pdf_ready)

def run_tiffany_report():
    return run_meta_report(addCrypto=True)

def run_meta_report(addCrypto=False):
    if addCrypto:
        category_arts = jap.get_categories_last_5_days("metaverse", "crypto")
    else:
        category_arts = jap.get_categories_last_5_days("metaverse")
    by_date = artSort.sort_articles_into_lists_by_date(category_arts)
    pdf = PDF_ARTICLE().RUN_META_REPORT(by_date)
    return pdf

def run_crypto_report():
    category_arts = jap.get_categories_last_5_days("crypto")
    by_date = artSort.sort_articles_into_lists_by_date(category_arts)
    pdf = PDF_ARTICLE().RUN_META_REPORT(by_date)
    return pdf

if __name__ == '__main__':
    run_meta_report(addCrypto=True)
    # run_crypto_report()