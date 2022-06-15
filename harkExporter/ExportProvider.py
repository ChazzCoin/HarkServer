from Jarticle import jArticleProvider as jap
from PdfArticle import PDF_ARTICLE

def get_pdf(name, articles):
    pdf = PDF_ARTICLE()
    pdf.setup_name_and_file(name)
    pdf.add_articles(articles)
    return pdf

def create_export_pdf(pdf):
    pdf.create_pdf_of_articles()
    pdf.outputPdf()


def RUN_REDDIT_POSTS():
    reddit_articles = jap.get_reddit_days_back(1)
    pdf_ready = get_pdf("New-Testing", reddit_articles)
    create_export_pdf(pdf_ready)


if __name__ == '__main__':
    RUN_REDDIT_POSTS()