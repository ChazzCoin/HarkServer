from fpdf import FPDF
from FSON import DICT
from FDate import DATE
import os

from fairNLP import Regex
from harkDataProvider import Provider as pro
from Jarticle import jArticleProvider as jap
from FLog.LOGGER import Log
Log = Log("Utils.PDF")

half_height = 3
height = 6
sentence_length = 110
force_length = 110

font_size = 10

CENTER = "C"
LEFT = "L"

EXPORTED_PDF_FILE = lambda file_name: os.path.join(os.path.dirname(__file__), file_name)

class PDF_ARTICLE(FPDF):
    file = ""
    name = ""
    articles = []
    total_count = 0
    firstPage: dict = None

    def __init__(self):
        super().__init__()

    @classmethod
    def RUN_SUMMARY(cls, articles, fileName):
        newCls = cls()
        _sorted = sort_articles_by_score(articles)
        newCls.articles = _sorted
        newCls.name = f"{fileName}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.create_pdf_of_articles()
        newCls.outputPdf()

    @classmethod
    def RUN_BODY(cls, articles, fileName):
        newCls = cls()
        _sorted = sort_articles_by_score(articles)
        newCls.articles = _sorted
        newCls.name = f"{fileName}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.create_pdf_of_articles()
        newCls.outputPdf()

    @classmethod
    def RUN_CATEGORY(cls, category):
        arts = jap.get_category(category)
        _sorted = sort_articles_by_score(arts)
        newCls = cls()
        newCls.articles = _sorted
        newCls.name = f"{category}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.create_pdf_of_articles()
        newCls.outputPdf()

    @classmethod
    def RUN_SEARCH_SUMMARY(cls, searchTerm):
        arts = jap.get_search(searchTerm)
        _sorted = sort_articles_by_score(arts)
        newCls = cls()
        newCls.articles = _sorted[:19]
        newCls.name = f"{searchTerm}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.create_pdf_of_articles()
        newCls.outputPdf()

    @classmethod
    def RUN_CATEGORY_SUMMARY(cls, category):
        arts = jap.get_category(category)
        _sorted = sort_articles_by_score(arts)
        newCls = cls()
        newCls.articles = _sorted
        newCls.name = f"{category}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.create_pdf_of_articles()
        newCls.outputPdf()

    @classmethod
    def RUN_DOUBLE_CATEGORY_SUMMARY(cls, category1, category2):
        _sorted = jap.get_categories(category1, category2)
        newCls = cls()
        newCls.articles = _sorted
        todays_date = DATE.mongo_date_today_str().replace(" ", "-")
        newCls.name = f"{category1}-{category2}-Summary-{todays_date}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.create_pdf_of_articles()
        newCls.outputPdf()

    @classmethod
    def RUN_TRIPLE_CATEGORY_SUMMARY(cls, category1, category2, category3):
        _sorted = jap.get_categories(category1, category2, category3)
        newCls = cls()
        newCls.articles = _sorted
        newCls.setup_name_and_file(f"{category1}-{category2}-{category3}-Summary")
        newCls.firstPage = {}
        newCls.create_pdf_of_articles()
        newCls.outputPdf()

    def setup_name_and_file(self, name):
        todays_date = DATE.mongo_date_today_str().replace(" ", "-")
        self.name = f"{name}-{todays_date}.pdf"
        self.file = EXPORTED_PDF_FILE(self.name)

    def add_articles(self, articles):
        for art in articles:
            self.articles.append(art)

    def create_pdf_of_articles(self, summaryOnly=True):
        for art in self.articles:
            self.total_count += 1
            source = DICT.get("source", art)
            if Regex.contains("reddit", source):
                # create reddit pdf
                self.write_reddit_post_to_page(art)
            else:
                # create article pdf
                self.write_article_to_page(art, summaryOnly=summaryOnly)

    def createFirstPage(self):
        self.add_page()
        self.safe_write("Overall Statistics", align=CENTER)
        self.set_font("Arial", size=font_size)
        for key in self.firstPage.keys():
            i = 1
            if key == "Titles":
                self.spacer()
                self.write_sentences(f"Article Titles:", align=LEFT)
                for title_item in self.firstPage[key]:
                    self.write_sentences(f"{i}: {title_item}", align=LEFT)
                    i += 1
            else:
                self.spacer()
                self.write_sentences(f"{key}: {self.firstPage[key]}", align=LEFT)

    def upload_to_google_drive(self):
        from harkUploader import GoogleDriveUploader
        GoogleDriveUploader.upload_pdf(self.file)

    def write_article_to_page(self, article, summaryOnly=True):
        # -> Loop each hookup, add it to the pdf.
        source = DICT.get("source", article)
        score = DICT.get("score", article)
        if str(source).__contains__("investopedia"):
            return
        elif int(score) < 500:
            return
        self.add_page()
        self.set_font("Arial", size=font_size)
        # -> Loop Each Hookup Here ->
        title = DICT.get('title', article)
        body = DICT.get('body', article)
        category = DICT.get('category', article)
        score = DICT.get('score', article)
        sentiment = DICT.get('sentiment', article)
        author = str(DICT.get('author', article))
        tags = str(DICT.get('tags', article))
        source = DICT.get('source', article)
        source_rank = DICT.get('source_rank', article)
        url = DICT.get('url', article)
        published_date = DICT.get('published_date', article)
        categories = DICT.get("category_scores", article)
        # -> Header Work
        self.write_sentences(title, align=CENTER)
        self.safe_write(f"Date: {published_date}", align=CENTER)
        self.safe_write(f"Topic: {category}", align=CENTER)
        self.safe_write(f"#: {str(self.total_count)} | Score: {score}", align=CENTER)
        self.spacer()
        # -> Pre-Body
        self.write_sentences(f"Author: {author}")
        self.safe_write(f"Source: {source}", align=LEFT)
        self.safe_write(f"Source Rank: {source_rank}", align=LEFT)
        self.safe_write(f"Sentiment: {sentiment}", align=LEFT)
        self.safe_write(f"Tags: {tags}", align=LEFT)
        self.write_sentences(f"URL: {url}", align=LEFT, forceLimit=force_length)
        self.spacer()
        self.safe_write("--Topic Scores--", align=LEFT)
        for key in categories.keys():
            item = categories[key]
            score = item[0]
            self.safe_write(f"{key}: [ {score} ]", align=LEFT)
        self.spacer()
        # -> Body Work
        summary = DICT.get('summary', article, False)
        if summaryOnly and summary:
            self.safe_write(f"Summary:", align=LEFT)
            self.spacer()
            newSum = str(summary).replace("\n", "")
            self.write_sentences(newSum)
        else:
            self.safe_write(f"Body:", align=LEFT)
            self.write_paragraphs(body)

    def write_reddit_post_to_page(self, reddit_post):
        # -> Loop each hookup, add it to the pdf.
        source = DICT.get("source", reddit_post)
        title = DICT.get('title', reddit_post)
        published_date = DICT.get('published_date', reddit_post)
        if Regex.contains("Daily Discussion", title):
            return
        self.add_page()
        self.set_font("Arial", size=font_size)
        # -> Loop Each Hookup Here ->
        title = DICT.get('title', reddit_post)
        body = DICT.get('body', reddit_post)
        subreddit = DICT.get('subreddit', reddit_post)
        comments = DICT.get('comments', reddit_post)
        author = str(DICT.get('author', reddit_post))
        url = DICT.get('url', reddit_post)
        # -> Header Work
        self.write_sentences(title, align=CENTER)
        self.safe_write(f"Date: {published_date}", align=CENTER)
        self.safe_write(f"Topic: {source}", align=CENTER)
        self.safe_write(f"{subreddit}", align=CENTER)
        self.write_sentences(f"Author: {author}")
        self.write_sentences(f"URL: {url}", align=LEFT, forceLimit=force_length)
        self.spacer()
        # -> Body Work
        self.safe_write(f"Post:", align=LEFT)
        self.spacer_half()
        self.write_sentences(body)
        self.spacer()
        self.safe_write("COMMENTS:", align=LEFT)
        comment_count = 0
        for comment in comments:
            authorComment = DICT.get("author", comment)
            bodyComment = DICT.get("body", comment)
            self.spacer_half()
            self.safe_write(f"-> #{comment_count} - {authorComment}", align=LEFT)
            self.write_sentences(bodyComment)
            comment_count += 1

    def safe_write(self, text, align):
        cleaned_text = str(text).encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, height, txt=cleaned_text, ln=1, align=align)

    def spacer(self):
        self.cell(0, height, ln=1, align=CENTER)

    def spacer_half(self):
        self.cell(0, half_height, ln=1, align=CENTER)

    def header(self):
        # Logo
        # self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'The Tiffany Report', 0, 0, CENTER)
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, CENTER)

    def outputPdf(self):
        # save the pdf with name .pdf
        self.output(self.name)

    def write_paragraphs(self, text, align=LEFT):
        paragraphs = extract_paragraphs(text)
        for paragraph in paragraphs:
            if paragraph == "" or paragraph == " ":
                self.cell(0, height, ln=1, align=align)
                continue
            self.write_sentences(paragraph)

    def write_sentences(self, text, align=LEFT, forceLimit=0):
        body_count = int(len(text) / sentence_length) + 10
        temp_body = text
        p = 0
        while p < body_count:
            results = build_single_line(temp_body, sentence_length, forceLimit=forceLimit)
            new_body = results[0]
            new_index = results[1]
            self.safe_write(new_body, align=align)
            if len(temp_body) <= new_index:
                break
            temp_body = temp_body[new_index:]
            p += 1


