from fpdf import FPDF
from FSON import DICT
from FDate import DATE
import os
from harkDataProvider import Provider as pro
from Jarticle import jArticleProvider as jap
from FLog.LOGGER import Log
Log = Log("Utils.PDF")

height = 6
sentence_length = 90

CENTER = "C"
LEFT = "L"

EXPORTED_PDF_FILE = lambda file_name: os.path.join(os.path.dirname(__file__), file_name)

class PDF_ARTICLE(FPDF):
    file = ""
    name = ""
    articles = []
    firstPage: dict = None

    def __init__(self):
        super().__init__()

    @classmethod
    def RUN_CATEGORY(cls, category):
        arts = jap.get_category(category)
        _sorted = sort_articles_by_score(arts)
        newCls = cls()
        newCls.articles = _sorted
        newCls.name = f"{category}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.createPdf_with_body()
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
        newCls.createPdf_with_summary()
        newCls.outputPdf()

    @classmethod
    def RUN_DOUBLE_CATEGORY_SUMMARY(cls, category1, category2):
        arts1 = jap.get_category(category1)
        arts2 = jap.get_category(category2)
        all_arts = arts1 + arts2
        _sorted = sort_articles_by_score(all_arts)
        newCls = cls()
        newCls.articles = _sorted
        todays_date = DATE.mongo_date_today_str().replace(" ", "-")
        newCls.name = f"{category1}-{category2}-Summary-{todays_date}.pdf"
        newCls.file = EXPORTED_PDF_FILE(newCls.name)
        newCls.firstPage = {}
        newCls.createPdf_with_summary()
        newCls.outputPdf()

    def createFirstPage(self):
        self.add_page()
        self.safe_write("Overall Statistics", align=CENTER)
        self.set_font("Arial", size=12)
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

    # def createPdf_test(self):
    #     self.articles = pro.load_dict_from_file("test_hookups", "/Users/chazzromeo/chazzcoin/TiffanyBot/Data")
    #     self.createPdf()
    #     self.outputPdf()

    def upload_to_google_drive(self):
        from harkUploader import GoogleDriveUploader
        GoogleDriveUploader.upload_pdf(self.file)

    def createPdf_with_body(self):
        # -> Loop each hookup, add it to the pdf.
        count = 0
        for hookup_json in self.articles:
            source = DICT.get("source", hookup_json)
            score = DICT.get("score", hookup_json)
            if str(source).__contains__("investopedia"):
                continue
            elif int(score) < 500:
                continue
            count += 1
            self.add_page()
            self.set_font("Arial", size=12)
            # -> Loop Each Hookup Here ->
            title = DICT.get('title', hookup_json)
            body = DICT.get('body', hookup_json)
            category = DICT.get('category', hookup_json)
            score = DICT.get('score', hookup_json)
            sentiment = DICT.get('sentiment', hookup_json)
            author = str(DICT.get('author', hookup_json))
            tags = str(DICT.get('tags', hookup_json))
            source = DICT.get('source', hookup_json)
            source_rank = DICT.get('source_rank', hookup_json)
            url = DICT.get('url', hookup_json)
            published_date = DICT.get('published_date', hookup_json)
            categories = DICT.get("category_scores", hookup_json)
            # -> Header Work
            self.write_sentences(title, align=CENTER)
            self.safe_write(f"Date: {published_date}", align=CENTER)
            self.safe_write(f"Topic: {category}", align=CENTER)
            self.safe_write(f"#: {str(count)} | Score: {score}", align=CENTER)
            self.spacer()
            # -> Pre-Body
            self.write_sentences(f"Author: {author}")
            self.safe_write(f"Source: {source}", align=LEFT)
            self.safe_write(f"Source Rank: {source_rank}", align=LEFT)
            self.safe_write(f"Sentiment: {sentiment}", align=LEFT)
            self.safe_write(f"Tags: {tags}", align=LEFT)
            self.write_sentences(f"URL: {url}", align=LEFT, forceLimit=90)
            self.spacer()
            self.safe_write("--Topic Scores--", align=LEFT)
            for key in categories.keys():
                item = categories[key]
                score = item[0]
                self.safe_write(f"{key}: [ {score} ]", align=LEFT)
            self.spacer()
            # -> Body Work
            self.safe_write(f"Body:", align=LEFT)
            self.write_paragraphs(body)

    def createPdf_with_summary(self):
        # -> Loop each hookup, add it to the pdf.
        count = 0
        for hookup_json in self.articles:
            source = DICT.get("source", hookup_json)
            score = DICT.get("score", hookup_json)
            if str(source).__contains__("investopedia"):
                continue
            elif int(score) < 500:
                continue
            count += 1
            summary = DICT.get('summary', hookup_json, False)
            if not summary:
                continue
            self.add_page()
            self.set_font("Arial", size=12)
            # -> Loop Each Hookup Here ->
            title = DICT.get('title', hookup_json)
            category = DICT.get('category', hookup_json)
            score = DICT.get('score', hookup_json)
            sentiment = DICT.get('sentiment', hookup_json)
            author = str(DICT.get('author', hookup_json))
            keywords = str(DICT.get('keywords', hookup_json))
            source = DICT.get('source', hookup_json)
            source_rank = DICT.get('source_rank', hookup_json)
            url = DICT.get('url', hookup_json)
            published_date = DICT.get('published_date', hookup_json)
            categories = DICT.get("category_scores", hookup_json)
            # -> Header Work
            self.write_sentences(title, align=CENTER)
            self.safe_write(f"Date: {published_date}", align=CENTER)
            self.safe_write(f"Topic: {category}", align=CENTER)
            self.safe_write(f"#: {str(count)} | Score: {score}", align=CENTER)
            self.spacer()
            # -> Pre-Body
            self.write_sentences(f"Author: {author}")
            self.safe_write(f"Source: {source}", align=LEFT)
            self.safe_write(f"Source Rank: {source_rank}", align=LEFT)
            self.safe_write(f"Sentiment: {sentiment}", align=LEFT)
            self.safe_write(f"Tags: {keywords}", align=LEFT)
            self.write_sentences(f"URL: {url}", align=LEFT, forceLimit=90)
            self.spacer()
            self.safe_write("--Topic Scores--", align=LEFT)
            for key in categories.keys():
                item = categories[key]
                score = item[0]
                self.safe_write(f"{key}: [ {score} ]", align=LEFT)
            self.spacer()
            # -> Body Work
            self.safe_write(f"Summary:", align=LEFT)
            self.spacer()
            newSum = str(summary).replace("\n", "")
            self.write_sentences(newSum)

    def safe_write(self, text, align):
        cleaned_text = str(text).encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, height, txt=cleaned_text, ln=1, align=align)

    def spacer(self):
        self.cell(0, height, ln=1, align=CENTER)

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
        paragraphs = breakup_text(text)
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


def breakup_text(body: str) -> [str]:
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

# def export_categories(firstPage, dict_of_categories):
#     Log.i(f"Exporting Out Results to PDF")
#     for key in dict_of_categories:
#         hookups = dict_of_categories[key]
#         if len(hookups) > 50:
#             hookups = hookups[:50]
#         export_report(key, firstPage, hookups)

def sort_articles_by_score(articles, reversed=True):
    Log.v(f"sort_hookups_by_score: IN: {articles}")
    sorted_articles = sorted(articles, key=lambda k: k.get("score"), reverse=reversed)
    return sorted_articles

if __name__ == '__main__':
    PDF_ARTICLE.RUN_DOUBLE_CATEGORY_SUMMARY("metaverse", "crypto")