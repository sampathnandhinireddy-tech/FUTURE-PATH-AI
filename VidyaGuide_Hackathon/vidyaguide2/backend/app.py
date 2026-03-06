"""
VidyaGuide AI Backend — Flask
Career Planning & Resume Mentor API
Run: python app.py
"""

import os, json, re
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── Init ──────────────────────────────────────────────────
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# ── Static Serving ────────────────────────────────────────
@app.route('/')
def root():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:p>')
def static_files(p):
    fp = os.path.join('../frontend', p)
    if os.path.isfile(fp):
        return send_from_directory('../frontend', p)
    return send_from_directory('../frontend', 'index.html')

# ── Health ────────────────────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'VidyaGuide AI Backend',
        'version': '2.0.0',
        'ai_enabled': bool(API_KEY),
        'timestamp': datetime.now().isoformat()
    })

# ── Resume Analysis ───────────────────────────────────────
@app.route('/api/resume/analyse', methods=['POST'])
def analyse_resume():
    body = request.json or {}
    text    = body.get('resume_text', '')
    role    = body.get('target_role', 'Software Engineer')
    jd      = body.get('job_desc', '')
    profile = body.get('profile', {})

    result = _claude_resume(text, role, jd, profile) if API_KEY else None
    if not result:
        result = _mock_resume(text, role)
    return jsonify(result)


def _claude_resume(text, role, jd, profile):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=API_KEY)
        prompt = f"""You are an expert resume coach and ATS specialist. Analyse the resume below for the role of "{role}".
{f'Job Description: {jd[:800]}' if jd else ''}
{f'Student Profile: {json.dumps(profile)}' if profile else ''}

Resume Text:
---
{text[:3500]}
---

Return ONLY valid JSON (no markdown, no explanation) with this exact structure:
{{
  "ats": <integer 0-100>,
  "cnt": <integer 0-100>,
  "fmt": <integer 0-100>,
  "grade": "<Excellent|Good|Needs Work>",
  "summary": "<2 concise sentences>",
  "strengths": ["<s1>","<s2>","<s3>","<s4>"],
  "gaps": ["<g1>","<g2>","<g3>","<g4>"],
  "found": ["<keyword>"],
  "miss": ["<missing keyword>"],
  "improvements": [
    {{"pri":"High|Medium|Low","title":"<title>","desc":"<description>"}}
  ],
  "rewrites": [
    {{"before":"<weak bullet>","after":"<strong bullet>"}}
  ]
}}"""
        msg = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=1800,
            messages=[{'role':'user','content':prompt}]
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r'^```json\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)
        return json.loads(raw)
    except Exception as e:
        print(f'[Claude resume] {e}')
        return None


