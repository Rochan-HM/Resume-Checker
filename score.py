import docx2txt
import os
import shutil
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pdfplumber


def parse_pdf(file):
    pdf = pdfplumber.open(file)
    content = ""
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = page.extract_text()
        content += text
    pdf.close()
    return content


def parse_word(file):
    return docx2txt.process(file)


def main(resume_file, job):
    main_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp/') + resume_file

    if main_file.endswith(".docx") or main_file.endswith(".doc"):
        resume = parse_word(main_file)
    elif main_file.endswith(".pdf"):
        resume = parse_pdf(main_file)
    elif main_file.endswith(".txt"):
        resume = main_file

    job_description = job

    text = [resume, job_description]

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)

    # Use cosine_similarity
    print("\nSimilarity Scores : ")
    print(cosine_similarity(count_matrix))

    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2)
    shutil.rmtree(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp/'))
    return "Your resume matches approximately " + str(matchPercentage) + "% of the job description."
