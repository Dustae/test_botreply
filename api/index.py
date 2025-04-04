from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import json
import time
import re

app = FastAPI()

keywords = {
    "Developer":  [
        "developer", "software developer", "programmer", "engineer", "software engineer",
        "full stack", "full-stack", "fullstack", "frontend", "front-end", "backend", "back-end",
        "web development", "web app", "mobile development", "native app", "progressive web app",
        "api development", "rest api", "graphql", "microservices", "cloud computing",
        "devops", "agile development", "scrum", "continuous integration", "continuous deployment",
        "javascript", "typescript", "python", "java", "c#", "go", "php", "ruby", "swift", "kotlin",
        "node.js", "react", "vue.js", "angular", "django", "flask", "spring boot",
        "containerization", "docker", "kubernetes", "ci/cd", "github actions", "jenkins",
        "database", "sql", "nosql", "mongodb", "firebase", "postgresql", "mysql",
        "software architecture", "system design", "algorithm", "data structure",
        "นักพัฒนาซอฟต์แวร์", "โปรแกรมเมอร์", "นักพัฒนาเว็บ", "นักพัฒนาแอป", "วิศวกรซอฟต์แวร์"
    ],
    "Designer": [
        "design", "ui/ux", "ux design", "ui design", "user interface", "user experience",
        "web design", "graphic design", "motion design", "animation", "interaction design",
        "visual design", "brand identity", "typography", "color theory", "responsive design",
        "wireframing", "prototyping", "figma", "adobe xd", "sketch", "illustrator", "photoshop",
        "css animation", "front-end design", "css framework", "bootstrap", "tailwind css",
        "design system", "web accessibility", "product design", "design thinking",
        "นักออกแบบ", "นักออกแบบเว็บ", "นักออกแบบ ui/ux", "นักออกแบบกราฟิก", "ออกแบบแอนิเมชัน",
        "การออกแบบประสบการณ์ผู้ใช้", "การออกแบบส่วนติดต่อผู้ใช้", "ดีไซน์"
    ],
    "Data & AI": [
        "data science", "data engineer", "data analyst", "big data", "machine learning",
        "deep learning", "artificial intelligence", "ai", "ml", "computer vision",
        "natural language processing", "predictive modeling", "data mining",
        "business intelligence", "data pipeline", "data warehousing", "data visualization",
        "neural networks", "reinforcement learning", "feature engineering",
        "data preprocessing", "cloud data", "cloud analytics", "streaming data",
        "sql", "mysql", "postgresql", "mongodb", "nosql", "firebase", "hadoop", "spark",
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib",
        "การวิเคราะห์ข้อมูล", "การเรียนรู้ของเครื่อง", "ปัญญาประดิษฐ์", "การขุดข้อมูล", 
        "ระบบแนะนำอัจฉริยะ", "การวิเคราะห์เชิงพยากรณ์", "วิศวกรข้อมูล", "นักวิทยาศาสตร์ข้อมูล"
    ],
    "Security": [
        "cybersecurity", "hacking", "ethical hacking", "penetration testing",
        "security engineer", "malware analysis", "ransomware", "firewall",
        "network security", "application security", "web security", "api security",
        "cloud security", "identity and access management", "zero trust",
        "security compliance", "iso 27001", "gdpr", "pci dss", "data protection",
        "vulnerability assessment", "threat intelligence", "incident response",
        "cryptography", "encryption", "password management", "red team", "blue team",
        "penetration tester", "security operations center", "phishing attack",
        "multi-factor authentication", "api security", "การรักษาความปลอดภัยไซเบอร์",
        "การเข้ารหัสข้อมูล", "การทดสอบเจาะระบบ", "การป้องกันมัลแวร์", "ความปลอดภัยเครือข่าย"
    ],
    "QA & Tester":  [
        "quality assurance", "qa", "software testing", "test automation", "manual testing",
        "performance testing", "load testing", "unit testing", "integration testing",
        "regression testing", "functional testing", "security testing", "api testing",
        "test-driven development", "tdd", "bdd", "selenium", "junit", "cypress", "postman",
        "bug tracking", "test case", "continuous testing", "agile testing", "quality control",
        "การทดสอบซอฟต์แวร์", "การประกันคุณภาพ", "การตรวจสอบคุณภาพ", "การทดสอบประสิทธิภาพ",
        "การพัฒนาที่เน้นการทดสอบ", "การทดสอบโหลด", "การทดสอบความปลอดภัย"
    ],
    "Clound Management": [
    "cloud", "cloud computing", "cloud management", "cloud infrastructure",
    "cloud security", "cloud storage", "multi-cloud", "hybrid cloud",
    "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud platform",
    "kubernetes", "docker", "containerization", "orchestration",
    "serverless", "lambda", "api gateway", "devops", "site reliability engineering",
    "sre", "cloud automation", "terraform", "ansible", "cloudformation",
    "cloud monitoring", "observability", "prometheus", "grafana", "log analytics",
    "cost optimization", "autoscaling", "load balancing", "cdn",
    "elastic compute", "vm", "virtual machine", "cloud networking",
    "vpn", "vpc", "subnet", "firewall", "security group", "iam",
    "identity and access management", "cloud compliance", "iso 27001",
    "cloud-native", "cloud governance", "finops", "cloud billing",
    "backup and disaster recovery", "dr", "high availability", "fault tolerance",
    "kubernetes cluster", "helm", "openstack", "cloud sql", "cloud nosql",
    "serverless functions", "microservices architecture", "cloud architecture",
    "cloud engineer", "cloud administrator", "cloud consultant",
    "นักบริหารคลาวด์", "การจัดการคลาวด์", "คลาวด์คอมพิวติ้ง", "เครือข่ายคลาวด์",
    "ระบบจัดการทรัพยากรคลาวด์", "ระบบสำรองและกู้คืนข้อมูลคลาวด์", "การรักษาความปลอดภัยบนคลาวด์"
    ]
}

