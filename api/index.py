from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import json
import time

app = FastAPI()

keywords = {
    "developer": [
        "software engineer", "backend developer", "frontend developer", "full stack developer", "mobile developer", "app developer",
        "javascript developer", "python developer", "java developer", "c# developer", "php developer", "go developer", "node.js developer",
        "api development", "microservices", "cloud computing", "devops", "agile development", "continuous integration", "software architecture",
        "วิศวกรซอฟต์แวร์", "นักพัฒนาซอฟต์แวร์", "นักพัฒนาเว็บ", "นักพัฒนาแอปพลิเคชัน", "นักพัฒนาแบ็กเอนด์", "นักพัฒนาฟรอนต์เอนด์", 
        "นักพัฒนาเต็มสแตก", "การพัฒนา api", "ระบบไมโครเซอร์วิส", "การประมวลผลบนคลาวด์"
    ],
    "web_designer": [
        "web design", "ui/ux designer", "graphic designer", "responsive design", "figma", "adobe xd", "wireframe", "prototyping", "user experience",
        "user interface", "css animation", "typography", "design thinking", "html/css", "bootstrap", "tailwind css", "web accessibility", 
        "color theory", "interaction design", "design system", "นักออกแบบเว็บ", "นักออกแบบ ui/ux", "กราฟิกดีไซน์", "การออกแบบโต้ตอบ", 
        "ระบบดีไซน์", "สีและฟอนต์", "การออกแบบเพื่อการเข้าถึง", "การออกแบบแอนิเมชัน", "เทรนด์การออกแบบ", "เครื่องมือออกแบบ"
    ],
    "data_ai": [
        "data engineer", "data scientist", "data analyst", "ai engineer", "machine learning", "deep learning", "natural language processing", 
        "computer vision", "big data", "sql", "nosql", "data warehousing", "data mining", "data pipeline", "business intelligence", 
        "data visualization", "neural networks", "reinforcement learning", "feature engineering", "predictive analytics", "วิศวกรข้อมูล", 
        "นักวิทยาศาสตร์ข้อมูล", "นักวิเคราะห์ข้อมูล", "ปัญญาประดิษฐ์", "การเรียนรู้ของเครื่อง", "การวิเคราะห์ข้อมูลขนาดใหญ่", 
        "ระบบฐานข้อมูล", "การขุดข้อมูล", "การวิเคราะห์เชิงพยากรณ์", "ระบบแนะนำอัจฉริยะ"
    ],
    "security": [
        "security", "cybersecurity", "penetration testing", "ethical hacking", "malware analysis", "threat intelligence", "vulnerability assessment", 
        "security engineer", "cryptography", "network security", "identity & access management", "security policy", "web security", 
        "zero trust", "red team", "blue team", "cloud security", "endpoint protection", "security awareness", "firewall", "security compliance", 
        "ความปลอดภัยทางไซเบอร์", "การทดสอบเจาะระบบ", "การป้องกันมัลแวร์", "การรักษาความปลอดภัยเครือข่าย", "การเข้ารหัสข้อมูล", 
        "ระบบยืนยันตัวตน", "การจัดการสิทธิ์การเข้าถึง", "ระบบความปลอดภัยบนคลาวด์", "ทีมแดง ทีมฟ้า (red team/blue team)", 
        "การปฏิบัติตามมาตรฐานความปลอดภัย"
    ],
    "qa_tester": [
        "quality assurance", "software testing", "test automation", "manual testing", "performance testing", "load testing", "security testing", 
        "unit testing", "integration testing", "regression testing", "test case", "bug tracking", "selenium", "junit", "cypress", "postman", 
        "api testing", "agile testing", "test-driven development", "quality control", "การทดสอบซอฟต์แวร์", "การตรวจสอบคุณภาพ", 
        "การทดสอบอัตโนมัติ", "การทดสอบประสิทธิภาพ", "การทดสอบโหลด", "ระบบติดตามข้อผิดพลาด", "การพัฒนาที่เน้นการทดสอบ (tdd)", 
        "การทดสอบการทำงานร่วมกัน", "การทดสอบ api", "การประกันคุณภาพ"
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

@app.get("/")
def home():
    return {"message": "Welcome to the Books Scraper API"}

@app.get("/scrape")
def getdata_jbkk():
    try:
        origin_url = "https://jobbkk.com/%E0%B8%AB%E0%B8%B2%E0%B8%87%E0%B8%B2%E0%B8%99/%E0%B9%84%E0%B8%AD%E0%B8%97%E0%B8%B5,%E0%B8%99%E0%B8%B1%E0%B8%81%E0%B8%A8%E0%B8%B6%E0%B8%81%E0%B8%A9%E0%B8%B2%E0%B8%9D%E0%B8%B6%E0%B8%81%E0%B8%87%E0%B8%B2%E0%B8%99"
        data_amount = 5  # Default
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
            label_tags = search_keywords(content)

            # Create structured job data
            blog_data = {
                "author": "InternHufSystem",
                "title": title,
                "company_name": company_name,
                "content": content,
                "type": "auto_news",
                "tag": label_tags,
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


   