#!/usr/bin/env python3
"""
Resume Generator Script
Creates a new folder and generates 100 random sample resumes in PDF format.
Uses random data generation and optionally Gemini API for enhanced content.
"""

import os
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import json
import time

# PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Optional: Gemini API for enhanced content generation
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Note: Gemini API not available. Install with: pip install google-generativeai")

class ResumeGenerator:
    def __init__(self, use_gemini=False, gemini_api_key=None):
        self.use_gemini = use_gemini and GEMINI_AVAILABLE
        if self.use_gemini and gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        
        # Sample data pools
        self.first_names = [
            "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn",
            "Blake", "Cameron", "Drew", "Emery", "Finley", "Hayden", "Jamie", "Kendall",
            "Logan", "Parker", "Reese", "Sage", "Skyler", "Tatum", "River", "Phoenix",
            "Sage", "Rowan", "Dakota", "Indigo", "Cedar", "Aspen", "Willow", "Juniper"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
            "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
        ]
        
        self.job_titles = [
            "Software Engineer", "Data Scientist", "Product Manager", "UX Designer",
            "DevOps Engineer", "Full Stack Developer", "Data Analyst", "Marketing Manager",
            "Sales Representative", "Project Manager", "Business Analyst", "System Administrator",
            "Frontend Developer", "Backend Developer", "Mobile Developer", "Cloud Architect",
            "Cybersecurity Specialist", "Machine Learning Engineer", "Database Administrator",
            "Quality Assurance Engineer", "Technical Writer", "Solutions Architect",
            "Scrum Master", "IT Consultant", "Network Engineer", "UI/UX Designer",
            "Digital Marketing Specialist", "Content Manager", "Operations Manager",
            "Financial Analyst", "HR Specialist", "Customer Success Manager"
        ]
        
        self.companies = [
            "TechCorp", "InnovateLabs", "DataFlow Systems", "CloudTech Solutions",
            "Digital Dynamics", "NextGen Technologies", "FutureSoft Inc", "SmartData Corp",
            "CyberGuard Systems", "Quantum Computing Ltd", "AI Innovations", "Blockchain Solutions",
            "WebCraft Studios", "MobileFirst Inc", "DevOps Pro", "SecurityFirst Corp",
            "Analytics Plus", "Machine Learning Co", "Database Masters", "Quality Assurance Ltd",
            "Project Management Pro", "Business Intelligence Inc", "Customer Experience Co",
            "Digital Transformation Ltd", "Agile Solutions", "Scalable Systems", "Performance Tech",
            "Reliability Corp", "Innovation Hub", "Technology Partners", "Digital Excellence"
        ]
        
        self.skills = [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin",
            "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
            "Spring Boot", "Laravel", "Ruby on Rails", "ASP.NET", "FastAPI", "Gin",
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra",
            "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
            "Jenkins", "GitLab CI", "GitHub Actions", "Ansible", "Puppet", "Chef",
            "Linux", "Windows Server", "macOS", "Ubuntu", "CentOS", "Red Hat",
            "Git", "SVN", "Mercurial", "Jira", "Confluence", "Slack", "Microsoft Teams",
            "Agile", "Scrum", "Kanban", "DevOps", "CI/CD", "Microservices", "REST API",
            "GraphQL", "gRPC", "WebSocket", "OAuth", "JWT", "SSL/TLS", "HTTPS",
            "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
            "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter", "Tableau", "Power BI"
        ]
        
        self.universities = [
            "Stanford University", "MIT", "Harvard University", "UC Berkeley", "Carnegie Mellon",
            "University of Washington", "Georgia Tech", "University of Illinois", "UT Austin",
            "University of Michigan", "Cornell University", "Princeton University", "Yale University",
            "Columbia University", "University of Pennsylvania", "Duke University", "Northwestern University",
            "University of Chicago", "Rice University", "Vanderbilt University", "Emory University",
            "University of Virginia", "University of North Carolina", "Wake Forest University",
            "Georgetown University", "Boston University", "Northeastern University", "Tufts University",
            "University of Southern California", "UCLA", "UC San Diego", "UC Irvine", "UC Davis",
            "Arizona State University", "University of Arizona", "University of Colorado",
            "University of Utah", "University of Oregon", "University of Washington", "Oregon State"
        ]
        
        self.majors = [
            "Computer Science", "Software Engineering", "Information Technology", "Data Science",
            "Computer Engineering", "Electrical Engineering", "Mathematics", "Statistics",
            "Physics", "Business Administration", "Marketing", "Finance", "Economics",
            "Psychology", "Communications", "Graphic Design", "Digital Media", "Cybersecurity",
            "Information Systems", "Management Information Systems", "Operations Research",
            "Industrial Engineering", "Mechanical Engineering", "Biomedical Engineering",
            "Chemical Engineering", "Civil Engineering", "Environmental Engineering"
        ]

    def generate_random_email(self, first_name, last_name):
        """Generate a random email address"""
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "company.com"]
        domain = random.choice(domains)
        return f"{first_name.lower()}.{last_name.lower()}@{domain}"

    def generate_random_phone(self):
        """Generate a random phone number"""
        return f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

    def generate_random_address(self):
        """Generate a random address"""
        street_numbers = [str(random.randint(100, 9999))]
        street_names = ["Main St", "Oak Ave", "Pine Rd", "Cedar Ln", "Maple Dr", "Elm St", "First Ave", "Second St"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
        states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
        zip_codes = [f"{random.randint(10000, 99999)}"]
        
        street = f"{random.choice(street_numbers)} {random.choice(street_names)}"
        city_idx = random.randint(0, len(cities) - 1)
        city = cities[city_idx]
        state = states[city_idx]
        zip_code = random.choice(zip_codes)
        
        return f"{street}, {city}, {state} {zip_code}"

    def generate_education(self):
        """Generate random education details"""
        degree_types = ["Bachelor's", "Master's", "PhD", "Associate's"]
        degree = random.choice(degree_types)
        major = random.choice(self.majors)
        university = random.choice(self.universities)
        gpa = round(random.uniform(2.5, 4.0), 2)
        graduation_year = random.randint(2015, 2024)
        
        return {
            "degree": degree,
            "major": major,
            "university": university,
            "gpa": gpa,
            "graduation_year": graduation_year
        }

    def generate_experience(self, num_jobs=None):
        """Generate random work experience"""
        if num_jobs is None:
            num_jobs = random.randint(1, 4)
        
        experiences = []
        current_year = datetime.now().year
        
        for i in range(num_jobs):
            job_title = random.choice(self.job_titles)
            company = random.choice(self.companies)
            
            # Calculate start and end dates
            if i == 0:  # Most recent job
                end_year = current_year
                start_year = end_year - random.randint(1, 5)
            else:
                end_year = experiences[i-1]["start_year"]
                start_year = end_year - random.randint(1, 3)
            
            # Generate job description using Gemini if available, otherwise use template
            if self.use_gemini:
                description = self.generate_job_description_with_gemini(job_title, company)
            else:
                description = self.generate_job_description_template(job_title, company)
            
            experiences.append({
                "job_title": job_title,
                "company": company,
                "start_year": start_year,
                "end_year": end_year,
                "description": description
            })
        
        return experiences

    def generate_job_description_template(self, job_title, company):
        """Generate a template-based job description"""
        templates = [
            f"Led development of scalable web applications using modern technologies, resulting in 30% performance improvement.",
            f"Collaborated with cross-functional teams to deliver high-quality software solutions on time and within budget.",
            f"Implemented automated testing and CI/CD pipelines, reducing deployment time by 50%.",
            f"Designed and maintained database schemas, optimizing query performance and ensuring data integrity.",
            f"Mentored junior developers and conducted code reviews to maintain high code quality standards.",
            f"Analyzed business requirements and translated them into technical specifications and implementation plans.",
            f"Participated in agile development processes including sprint planning, daily standups, and retrospectives.",
            f"Troubleshot and resolved complex technical issues, improving system reliability and user experience."
        ]
        
        # Select 3-4 random responsibilities
        selected_responsibilities = random.sample(templates, random.randint(3, 4))
        return "\n".join([f"• {resp}" for resp in selected_responsibilities])

    def generate_job_description_with_gemini(self, job_title, company):
        """Generate job description using Gemini API"""
        try:
            prompt = f"Generate 3-4 professional bullet points for a {job_title} position at {company}. Each bullet point should be 1-2 sentences and highlight key responsibilities and achievements. Format as bullet points starting with •"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating description with Gemini: {e}")
            return self.generate_job_description_template(job_title, company)

    def generate_skills(self):
        """Generate random skills"""
        num_skills = random.randint(8, 15)
        return random.sample(self.skills, num_skills)

    def generate_resume_data(self):
        """Generate complete resume data"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        
        return {
            "name": f"{first_name} {last_name}",
            "email": self.generate_random_email(first_name, last_name),
            "phone": self.generate_random_phone(),
            "address": self.generate_random_address(),
            "education": self.generate_education(),
            "experience": self.generate_experience(),
            "skills": self.generate_skills(),
            "summary": self.generate_summary()
        }

    def generate_summary(self):
        """Generate a professional summary"""
        summaries = [
            "Experienced software professional with a passion for creating innovative solutions and driving technical excellence.",
            "Results-driven developer with expertise in full-stack development and a track record of delivering high-quality software.",
            "Detail-oriented technical professional with strong problem-solving skills and experience in agile development methodologies.",
            "Creative and analytical professional with a proven ability to design and implement scalable software solutions.",
            "Collaborative team player with excellent communication skills and a commitment to continuous learning and improvement."
        ]
        return random.choice(summaries)

    def create_pdf_resume(self, resume_data, filename):
        """Create a PDF resume using reportlab"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.darkblue
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        
        # Header
        story.append(Paragraph(resume_data['name'], title_style))
        story.append(Paragraph(f"Email: {resume_data['email']} | Phone: {resume_data['phone']}", normal_style))
        story.append(Paragraph(resume_data['address'], normal_style))
        story.append(Spacer(1, 20))
        
        # Professional Summary
        story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        story.append(Paragraph(resume_data['summary'], normal_style))
        story.append(Spacer(1, 12))
        
        # Education
        story.append(Paragraph("EDUCATION", heading_style))
        edu = resume_data['education']
        edu_text = f"{edu['degree']} in {edu['major']}<br/>"
        edu_text += f"{edu['university']}<br/>"
        edu_text += f"GPA: {edu['gpa']} | Graduated: {edu['graduation_year']}"
        story.append(Paragraph(edu_text, normal_style))
        story.append(Spacer(1, 12))
        
        # Experience
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
        for exp in resume_data['experience']:
            exp_title = f"{exp['job_title']} at {exp['company']}"
            exp_dates = f"{exp['start_year']} - {exp['end_year']}"
            story.append(Paragraph(f"<b>{exp_title}</b>", normal_style))
            story.append(Paragraph(f"<i>{exp_dates}</i>", normal_style))
            story.append(Paragraph(exp['description'], normal_style))
            story.append(Spacer(1, 8))
        
        # Skills
        story.append(Paragraph("TECHNICAL SKILLS", heading_style))
        skills_text = " | ".join(resume_data['skills'])
        story.append(Paragraph(skills_text, normal_style))
        
        # Build PDF
        doc.build(story)

    def create_pdf_resume_memory(self, resume_data, output_buffer):
        """Create a PDF resume in memory using reportlab"""
        doc = SimpleDocTemplate(output_buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.darkblue
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        
        # Header
        story.append(Paragraph(resume_data['name'], title_style))
        story.append(Paragraph(f"Email: {resume_data['email']} | Phone: {resume_data['phone']}", normal_style))
        story.append(Paragraph(resume_data['address'], normal_style))
        story.append(Spacer(1, 20))
        
        # Professional Summary
        story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        story.append(Paragraph(resume_data['summary'], normal_style))
        story.append(Spacer(1, 12))
        
        # Education
        story.append(Paragraph("EDUCATION", heading_style))
        edu = resume_data['education']
        edu_text = f"{edu['degree']} in {edu['major']}<br/>"
        edu_text += f"{edu['university']}<br/>"
        edu_text += f"GPA: {edu['gpa']} | Graduated: {edu['graduation_year']}"
        story.append(Paragraph(edu_text, normal_style))
        story.append(Spacer(1, 12))
        
        # Experience
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
        for exp in resume_data['experience']:
            exp_title = f"{exp['job_title']} at {exp['company']}"
            exp_dates = f"{exp['start_year']} - {exp['end_year']}"
            story.append(Paragraph(f"<b>{exp_title}</b>", normal_style))
            story.append(Paragraph(f"<i>{exp_dates}</i>", normal_style))
            story.append(Paragraph(exp['description'], normal_style))
            story.append(Spacer(1, 8))
        
        # Skills
        story.append(Paragraph("TECHNICAL SKILLS", heading_style))
        skills_text = " | ".join(resume_data['skills'])
        story.append(Paragraph(skills_text, normal_style))
        
        # Build PDF
        doc.build(story)

def main():
    print("=" * 60)
    print("           RESUME GENERATOR")
    print("=" * 60)
    print()
    
    # Ask user for number of resumes to generate
    while True:
        try:
            num_resumes = input("How many resumes would you like to generate? (1-1000): ").strip()
            num_resumes = int(num_resumes)
            if 1 <= num_resumes <= 1000:
                break
            else:
                print("Please enter a number between 1 and 1000.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Ask user for preferences
    use_gemini = False
    gemini_api_key = None
    
    if GEMINI_AVAILABLE:
        use_gemini_input = input("Do you want to use Gemini API for enhanced content generation? (y/n): ").lower().strip()
        if use_gemini_input == 'y':
            use_gemini = True
            gemini_api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
            if not gemini_api_key:
                use_gemini = False
                print("Skipping Gemini API, using template-based generation.")
    
    # Create folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"generated_resumes_{timestamp}"
    
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Created folder: {folder_name}")
    except Exception as e:
        print(f"Error creating folder: {e}")
        return
    
    # Initialize generator
    generator = ResumeGenerator(use_gemini=use_gemini, gemini_api_key=gemini_api_key)
    
    print(f"Generating {num_resumes} resumes...")
    print("Progress: ", end="", flush=True)
    
    # Generate resumes
    for i in range(num_resumes):
        try:
            # Generate resume data
            resume_data = generator.generate_resume_data()
            
            # Create filename
            safe_name = "".join(c for c in resume_data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{folder_name}/resume_{i+1:03d}_{safe_name.replace(' ', '_')}.pdf"
            
            # Create PDF
            generator.create_pdf_resume(resume_data, filename)
            
            # Progress indicator
            if num_resumes <= 10:
                print(f"{i + 1}...", end="", flush=True)
            elif (i + 1) % max(1, num_resumes // 10) == 0:
                print(f"{i + 1}...", end="", flush=True)
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.1)
            
        except Exception as e:
            print(f"\nError generating resume {i+1}: {e}")
            continue
    
    print(f"\n\n✅ Successfully generated {num_resumes} resumes in folder: {folder_name}")
    print(f"📁 Location: {os.path.abspath(folder_name)}")
    print("\nResume generation complete!")

if __name__ == "__main__":
    main()