def search_keywords(desc_data):
    found_keywords = {}
    
    # Flatten the nested list and combine all the text into one list
    flattened_data = [text for sublist in desc_data for text in sublist]
    
    # Loop over the categories and their associated keywords
    for label, keyword_list in keywords.items():
        matching_keywords = {kw for kw in keyword_list if any(kw.lower() in text.lower() for text in flattened_data)}
        
        # If a match is found, label it accordingly
        if matching_keywords:
            found_keywords[label] = matching_keywords
            
    return found_keywords

def search_keywords_th(desc_data):
    found_keywords = {}

    # Flatten the nested list and combine all the text into one list
    flattened_data = [text for sublist in desc_data for text in sublist if isinstance(text, str)]  # Ensure text is a string

    # Loop over the categories and their associated keywords
    for label, keyword_list in keywords.items():
        matching_keywords = {
            kw for kw in keyword_list
            if any(
                (kw.lower() in text.lower() if re.search(r'[a-zA-Z]', kw) else kw in text)
                for text in flattened_data
            )
        }

        if matching_keywords:
            found_keywords[label] = matching_keywords

    return found_keywords

def contains_thai_and_alnum(text):
    has_thai = bool(re.search(r'[\u0E00-\u0E7F]', text))  # Check for Thai characters
    has_alnum = bool(re.search(r'[a-zA-Z0-9]', text))  # Check for English letters or numbers
    return has_thai and has_alnum  # True if both exist

@app.get("/")
def home():
    return {"message": "Welcome to the Books Scraper API"}

