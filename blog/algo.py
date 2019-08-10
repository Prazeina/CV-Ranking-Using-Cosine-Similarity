import json
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import matplotlib.pyplot as plot
# from .views import upload_cv_list
# from .models import CV

keyword = ["technical skills", "top skills", "skills", "key skills", "special skills", "skills and abilities",
                   "professional skills", "special knowledge",
                   "knowledge and skills", "technical expertise", "technical qualification ", "education",
                   "academic qualification", "academic", "experience",
                   "professional work experience", "work experience","honors and awards","training","certifications","links","awards"]
keywordSkill = ["technical Skills", "key skills","top skills", "skills", "professional skills", "special knowledge",
                "knowledge and skills", "technical expertise",
                "technical qualification "]
keywordEducation = ["education", "academic qualification", "academic", "qualification"]
keywordExperience = ["experience", "work experience", "professional work experience"]
SkillWords = [
        'cobra', 'javascript', 'jscript', 'julia', 'matlab', 'numpy', 'r', 'sas', 'excel', 'outlook',
        'powerpoint',
        'excel', 'powerpoint', 'databases', 'sap', 'scipy', 'matplotlib', 'sckit-learn', 'graphlab',
        'image processing',
        'php', 'python', 'c', 'c++', 'c sharp', 'c#', 'java', 'mysql', 'sql', 'jquery', 'json', 'linux', 'verilog',
        'nosql', 'machine learning', 'apache', 'hadoop', 'cisa', 'mongodb', 'ruby', 'postgresql', 'big data', 'tableau',
        'architectural design', 'software engineering', 'matlab',
        'simulation', 'software as a service (ssas', 'perl', 'lampstack', 'debugging', 'mysql', 'embedded systems',
        'mobile application design', 'cryptography', 'ssl', 'html', 'html5', 'css',
        'system development life cycle(SDLC)', 'IT management', 'data architecture',
        'sturds', 'java message service', 'scrum', 'unix administration', 'database',
        'project manager',
        'unified modelling language', 'quality analyst', 'erwin', 'sybase', 'integrated development environment',
        'android', 'django', 'django rest framework', 'jQuery', 'js', 'asp.net', '.net', 'dot net', 'jsp',
        'servlet', 'web services', 'apache', 'sun', 'bootstrap', 'software engineering', 'anaconda',
        'conda', 'react js', 'react', 'node js', 'arduino', 'raspberry pi']
Education = {'master': ['master\'s', 'master', 'ms', 'm.s', 'me', 'm.e', 'm.e.', 'MBA', 'MSC', ],
             'bachelor': ['bachelor\'s', 'btech', 'bachelor', 'bachelors', 'diploma', 'computer', 'bim',
                          'b.e', 'b.e.', 'csit', 'bit', 'BSC']}
indexValue = []
topicName = []
lineList = list()


from collections import OrderedDict


def Rank(cv_list, post):  # Rank(qs,post)

    Rank = cosineFunc(cv_list, post)#cosine value return
    # x, y = zip(*Rank)  # unpack a list of pairs into two tuples
    # plt.plot(x, y)
    # plt.xlabel('Cosine Value Of Respective PDF')
    # plt.ylabel('PDF Name')
    # plt.title('Plot of cosine value and PDF')
    # # plt.legend(mode="expand")
    # plt.show()
    num = []
    pdf = []
    for k, v in Rank:
        if k >= 0.5:

            num.append(k) #cosine value
            pdf.append(v) #pdf
    print(num)
    print(pdf)

    # pdfName = json.dumps(pdf)
    return pdf


def cosineFunc(cv_list, post):
    cosine = []
    files = []
    text = []
    #mentor code from here
    # for cv in cv_list
    #     for pdf in os.listdir(pdfDir):  # iterate through pdfs in pdf directory

    for cv in cv_list:
        cvPath = str (cv.pdf)
        files.append(cvPath.split('/')[-1])#list of pdf
        print('file name: ',files)
        text.append(convert(cvPath))
        for line in text:
            lineList = line.lower().replace(',', '\n').rstrip('\n').split('\n')
        FilteredSkill, FilteredEducation = filtered_info(lineList)
        print('Skill:', FilteredSkill)
        print('Education:', FilteredEducation)