def _mock_resume(text, role):
    wc   = len(text.split()) if text else 0
    nums = bool(re.search(r'\d+%|\d+x|\b\d+ (users|requests|people|teams|days)\b', text, re.I))
    verbs= bool(re.search(r'\b(built|led|designed|developed|implemented|achieved|reduced|improved|launched|optimised)\b', text, re.I))
    cont = bool(re.search(r'@|github|linkedin|portfolio', text, re.I))

    ats = min(94, 46 + min(22, wc//20) + (13 if nums else 0) + (8 if verbs else 0) + (6 if cont else 0))
    cnt = min(90, ats - 4 + (5 if nums else 0))
    fmt = min(93, ats + 3)

    KW = {
        'Software Engineer':    (['Python','JavaScript','REST API','Git','OOP','Problem Solving'],  ['Docker','Kubernetes','CI/CD','AWS','TypeScript','Microservices','Redis']),
        'Data Scientist':       (['Python','SQL','Pandas','ML','Statistics','Data Analysis'],       ['TensorFlow','PyTorch','Spark','MLflow','A/B Testing','Feature Engineering']),
        'Data Analyst':         (['SQL','Excel','Python','Tableau','Reporting'],                    ['Power BI','dbt','Airflow','Statistical Modelling','A/B Testing']),
        'Product Manager':      (['Agile','Scrum','Roadmap','User Stories','Stakeholder Mgmt'],     ['SQL','A/B Testing','OKRs','Figma','Go-to-market','Analytics']),
        'DevOps Engineer':      (['Linux','Git','CI/CD','Docker','Scripting'],                      ['Kubernetes','Terraform','Ansible','Prometheus','Grafana','AWS EKS']),
        'Full-Stack Developer': (['HTML','CSS','JavaScript','React','Node.js','Git'],               ['TypeScript','GraphQL','Redis','Docker','PostgreSQL','Testing']),
    }
    rk = next((k for k in KW if k.lower() in role.lower()), 'Software Engineer')
    found, miss = KW[rk]

    return {
        'ats': ats, 'cnt': cnt, 'fmt': fmt,
        'grade': 'Excellent' if ats>=82 else 'Good' if ats>=68 else 'Needs Work',
        'summary': f'Your resume scores {ats}/100 for ATS compatibility for a {role} role. {"Strong foundation — targeted improvements will make it exceptional." if ats>=70 else "Several improvements can significantly boost your shortlisting rate."}',
        'strengths': [
            'Contact information and professional structure are clearly organised',
            f'{"Good use of action verbs strengthens impact of experience bullets" if verbs else "Technical skills section lists relevant keywords for the role"}',
            'Education section is complete and easy to scan',
            'Overall document length is appropriate for your experience level'
        ],
        'gaps': [
            'Missing quantifiable achievements — every bullet needs a number, percentage, or measurable outcome',
            f'Critical ATS keywords missing: {", ".join(miss[:3])}',
            'Professional summary is weak or absent — must clearly target the specific role',
            'GitHub or portfolio link missing — 73% of recruiters check before interviewing'
        ],
        'found': found,
        'miss': miss,
        'improvements': [
            {'pri':'High',   'title':'Quantify Every Bullet Point',        'desc':f'Replace "worked on X" with "Built X serving 2,000+ daily users, reducing load time by 38%". Numbers make you memorable.'},
            {'pri':'High',   'title':'Add a Targeted Professional Summary','desc':f'Write 3 lines targeting {role}: your experience level, 3 key skills, and the specific value you bring.'},
            {'pri':'Medium', 'title':'Add Missing ATS Keywords',           'desc':f'Naturally integrate into bullet points: {", ".join(miss[:4])}. Recruiters filter resumes by these exact terms.'},
            {'pri':'Medium', 'title':'Link GitHub & Portfolio',            'desc':'Add a GitHub profile URL in the header. Pin 3 best projects. Recruiters and interviewers will check before your round.'},
            {'pri':'Low',    'title':'Standardise Formatting',             'desc':'Use consistent date format (Jan 2023 – May 2024), consistent bullet style, and uniform section spacing throughout.'},
        ],
        'rewrites': [
            {'before':'"Worked on several web development projects"',    'after':'"Built 4 full-stack apps (React + Node.js) deployed on AWS, collectively serving 1,800+ daily active users with 99.9% uptime"'},
            {'before':'"Helped with data analysis tasks for the team"',  'after':'"Analysed customer churn data using Python/Pandas, identified 3 root causes, enabling a retention strategy that reduced churn by 22%"'},
            {'before':'"Was a good team player throughout the project"', 'after':'"Collaborated with cross-functional team of 9 (FE, BE, QA, Design) using Agile/Scrum; maintained 97% sprint completion across 8-month engagement"'},
        ]
    }

# ── Agent Chat ────────────────────────────────────────────
@app.route('/api/agent/chat', methods=['POST'])
def agent_chat():
    body     = request.json or {}
    messages = body.get('messages', [])
    profile  = body.get('profile', {})

    reply = _claude_agent(messages, profile) if API_KEY else None
    if not reply:
        reply = _smart_reply(messages[-1]['content'] if messages else '', profile)
    return jsonify({'reply': reply})


def _claude_agent(messages, profile):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=API_KEY)

        ctx = ''
        if profile.get('name'):     ctx += f"Student name: {profile['name']}. "
        if profile.get('role'):     ctx += f"Target role: {profile['role']}. "
        if profile.get('degree'):   ctx += f"Degree: {profile['degree']} in {profile.get('major','')}. "
        if profile.get('skills'):   ctx += f"Skills: {', '.join(profile['skills'][:8])}. "
        if profile.get('exp'):      ctx += f"Experience: {profile['exp']}. "

        system = f"""You are Vidya, an expert AI Career Mentor on the VidyaGuide platform for students and early-career professionals in India.

You specialise in:
- Career planning, roadmaps, and goal setting for tech and non-tech roles
- Resume writing, ATS optimisation, LinkedIn profile improvement
- Skill gap analysis and personalised learning path recommendations
- Interview preparation (DSA, system design, behavioural, HR rounds)
- Salary benchmarks, negotiation strategies, and job search tactics
- Indian job market insights (startups, MNCs, FAANG India, campus placements)
- Higher education guidance (MS, MBA, certifications)

{f'Student context: {ctx}' if ctx else ''}

Style guidelines:
- Be warm, encouraging, and highly specific — avoid generic platitudes
- Use **bold** for key terms and bullet points for clarity
- Reference India-specific context (salary in LPA, Indian companies, college tiers)
- Name specific tools, platforms, and resources
- Keep responses 180–300 words unless more depth is explicitly requested
- End complex answers with a follow-up question to keep engagement"""

        msg = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=900,
            system=system,
            messages=[{'role':m['role'],'content':m['content']} for m in messages[-12:]]
        )
        return msg.content[0].text
    except Exception as e:
        print(f'[Claude agent] {e}')
        return None