@app.get("/dekf")
def getdata_dekf():
    try:
        origin_url = "https://เด็กฝึกงาน.com"
        data_amount = 3 # defualt

        page = 1
        url = origin_url + "/ค้นหางาน?search%5Btypes%5D=3277&search%5Bpositions%5D%5B0%5D=2840&page=" + str(page)
        # Send an HTTP GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        print("get list success")
        
        list_data = soup.find_all("div", {"class": "job-post-box"})[:data_amount]
        job_posts = list_data[:data_amount]

        href_links = [job.find("a")["href"] for job in job_posts if job.find("a")]
        
        dekf_data = []
        for i in range(min(data_amount, len(href_links))):
            src = href_links[i]
            url2 = origin_url + src
            # Send an HTTP GET request
            response2 = requests.get(url2)

            # Check if the request was successful
            if response2.status_code != 200:
                print(f"Failed to retrieve content. Status code: {response2.status_code}")
                return []
            
            soup2 = BeautifulSoup(response2.text, "html.parser")

            title = (soup2.find("div", class_="job-post-show__header--body media-body")).find("h1", class_="h5").text.strip()
            company_name = (soup2.find("div", class_="job-post-show__header--body media-body")).find("h2", class_="h6").text.strip()
            company_info = " ".join((soup2.find("div", class_="col mb-2 mb-sm-0")).find("p").text.strip().split())
            position = (soup2.find("div", class_="col-md-4 col-sm-6")).text.strip().split("\n", 1)[1].strip()
            position_amount = (soup2.find("div", class_="col-md-3 col-sm-6")).text.strip().split("\n", 1)[1].strip()
            allowance = (soup2.find_all("div", class_="col-md-4")[1]).text.strip().split("\n", 1)[1].strip()
            working_time = (soup2.find_all("div", class_="col-md-5")[1]).text.strip().split("\n", 1)[1].strip()

            # - รายละเอียด
            desc_tags = (soup2.find_all("strong", class_="h6")[9]).find_parent("div").find_all("p") 
            desc_texts = [p.text.strip() for p in desc_tags] 
            desc_data = [line.strip() for p in desc_texts for line in p.split("\n") if line.strip()]
            # - คุณสมบัติ
            specification_tags = (soup2.find_all("strong", class_="h6")[10]).find_parent("div").find_all("p") 
            specification_texts = [p.text.strip() for p in specification_tags] 
            specification = [line.strip() for p in specification_texts for line in p.split("\n") if line.strip()]
            # - สวัสดิการ
            benefit_tags = (soup2.find_all("strong", class_="h6")[11]).find_parent("div").find_all("p") 
            benefit_texts = [p.text.strip() for p in benefit_tags] 
            benefit = [line.strip() for p in benefit_texts for line in p.split("\n") if line.strip()]
            # - สถานที่ปฏิบัติงาน
            working_place_tags = soup2.find_all("strong", class_="h6")[12].find_parent("div").text.strip().split("\n", 1)[1].strip().replace("\n", " ")
            working_place = " ".join(working_place_tags.split())

            banner_link = soup2.find("img", class_="job-post-show__header--logo d-flex mr-sm-3")['src']
            
            content = [
                        ["ข้อมูลบริษัท"] + [company_info],
                        ["ตำแหน่งที่เปิดรับ"] + [position],
                        ["จำนวนที่เปิดรับ"] + [position_amount],
                        ["เบี้ยเลี้ยง"] + [allowance],
                        ["เวลาทำงาน"] + [working_time],
                        ["รายละเอียดงาน"] + desc_data,
                        ["คุณสมบัติ"] + specification,
                        ["สวัสดิการ"] + benefit,
                        ["สถานที่ปฏิบัติงาน"] + [working_place]
                    ]
            label_tags = {}
            label_tags = search_keywords(content)
            if not label_tags or label_tags == {}:
                label_tags = {"NODATA": ""}


            blog_data = {
                            "author": "InternHufSystem",
                            "title": title,
                            "company_name": company_name,
                            "content": content,
                            "type": "auto_news",
                            "tags": label_tags,
                            "src_from": url2,
                            "banner_link": banner_link
                        }
            
            dekf_data.append(blog_data)
            print("data " + str(i) + " success")

            # Delay between requests
            print("waiting for cooldown")
            # time.sleep(5)
            print("cooldown success")
        return dekf_data
    except Exception as e:
        print(f"Error: {e}")  # Print the actual error
        return {"status": "error", "message": str(e)}