def build_single_line(body: str, i: int, forceLimit=0) -> (str, int):
    """ -> return string with space at the end of first 125 - 140 characters <- """
    count = len(body)
    if i > count:
        return body, i
    prep = body[:i]
    # if last character is empty
    if forceLimit > 0:
        if forceLimit <= i:
            return prep, i
    if prep[-1] == " " or prep[-1] == "." or prep[-1] == "," or prep[-1] == "\n":
        # write to cell
        return prep,  i
    # go forward one more.
    i += 1
    return build_single_line(body, i)


def extract_paragraphs(body: str) -> [str]:
    """ -> Separates text based on "\n" <- """
    paragraph_list = []
    i = 0
    temp_body = body
    for char in body:
        if char == "\n":
            new_body = temp_body[:i]
            paragraph_list.append(new_body)
            temp_body = temp_body[i+1:]
            i = 0
            continue
        i += 1
    return paragraph_list

def sort_articles_by_score(articles, reversed=True):
    Log.v(f"sort_hookups_by_score: IN: {articles}")
    sorted_articles = sorted(articles, key=lambda k: k.get("score"), reverse=reversed)
    return sorted_articles

if __name__ == '__main__':
    PDF_ARTICLE.RUN_SEARCH_SUMMARY("decentraland")
    # PDF_ARTICLE.RUN_TRIPLE_CATEGORY_SUMMARY("metaverse", "crypto", "programming")