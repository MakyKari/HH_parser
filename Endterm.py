import requests
import csv
import pandas
from bs4 import BeautifulSoup

def parse_resumes(search_text):
    fields=[["name","salary","specialization","sex","age","experience","employment","citizenship"]]
    for i in range(1):
        if i == 0 : URL = "https://hh.kz/search/resume?text=" + search_text + "&area=40&currency_code=KZT&ored_clusters=true&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&items_on_page=20"
        else: URL = "https://hh.kz/search/resume?text=" + search_text + "&area=40&currency_code=KZT&ored_clusters=true&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&items_on_page=20 &page=" + str((i + 1))
        

        page = requests.get(URL, headers={'User-Agent': 'Custom'})
        soup = BeautifulSoup(page.content, "html.parser")

        job_elements = soup.find_all(class_ = "serp-item")

        for element in job_elements:
            Aelement = element.find(class_ = "serp-item__title")
            link = Aelement.get('href')

            newUrl = "https://hh.kz/" + link
            newPage = requests.get(newUrl, headers={'User-Agent': 'Custom'})
            newsoup = BeautifulSoup(newPage.content, "html.parser")
            
            title = element.find(class_ = "serp-item__title").get_text()
            Specialization = "Specialization not found :_("
            Salary = 0
            Age = "Age not found :_("
            EmpAndWork = []
            Exp = "Experince not found"
            Cs = "Citizenship not found"
            sex = "Sex not found"

            """ Finds specialization"""
            SpecializationElement = newsoup.find(class_ = "resume-block__specialization")
            if SpecializationElement is not None: Specialization = SpecializationElement.get_text() 

            """ Finds salary"""
            SalaryElement = newsoup.find(class_ = "resume-block__salary")
            if SalaryElement is not None:
                temp = ""
                for char in SalaryElement.get_text():
                    if '0' <= char <= '9':
                        temp += char
                Salary = int(temp)

            """ Finds Age"""
            AgeElement = element.find(class_ = "resume-search-item__fullname")
            if AgeElement is not None: Age = AgeElement.get_text()
            
            """ Finds employment and work schedule"""
            EmpElement = newsoup.find(class_ = "resume-block-container")
            
            if EmpElement is not None: Found = EmpElement.find_all("p")
            for EW in Found:
                if EW is not None:
                    EmpAndWork += EW.get_text()
                    EmpAndWork += "\n"
            EmpAndWork = ''.join(EmpAndWork)

            """ Finds years and month exp"""
            ExpElement = newsoup.find(class_ = "resume-block__title-text resume-block__title-text_sub")
            if ExpElement is not None: Exp = ExpElement.get_text()

            """ Finds citizenship"""
            CsElement = newsoup.find(lambda tag: tag.name == "p" and "Гражданство" in tag.text)
            if CsElement is None: CsElement = newsoup.find(lambda tag: tag.name == "p" and "Citizenship" in tag.text)
            if CsElement is not None: Cs = CsElement.get_text()

            """ Finds sex"""
            sexElement = newsoup.find(lambda tag: tag.name == "span" and (("Мужчина" in tag.text) or ("Женщина" in tag.text) or ("Male" in tag.text) or ("Female" in tag.text)))
            if sexElement is not None: sex = sexElement.get_text()

            field = [  title,
                        Salary,
                        Specialization,
                        sex,
                        Age,
                        Exp,
                        EmpAndWork,
                        Cs]

            fields.append(field)
    
    return fields
            
    
if __name__ == "__main__":
    search_text = input()

    with open("resumes.csv",'w', newline='', encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        writer.writerows(parse_resumes("java"))

pandas.read_csv('resumes.csv',delimiter=',')
reader = pandas.read_csv('resumes.csv',delimiter=',')
reader.sort_values(["salary","age","experience","name"])

reader.salary.min()
reader.salary.max()
reader.salary.mean()

info=[["Male",reader.loc[reader.sex==True].salary.min(),
       reader.loc[reader.sex==True].salary.max(),
       reader.loc[reader.sex==True].salary.mean()],
       ["Female",reader.loc[reader.sex==False].salary.min(),
        reader.loc[reader.sex==False].salary.max(),
        reader.loc[reader.sex==False].salary.mean()]]

daf = pandas.DataFrame(info, columns=['Sex','Min', 'Max','Average'])
daf