@app.get("/jobdb")
def getdata_jobdb():
    try:
        origin_url = "https://th.jobsdb.com"
        data_amount = 3 # defualt
        url = origin_url + "/th/intern-jobs-in-information-communication-technology"
        # Send an HTTP GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return []
        
            # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        print("get data list")

        list_data = soup.find_all("div", {"class": "gepq850 eihuid4z eihuid4x"})[:data_amount]
        job_posts = list_data[:data_amount]
        href_links = [job.find("a")["href"] for job in job_posts if job.find("a")]

        jobdb_data = []
        for i in range(min(data_amount, len(href_links))):
            src = href_links[i]
            url2 = origin_url + src
            # Send an HTTP GET request
            response2 = requests.get(url2)

            # Check if the request was successful
            if response2.status_code != 200:            
                print(f"Failed to retrieve content. Status code: {response2.status_code}")
                return []
            
            soup2 = BeautifulSoup(response2.text, "html.parser")
            
            # รายละเอียดที่ได้ 
            # - สถานที่ (จังหวัด)
            # - รายละเอียดทั้งหมดอยู๋ใน div ก้อนเดียว เรียงกันในแท็ก p 
            # - ถ้าอยาก label ต้องดึงคีย์เวิณืดเอาเอง
            title = soup2.find_all("div", class_="gepq850 eihuid5b eihuidhf eihuid6r")[1].find("h1").text.strip()
            company_name = soup2.find_all("div", class_="gepq850 eihuid5b eihuidhf eihuid6r")[1].find("span").text.strip()
            working_place = soup2.find_all("div", class_="gepq850 eihuid4z eihuidr eihuidp eihuidi3 eihuidb7")[1].text.strip()
            # รายละเอียดงาน
            desc_tags = soup2.find("div", class_="gepq850 _1iptfqa0").find_all(["p", "li"])
            desc_texts = [p.text.strip() for p in desc_tags] 
            desc_data = [line.strip() for p in desc_texts for line in p.split("\n") if line.strip()]

            content = [desc_data]
            label_tags = {}
            label_tags = search_keywords(content)
            if not label_tags or label_tags == {}:
                label_tags = {"NODATA": ""}
    
            blog_data = {
                            "author": "InternHufSystem",
                            "title": title,
                            "company_name": company_name,
                            "content": content,
                            "type": "auto_news",
                            "tags": label_tags ,
                            "src_from": url2,
                            "banner_link": None
                        }
            jobdb_data.append(blog_data)
            print("data " + str(i) + " success")

            # Delay between requests
            print("waiting for cooldown")
            # time.sleep(5)
            print("cooldown success")
        return jobdb_data
    except Exception as e:
        print(f"Error: {e}")  # Print the actual error
        return {"status": "error", "message": str(e)}