def _smart_reply(msg, profile):
    m    = msg.lower()
    role = profile.get('role', 'software engineer')

    if re.search(r'resume|cv|curriculum', m):
        return f"""**Resume Tips for {role.title()}:**

**3 Rules That Matter Most:**
• **Quantify everything** — "reduced API latency by 40%" > "improved performance"
• **Keywords first** — mirror exact language from the job description
• **Action verbs** — Built, Led, Designed, Optimised, Delivered, Reduced

**ATS Checklist:**
• Standard headings (Experience, Education, Skills, Projects)
• No tables, columns, or graphics — ATS cannot parse them
• PDF format unless instructed otherwise
• 10–12pt font, your name at 16–18pt at the top

**For {role.title()}:** Always include GitHub link, live project URLs, and relevant certifications in the header area.

Want me to rewrite specific bullet points from your resume?"""

    if re.search(r'interview|placement|crack|offer', m):
        return """**Interview Prep Strategy 💼**

**Technical Preparation:**
• **DSA:** Striver's A2Z Sheet — structured 450 problems, perfect for placements
• **System Design:** Grokking System Design (paid) or System Design Primer (free GitHub)
• **Coding:** 3 LeetCode problems per day, focus on patterns not brute force

**Prep Timeline:**
• 3 months before → DSA intensive + build 2 solid projects
• 1 month before → Company-specific prep + mock interviews on Pramp
• 1 week before → Research company, Glassdoor reviews, practice STAR stories

**Behavioural Rounds:**
Prepare 6 STAR stories covering: leadership, failure & learning, conflict resolution, biggest achievement, cross-team work, and handling ambiguity.

**Key Insight:** Thinking out loud during coding rounds impresses interviewers far more than silent solving.

Which company or interview type are you preparing for?"""

    if re.search(r'skill|learn|course|study|roadmap', m):
        return f"""**Must-Have Skills for {role.title()} in 2025 ⚡**

**Tier 1 — Non-Negotiable:**
• DSA fundamentals (every product company tests this)
• Primary language mastery (Python or JavaScript/TypeScript)
• SQL — required in 80%+ of tech roles
• Git/GitHub — must be fluent, not just aware

**Tier 2 — Strong Differentiator:**
• Cloud basics (AWS free tier — hands-on practice)
• Docker + basic containerisation
• System design fundamentals

**Trending in 2025:**
• AI/ML integration into products — massive hiring signal
• Open source contributions on GitHub
• Technical writing and documentation

**Free Learning Path:**
CS50 (Harvard) → Striver's DSA → The Odin Project → AWS Free Tier

**Daily rule:** 45 focused minutes > 4 distracted hours.

Want a personalised 90-day study plan for your specific target role?"""

    if re.search(r'salary|pay|lpa|ctc|offer|negotiate|package', m):
        return """**India Tech Salary Guide 2025 💰**

**Fresher Ranges by Company Type:**
• Service companies (TCS, Infosys, Wipro): ₹3.5–6 LPA
• Mid-tier product companies (Freshworks, Zoho): ₹8–16 LPA
• Top startups (Razorpay, CRED, Swiggy, Zepto): ₹15–30 LPA
• FAANG India (Google, Amazon, Microsoft): ₹28–60 LPA

**Negotiation Playbook:**
1. Research first — Glassdoor, levels.fyi, LinkedIn Salary
2. Never reveal your number first — let them make the offer
3. Counter 15–20% above their initial number
4. Negotiate the full package: base salary + ESOPs + joining bonus + WFH flexibility

**What Multiplies Your Package:**
✅ Strong DSA + system design = 2–3x higher offers
✅ A competing offer (even informal — mention it confidently)
✅ Visible projects with real users / stars on GitHub
✅ Relevant internship at a reputed company

What specific offer are you evaluating? I can help you craft a negotiation response!"""

    return f"""Great question! Here's focused guidance for you as an aspiring **{role}**:

**What Matters Most Right Now:**
• Define a clear 90-day goal with specific, measurable outcomes
• Identify your top 3 skill gaps by studying real job descriptions for your target role
• Build one project this month that directly demonstrates those missing skills

**The 2025 Reality:**
Indian companies in 2025 value **demonstrated skills** over degrees alone. Recruiters spend 6 seconds on a resume — your GitHub and projects are your real portfolio.

**Your Next 3 Actions:**
1. Complete your VidyaGuide profile → enables personalised AI recommendations
2. Upload your resume → get your ATS score and improvement plan
3. Review the career roadmap → see your skill gaps vs. role requirements

**Consistency beats intensity.** Students who improve 1% every day for 6 months are dramatically more employable than those who have intense 2-week study sprints.

Could you share more about your specific situation? What's your biggest challenge right now?"""

