# Competitive Intelligence Tracker

An AI-powered agent that monitors competitor websites, detects updates, and alerts you in real time.  
Built during the **AI Agent Hackathon** in just 3 days!

---

## What It Does

Startups often struggle to keep track of competitor product launches, feature updates, and campaigns.  
This project automates that by:

- **Monitoring websites** (e.g., product pages, blogs, announcements)  
- **Detecting changes** in content or version updates  
- **Sending alerts** when something changes  
- **Displaying a dashboard** with:
  - Tracked target links  
  - Recent alerts (with before/after diffs)  
  - Auto-refreshing logs  

Instead of manually checking competitor sites, the agent watches them for you.

---

## How It Works

1. **Target Links** – Add the websites you want to track in the web UI  
2. **Monitoring Loop** – The `monitor.py` script fetches and compares changes  
3. **Version Tracking** – If a site changes (e.g., “Version 1” → “Version 2”), it records the difference  
4. **Alerts Dashboard** – Changes show up as **Recent Alerts** in the tracker web interface  
5. **Dark/Light Theming** – The interface can be customized with different color themes  

**Example Demo Flow (as shown in the video):**

- Add a competitor URL in the dashboard  
- Run the monitor → script detects changes  
- Recent Alerts instantly show what changed  

---

## Project Structure

```bash
 competitive-intel-tracker
┣  monitor.py # Main monitoring script
┣  server.py # Web dashboard (Flask/HTTP server)
┣  templates/ # HTML pages
┣  static/ # CSS themes & styling
┗  README.md
```

---

## Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/competitive-intel-tracker.git
```

```bash
cd competitive-intel-tracker
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

```bash
source venv/bin/activate   # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Use Three terminals

1. On First Terminal Run :

```bash
cd demo-site
python -m http.server 8000
```

On Second Terminal :

```bash
uvicorn app:app --reload --port 8500
```

### 5️⃣ Start monitoring

In Third Terminal :

```bash
python monitor.py
```

---

**This will:**

- Continuously fetch target links
- Compare with previous versions
- Generate alerts when content changes

---

### Built For

- AI Agent Hackathon – 3 days, idea → prototype
- Focused on thinking, building, showing (not just theory)
- Real, working portfolio project to showcase skills

### Contributing

- Want to improve this agent? Fork it, clone it, and send a PR!

### License

- MIT License – free to use and modify.

---