@app.get("/jbkk")
def getdata_jbkk():
    try:
        origin_url = "https://jobbkk.com/%E0%B8%AB%E0%B8%B2%E0%B8%87%E0%B8%B2%E0%B8%99/%E0%B9%84%E0%B8%AD%E0%B8%97%E0%B8%B5,%E0%B8%99%E0%B8%B1%E0%B8%81%E0%B8%A8%E0%B8%B6%E0%B8%81%E0%B8%A9%E0%B8%B2%E0%B8%9D%E0%B8%B6%E0%B8%81%E0%B8%87%E0%B8%B2%E0%B8%99"
        data_amount = 3  # Default
        url = origin_url
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        print("Get list success")

        # Perform URL data list
        job_posts = soup.find_all("div", {"class": "joblist-detail-device"})[:data_amount]
        href_links = [job.find("a")["href"] for job in job_posts if job.find("a")]

        jbkk_data = []  # Store all job data

        # Loop to extract data
        for i in range(min(data_amount, len(href_links))):

            url2 = href_links[i]
            response2 = requests.get(url2)

            if response2.status_code != 200:
                print(f"Failed to retrieve content. Status code: {response2.status_code}")
                continue  # Skip this entry and continue

            soup2 = BeautifulSoup(response2.text, "html.parser")

            # Extract job details
            title = soup2.find("p", class_="textRed font-text-20 font-DB-HeaventRounded-Bold")
            company_name = soup2.find("p", class_="textRed fontSubHead font-DB-HeaventRounded-Bold")

            title = title.text.strip() if title else "N/A"
            company_name = company_name.text.strip() if company_name else "N/A"

            # Extract job description
            desc_tags = soup2.find("p", class_="fontText mb-2")
            desc_data = []
            if desc_tags:
                desc_tags = desc_tags.find_parent("div").find_all("p") 
                desc_texts = [p.text.strip() for p in desc_tags] 
                desc_data = [line.strip() for p in desc_texts for line in p.split("\n") if line.strip()]

            # Extract qualifications
            keywords = ["คุณสมบัติด้านความรู้และความสามารถ", "คุณสมบัติเพิ่มเติม"]
            p_tags = soup2.find_all("p", class_="textRed mb-2")
            specification = []
            for keyword in keywords:
                for p in p_tags:
                    if p.text.strip() == keyword:
                        section = p.find_parent("section")
                        li_element = section.find("li") if section else None
                        if li_element:
                            specification.append(li_element.text.strip())
                        break  

            # Extract benefits
            benefit = []
            for p in p_tags:
                if p.text.strip() == "สวัสดิการ":
                    benf_section = p.find_parent("section")
                    if benf_section:
                        benefit = [li.text.strip() for li in benf_section.find_all("li")]
                    break  

            # Extract contact info
            contact_info = []
            for keyword in ["สนใจสมัครงานตำแหน่งงานนี้กรุณาติดต่อ", "ข้อมูลการติดต่อบริษัท"]:
                for p in p_tags:
                    if p.text.strip() == keyword:
                        parent_section = p.find_parent("section")  
                        if parent_section:
                            if keyword == "สนใจสมัครงานตำแหน่งงานนี้กรุณาติดต่อ":
                                spans = parent_section.find_all("span", class_="font-DB-HeaventRounded-Bold")
                                for span in spans:
                                    label = span.text.strip().replace(" :", "") 
                                    value = span.next_sibling.strip() if span.next_sibling else ""
                                    contact_info.append(f"{label}: {value}")
                            elif keyword == "ข้อมูลการติดต่อบริษัท":
                                div = p.find_next_sibling("div")
                                if div:
                                    contact_info.extend([p.text.strip() for p in div.find_all("p")])
                        break  

            # Extract banner image
            banner_tag = soup2.find("figure", class_="picCompany")
            banner_link = banner_tag.find("img")["src"] if banner_tag and banner_tag.find("img") else "N/A"

            # Structure content
            content = [
                ["รายละเอียดงาน"] + desc_data,
                ["คุณสมบัติ"] + specification,
                ["สวัสดิการ"] + benefit,
                ["ข้อมูลติดต่อ"] + contact_info
            ]

            # Get keyword labels
            label_tags = {}
            label_tags = search_keywords(content)
            if not label_tags or label_tags == {}:
                label_tags = {"NODATA": ""}


            # Create structured job data
            blog_data = {
                "author": "InternHufSystem",
                "title": title,
                "company_name": company_name,
                "content": content,
                "type": "auto_news",
                "tags": label_tags,
                "src_from": url2,
                "banner_link": banner_link
            }

            # Append to result list
            jbkk_data.append(blog_data)
            print("data " + str(i) + " success")

            # Delay between requests
            print("waiting for cooldown")
            # time.sleep(5)
            print("cooldown success")

        return jbkk_data
    except Exception as e:
        print(f"Error: {e}")  # Print the actual error
        return {"status": "error", "message": str(e)}