# ── Skills Assessment ─────────────────────────────────────
@app.route('/api/skills/assess', methods=['POST'])
def assess_skills():
    body    = request.json or {}
    skills  = [s.lower() for s in body.get('skills', [])]
    role    = body.get('target_role', 'Software Engineer')

    REQS = {
        'Software Engineer':    ['python','javascript','data structures','algorithms','git','sql','system design'],
        'Data Scientist':       ['python','sql','machine learning','statistics','pandas','data visualisation'],
        'Data Analyst':         ['sql','excel','python','tableau','statistics','data cleaning'],
        'Product Manager':      ['agile','user research','data analysis','roadmap','sql','figma'],
        'DevOps Engineer':      ['linux','docker','kubernetes','ci/cd','aws','scripting'],
        'Full-Stack Developer': ['html','css','javascript','react','node.js','sql','git'],
    }
    req  = REQS.get(role, REQS['Software Engineer'])
    have = [r for r in req if any(r in s or s in r for s in skills)]
    miss = [r for r in req if r not in have]
    score= round(len(have)/len(req)*100) if req else 0

    return jsonify({
        'score':         score,
        'have_skills':   have,
        'miss_skills':   miss,
        'total_required':len(req),
        'recommendation':f'You have {len(have)}/{len(req)} key skills for {role}. Priority gaps: {", ".join(miss[:3])}'
    })

# ── Career Paths ──────────────────────────────────────────
@app.route('/api/career/paths')
def career_paths():
    return jsonify({'paths': [
        {'id':'swe',    'title':'Software Engineer',      'salary':'₹6–22 LPA', 'growth':'+32%'},
        {'id':'ds',     'title':'Data Scientist',         'salary':'₹7–26 LPA', 'growth':'+46%'},
        {'id':'pm',     'title':'Product Manager',        'salary':'₹10–32 LPA','growth':'+38%'},
        {'id':'devops', 'title':'DevOps / Cloud Engineer','salary':'₹8–24 LPA', 'growth':'+36%'},
        {'id':'fs',     'title':'Full-Stack Developer',   'salary':'₹6–20 LPA', 'growth':'+30%'},
        {'id':'da',     'title':'Data Analyst',           'salary':'₹4–14 LPA', 'growth':'+28%'},
        {'id':'ux',     'title':'UX Designer',            'salary':'₹5–18 LPA', 'growth':'+33%'},
        {'id':'cyber',  'title':'Cybersecurity Analyst',  'salary':'₹7–22 LPA', 'growth':'+40%'},
    ]})

# ── Profile ───────────────────────────────────────────────
@app.route('/api/profile', methods=['POST'])
def save_profile():
    # In production: save to DB
    return jsonify({'status': 'saved'})

# ── Main ──────────────────────────────────────────────────
if __name__ == '__main__':
    banner = '\n'.join([
        '=' * 52,
        '  ⬡  VidyaGuide AI Backend  v2.0',
        '     http://localhost:5000',
        '=' * 52,
        f'  AI Mode: {"✅ Claude API Active" if API_KEY else "⚠  Demo mode (set ANTHROPIC_API_KEY)"}',
        '=' * 52
    ])
    print(banner)
    app.run(debug=True, host='0.0.0.0', port=5000)