#List of skill and education from CV
        SkillEducationFromCV = FilteredSkill + FilteredEducation
        print('List of Skill and Education from CV', SkillEducationFromCV)

        job_description_SkillEducation=Info_from_job_desc(post)
        print(job_description_SkillEducation)

        #train the vectorizer
        vectoriser = CountVectorizer().fit(job_description_SkillEducation)
        vectoriser.vocabulary_  # show the word-matrix position pairs
        SkillEducation_vect, SkillEducation_cos = vect_cos(vect=vectoriser, test_list=[' '.join(SkillEducationFromCV)])#vect vector cos cosine value
        print('skill_vect',SkillEducation_vect)
        print('skill_cos',SkillEducation_cos)
        print('The cosine similarity for the first list is {}.'.format(SkillEducation_cos), '\n')
        cosine.append(SkillEducation_cos)
    print(cosine)
    combine = dict(zip(files, cosine))

    sorted_cv = sort(combine)

    print(sorted_cv)
    return sorted_cv


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open("media/"+fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


def filtered_info(lineList):
    print('linelist: ', lineList)
    for i in lineList:
        for m in keyword:
            if i == m:
                topicName.append(i)
                indexValue.append(lineList.index(i))

    merged = dict(zip(topicName, indexValue))  # merged topicName and its Index value zip ley merge garcha ani key ra value ho vanera dictionary le garcha
    print('merge: ', merged)

    # def extract(merged):
    skill = []
    for i in merged:
        try:
            second = next_value_of_Index(merged, i)#next index value read
        except IndexError:
            second = None
        read = lineList[merged[i] + 1:second] #read content of topic until next topic arrrives
        merged[i] = read

    # print(merged)
    skill = []
    education = []
    experience = []

    for i in merged.keys():
        for j in keywordSkill: #merged ma ako ra keyword skill hamile provide gareko mileyo vaney content skill[] ma halney
            if i == j:
                skill = (merged[i])#skill topicko content matra rakhne
                break
        for m in keywordEducation:
            if i == m:
                education = merged[i]
                break
        for n in keywordExperience:
            if i == n:
                experience = merged[i]
                # experienceName = i
                break

    ListSkill = []

    for i in skill:
        ListSkill += i.split()#split sentenct into each word
    print('Skill:', ListSkill)

    ListEducation = []
    for i in education:
        ListEducation += i.split()
    print('Education:', ListEducation)

    print('experience:', experience)

    FilteredSkill = []
    for i in SkillWords:
        if i in ListSkill:
            FilteredSkill.append(i) #skillWord ra listSkill ma matched vako jati filtered skillma append
    print("Filtered Skill:", FilteredSkill)

    FilteredEducation = []
    for i in Education.keys(): #masters, me j lekhey pani eutai ho vanera chalko loop
        for j in Education[i]:
            if j in ListEducation:
                FilteredEducation.append(i)
    print("Filtered Education:", FilteredEducation)
    return(FilteredSkill,FilteredEducation)


def next_value_of_Index(dictionary, current_key):

    # Get the list of keys from the OrderedDict
    keys = list(dictionary.keys())

    # Get an index of the current key and offset it by -1
    index = keys.index(current_key) + 1

    # return the previous key's value
    return dictionary[keys[index]]


def Info_from_job_desc(post):

    skillFromJob = [post.skill]#from database blog_post
    print(skillFromJob)
    job_description_skill=[]
    for tup in skillFromJob:
        joobskill=tup
        job_description_skill = (str(tup).lower().split(","))
    print(job_description_skill)

    educationFromJob = [post.education]
    for tup in educationFromJob:
        job_description_educationList = str(tup).lower().split(",")
    # print(educationFromJob)
    print(job_description_educationList)

    job_description_education = []
    for i in Education.keys():#me, m.e,mba j aayeni masters ho []
        for j in Education[i]: #''
            if j in job_description_educationList: #match garcha
                job_description_education.append(i)

    print('Skill from job description', job_description_skill)
    print('Education from job description', job_description_education)

    job_description_SkillEducation=job_description_skill +job_description_education
    print('List of Skill and education from Job description', job_description_SkillEducation)
    return job_description_SkillEducation


def sort(combine):
    combine_sorted = sorted({(v, k) for k, v in combine.items()}, reverse=True)
    return combine_sorted


def vect_cos(vect, test_list):
    """ Vectorise text and compute the cosine similarity """
    query_0 = vect.transform([' '.join(vect.get_feature_names())])
    print('query_0 : ', query_0)
    query_1 = vect.transform(test_list)
    print('query_1 : ', query_1)
    cos_sim = cosine_similarity(query_0.A, query_1.A)  # displays the resulting matrix #cosine_similarity use
    # plot(query_0.A, query_1.A)
    return query_1, np.round(cos_sim.squeeze(), 3)# upto 3 decimal places


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None