@app.get("/jobtk")
def getdata_toptk():
    try:
        origin_url = "https://www.jobtopgun.com"
        data_amount = 5 # defualt

        page = 1
        url = origin_url + "/th/jobs?keywords=%25E0%25B8%259D%25E0%25B8%25B6%25E0%25B8%2581%25E0%25B8%2587%25E0%25B8%25B2%25E0%25B8%2599&fields=6"
        # Send an HTTP GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        print("get list success")
        
        list_data = soup.find("div", {"id": "scrollable-job-cards-container"}).find_all("a")
        job_posts = list_data[:data_amount]

        href_links = [a.get("href") for a in job_posts ]
        
        jobtg_data = []
        for i in range(min(data_amount, len(href_links))):
            src = href_links[i]
            url2 =  origin_url + src
            # Send an HTTP GET request
            response2 = requests.get(url2)

            # Check if the request was successful
            if response2.status_code != 200:
                print(f"Failed to retrieve content. Status code: {response2.status_code}")
                return []
            soup2 = BeautifulSoup(response2.text, "html.parser")
            
            title = soup2.find("h1", {"class": "font-medium text-sub-primary text-lg"}).text.strip()
            company_name = soup2.find("span", {"class": "flex-1 font-medium text-lg"}).text.strip()
            working_place = soup2.find_all("div", {"class": "flex gap-2 text-sub-primary"})[2].find("span").text.strip()

            # - หน้าที่และความรับผิดชอบ
            desc_list = soup2.find("div", {"class": "text-foreground-700 [&_a]:text-primary [&_a]:underline [&_p]:pb-4 last:[&_p]:pb-0 [&_ul]:list-inside [&_ul]:list-disc"})
            desc_data = [child.get_text(strip=True) for child in desc_list.find_all(["p", "div"]) if child.get_text(strip=True)]

            # - คุณสมบัติ
            specification_list = soup2.find_all("div", {"class": "text-foreground-700 [&_a]:text-primary [&_a]:underline [&_p]:pb-4 last:[&_p]:pb-0 [&_ul]:list-inside [&_ul]:list-disc"})[1]
            specification = [text.strip() for text in specification_list.find_all(text=True, recursive=False) if text.strip()]
            specification.append([child.get_text(strip=True) for child in specification_list.find_all(["p", "div"]) if child.get_text(strip=True)])

            # - สวัสดิการ
            benf_list = soup2.find_all("div", {"class": "text-foreground-700 [&_a]:text-primary [&_a]:underline [&_p]:pb-4 last:[&_p]:pb-0 [&_ul]:list-inside [&_ul]:list-disc"})[2]
            benf = ([child.get_text(strip=True) for child in benf_list.find_all(["p", "div", "li"]) if child.get_text(strip=True)])

            banner_link = origin_url + soup2.find("img", {"class": "aspect-video h-16 w-auto shrink-0 object-contain sm:h-16 xl:h-20"})["src"]
            
            content = [
                        ["รายละเอียดงาน"] + desc_data,
                        ["คุณสมบัติ"] + specification,
                        ["สวัสดิการ"] + benf,
                        ["สถานที่ทำงาน"] + [working_place]
                    ]
            label_tags = {}
            label_tags = search_keywords_th(content)
            if not label_tags or label_tags == {}:
                label_tags = {"NODATA": ""}


            blog_data = {
                            "author": "InternHufSystem",
                            "title": title,
                            "company_name": company_name,
                            "content": content,
                            "type": "auto_news",
                            "tags": label_tags ,
                            "src_from": url2,
                            "banner_link": banner_link
                        }
            
            jobtg_data.append(blog_data)
            
            print("waiting for cooldown")
            # time.sleep(5)
            print("cooldown success")
        return jobtg_data
    except Exception as e:
        print(f"Error: {e}")  # Print the actual error
        return {"status": "error", "message": str(e)}

@app.get("/internth")
def getdata_internth():
    try:
        origin_url = "https://internth.com"
        data_amount = 1 # defualt
        page = 1
        url = origin_url + "/job?jobGroupId=11&jobTypeId=1"
        # Send an HTTP GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        print("get list success")
        
        list_data = soup.find_all("div", {"class": "details"})[:data_amount]
        job_posts = list_data[:data_amount]
        href_links = [job.find("a")["href"] for job in job_posts if job.find("a")]
        
        internth_data = []
        for i in range(min(data_amount, len(href_links))):
            src = href_links[i]
            # url2 =  origin_url + src
            url2 = "https://internth.com/job/5678"
            # Send an HTTP GET request
            response2 = requests.get(url2)

            # Check if the request was successful
            if response2.status_code != 200:
                print(f"Failed to retrieve content. Status code: {response2.status_code}")
                return []
            
            soup2 = BeautifulSoup(response2.text, "html.parser")
            
            title = soup2.find("div", {"class" : "job-details"}).find("h1").text.strip()
            company_name  = soup2.find("div", {"class" : "job-details"}).find("h2").text.strip()
            position_amount = soup2.find("h3", {"class" : "text-[1.1em] mt-6"}).text.strip()

            #รายละเอียดงาน
            desc_data  = soup2.find_all("p", {"class" : "whitespace-pre-wrap"})[0].text.strip().split("\n")

            #คุณสมบัติ 
            specification = soup2.find_all("p", {"class" : "whitespace-pre-wrap"})[1].text.strip().split("\n")

            #เบี้ยเลี้ยง
            for h3 in soup2.find_all("h3"):
                if h3.text.strip() == "เบี้ยงเลี้ยง":
                    next_p = h3.find_next_sibling("p")  # Get the next <p> element
                    if next_p:
                        allowance = next_p.text.strip()


            #สถานที่ทำงาน
            for h3 in soup2.find_all("h3"):
                if h3.text.strip() == "สถานที่ปฏิบัติงาน":
                    next_p = h3.find_next_sibling("p")  # Get the next <p> element
                    if next_p:
                        working_place = next_p.text.strip()

            #สวัสดิการ
            for h3 in soup2.find_all("h3"):
                if h3.text.strip() == "สวัสดิการ":
                    next_div = h3.find_next_sibling("div") 
                    if next_div:
                        li_texts = [li.text.strip() for li in next_div.find_all("li")]  
                        benf = li_texts

            #เวลาทำงาน
            working_time = soup2.find("p", {"class" : "flex flex-row gap-2 items-center whitespace-pre-line"}).text.strip()

            banner_link  = origin_url + soup2.find("div", {"class" : "flex flex-col gap-4 items-center"}).find("img")["src"]
            
            content = [
                        ["รายละเอียดงาน"] + desc_data,
                        ["คุณสมบัติ"] + specification,
                        ["เบี้ยเลี้ยง"] + [allowance],
                        ["สวัสดิการ"] + benf,
                        ["สถานที่ทำงาน"] + [working_place],
                        ["เวลาทำงาน"] + [working_time]
                    ]
            label_tags = {}
            label_tags = search_keywords_th(content)
            if not label_tags or label_tags == {}:
                label_tags = {"NODATA": ""}


            blog_data = {
                            "author": "InternHufSystem",
                            "title": title,
                            "company_name": company_name,
                            "content": content,
                            "type": "auto_news",
                            "tags": label_tags ,
                            "src_from": url2,
                            "banner_link": banner_link
                        }
            
            internth_data.append(blog_data)
            print("data " + str(i) + " success")
            print("waiting for cooldown")
            time.sleep(5)
            print("cooldown success")
        return internth_data
    except Exception as e:
        print(f"Error: {e}")  # Print the actual error
        return {"status": "error", "message": str(e)}