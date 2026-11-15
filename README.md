<div align="center">

<!-- Hero Banner with Custom ASCII Portrait & Cyber Aesthetics -->
<a href="https://github.com/Sathurjanv23">
  <img src="assets/banner.png" width="100%" alt="Sathurjan Vijithakumarasena - Hero Banner" />
</a>

<br/><br/>

<!-- Sleek Navigation / Contact Pills -->
<a href="https://github.com/Sathurjanv23">
  <img src="https://img.shields.io/badge/%F0%9F%8C%90_Portfolio-%E2%86%97-14151a?style=for-the-badge&logoColor=white" alt="Portfolio" />
</a>
&nbsp;
<a href="https://www.linkedin.com/in/vijithakumarasena-sathurjan">
  <img src="https://img.shields.io/badge/LinkedIn-%E2%86%97-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
&nbsp;
<a href="mailto:sathurjanv.dev@gmail.com">
  <img src="https://img.shields.io/badge/Email-%E2%86%97-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
</a>
&nbsp;
<img src="https://komarev.com/ghpvc/?username=Sathurjanv23&label=PROFILE+VIEWS&color=f97316&style=for-the-badge" alt="Profile Views" />

<br/><br/>

<!-- Dynamic Terminal Typing Animation -->
<a href="#-architectural-overview">
  <img src="https://readme-typing-svg.herokuapp.com/?lines=Full-Stack+Developer+%7C+Enterprise+Backend+Architect;Modular+Monoliths+%7C+Distributed+Systems+%7C+CQRS;ASP.NET+Core+Web+API+(.NET+10)+%7C+Spring+Boot+3;Next.js+14+%7C+React+%7C+TypeScript+%7C+FastAPI;Building+Web+Platforms+%26+Seeing+Them+Through+to+Production&center=true&width=800&height=46&font=JetBrains+Mono&size=18&color=F97316&pause=1000" alt="Typing SVG" />
</a>

</div>

---

## 🏛️ Architectural Overview & Engineering Philosophy

I am a **Software Engineer & Solutions Architect** with an academic background in **Information Technology (BSc Hons) at the University of Moratuwa**. I specialize in designing and engineering **enterprise-grade backend systems, multi-tenant SaaS platforms, and resilient full-stack architectures**.

My engineering focus spans **modern .NET ecosystems (C#, ASP.NET Core Web API, EF Core)** and **Java enterprise systems (Spring Boot 3, Spring Security)**, paired with **reactive frontend platforms (Next.js 14, React, TypeScript)**. I design systems with an emphasis on **domain boundaries, modular monoliths, selective CQRS, and zero-trust security protocols**.

```
                           ┌────────────────────────────────────────┐
                           │      Modern Web & Edge Clients         │
                           │   Next.js 14 • React • TypeScript      │
                           └───────────────────┬────────────────────┘
                                               │ Secure REST / WebSocket
                           ┌───────────────────▼────────────────────┐
                           │   Core API Gateway & Domain Services   │
                           │ ASP.NET Core (.NET 10) • Spring Boot 3 │
                           └─────────┬────────────────────┬─────────┘
                                     │                    │
                   ┌─────────────────▼────────┐  ┌────────▼────────────────┐
                   │ Data Persistence Tier    │  │ Real-Time & Caching Tier│
                   │ PostgreSQL • EF Core     │  │ Redis Pub/Sub • WS      │
                   │ MongoDB Atlas • MySQL    │  │ AWS S3 Asset Pipeline   │
                   └──────────────────────────┘  └─────────────────────────┘
```

---

## ⚡ Core Technical Competencies

| Architectural Pillar | Core Capabilities & Focus |
| :--- | :--- |
| **System Architecture** | Modular Monoliths, Domain-Driven Design (DDD), Selective CQRS, Multi-Tenant SaaS Isolation, RESTful API Versioning |
| **Enterprise Backend** | C# (.NET 10, ASP.NET Core Web API, EF Core), Java (Spring Boot 3, Spring Security, JPA/Hibernate), Python (FastAPI) |
| **Frontend Engineering** | Next.js 14 (App Router), React.js, TypeScript, Tailwind CSS, State Architecture, Vite |
| **Data Persistence & Cache** | PostgreSQL (Tenant Partitioning, Optimistic Concurrency), MongoDB / Atlas, MySQL, Redis (Caching & Pub/Sub) |
| **Security & Compliance** | JWT, RBAC (Role-Based Access Control), Audit Logging, API Rate Limiting, OWASP Hardening |
| **DevOps & Cloud Native** | Docker, Docker Compose, GitHub Actions (CI/CD Pipelines), AWS S3, Linux/Bash Environments |
| **Real-Time Systems** | WebSocket Communication, Event Dispatchers, Real-Time Telemetry & Notification Pipelines |

---

## 🚀 Flagship Engineered Platforms

### 🏢 MaintenX — Enterprise Multi-Tenant Facility Maintenance & Field Service SaaS
> *An enterprise B2B SaaS platform engineered for facility maintenance, automated work-order dispatching, SLA enforcement, and multi-tenant asset management.*

* **System Design & Core Architecture**:
  * Designed a high-throughput **C# / ASP.NET Core Web API (.NET 10)** modular monolith with clean domain boundaries and selective **CQRS** for high-frequency maintenance logs.
  * Architected a **tenant-aware data isolation layer** with **PostgreSQL** and **Entity Framework Core**, featuring optimistic concurrency control and tamper-proof audit trails.
  * Specified multi-channel client integration for **Next.js** web dashboards and **Flutter** mobile field apps, supported by automated **Docker** CI/CD container workflows.
* **Tech Stack**: `C#` `ASP.NET Core (.NET 10)` `EF Core` `PostgreSQL` `Next.js` `Docker` `CQRS`

---

### 🏥 MedAssist AI X — High-Availability Healthcare & Telemetry Platform
> *A distributed, multi-portal healthcare ecosystem coordinating real-time interactions across Patients, Doctors, and Hospital Administrators.*

* **System Design & Core Architecture**:
  * Built an enterprise **Spring Boot** backend enforcing rigorous **JWT & Spring Security** role-based access control (RBAC).
  * Integrated **Redis** caching for sub-millisecond session lookups and **WebSocket** channels for bi-directional live clinical telemetry and notifications.
  * Implemented an **AWS S3** asset storage pipeline for secure, encrypted medical record exchange alongside containerized **Docker** micro-deployments.
* **Tech Stack**: `Java 17` `Spring Boot 3` `Next.js` `Redis` `WebSocket` `AWS S3` `Docker` `Spring Security`

---

### 🔄 CRMS — Enterprise Change Request & Lifecycle Management System
> *Cognitx Company / University Software Engineering Project — An audit-compliant change control engine orchestrating enterprise software modifications.*

* **System Design & Core Architecture**:
  * Designed structured enterprise workflows across Client, Company, and Admin tiers, featuring PRD lifecycle management and interactive Kanban boards.
  * Implemented stateless **JWT authentication** and granular authorization rules to safeguard sensitive change specifications and approval gates.
  * Developed robust RESTful APIs with **Spring Boot** and **MongoDB** for seamless document tracking, paired with responsive **Next.js / React** frontends.
* **Tech Stack**: `Java` `Spring Boot` `Next.js` `React` `TypeScript` `MongoDB` `REST APIs`

---

### 📊 EduSmart AI — Distributed Student Performance & Risk-Prediction Analytics
> *An analytical data platform supporting academic insights, institutional dashboards, and automated student risk-prediction pipelines.*

* **System Design & Core Architecture**:
  * Architected a dual-backend service model coupling **Spring Boot** enterprise services with high-performance **FastAPI** data-crunching microservices.
  * Automated testing and deployment cycles with **GitHub Actions** and containerized **Docker** environments.
  * Designed MongoDB persistence schemas optimized for high-volume telemetry ingestion and analytical reporting.
* **Tech Stack**: `FastAPI` `Spring Boot` `Next.js` `MongoDB` `Python` `Docker` `GitHub Actions`

---

## 🧰 Technology Arsenal

### 💻 Languages & Runtimes
<p align="left">
  <img src="https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=csharp&logoColor=white" alt="C#" />
  <img src="https://img.shields.io/badge/Java_17+-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/JavaScript_ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" />
  <img src="https://img.shields.io/badge/SQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="SQL" />
  <img src="https://img.shields.io/badge/C%2FC%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++" />
</p>

### ⚙️ Backend & Distributed Architecture
<p align="left">
  <img src="https://img.shields.io/badge/.NET_10-512BD4?style=for-the-badge&logo=dotnet&logoColor=white" alt=".NET 10" />
  <img src="https://img.shields.io/badge/ASP.NET_Core_Web_API-512BD4?style=for-the-badge&logo=dotnet&logoColor=white" alt="ASP.NET Core" />
  <img src="https://img.shields.io/badge/Spring_Boot_3-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot" />
  <img src="https://img.shields.io/badge/Spring_Security-6DB33F?style=for-the-badge&logo=springsecurity&logoColor=white" alt="Spring Security" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/RESTful_APIs-02569B?style=for-the-badge&logo=rest&logoColor=white" alt="REST APIs" />
  <img src="https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socketdotio&logoColor=white" alt="WebSocket" />
</p>

### 🌐 Frontend & User Experience
<p align="left">
  <img src="https://img.shields.io/badge/Next.js_14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/React_18/19-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
</p>

### 🗄️ Database, Caching & Cloud Storage
<p align="left">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Entity_Framework_Core-512BD4?style=for-the-badge&logo=dotnet&logoColor=white" alt="EF Core" />
  <img src="https://img.shields.io/badge/MongoDB_Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/AWS_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" alt="AWS S3" />
</p>

### ☁️ DevOps, CI/CD & Development Tools
<p align="left">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
  <img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman" />
  <img src="https://img.shields.io/badge/IntelliJ_IDEA-000000?style=for-the-badge&logo=intellijidea&logoColor=white" alt="IntelliJ IDEA" />
  <img src="https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white" alt="VS Code" />
  <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white" alt="Figma" />
</p>

---

## 🏆 Honors, Competitions & Certifications

* 🥇 **CryptX 2.0 — Top 20 Performer** | University of Sri Jayewardenepura (2026)
* 🚀 **CodeRally 7.0 Finalist** | Competitive Programming & Algorithmic Problem Solving (2026)
* ⚡ **JPura Xtreme 3.0 Finalist** | High-intensity algorithmic coding hackathon (2026)
* 💡 **Innovate with Ballerina Coding Challenge** | WSO2 (2026)
* 📮 **Postman API Fundamentals Student Expert** | Certified API Design, Testing & Automation (2025)
* 💻 **HackerRank Certified** | Go Programming (Intermediate) & Java Programming (Basic)
* 📊 **DataCamp** | Intermediate SQL Certification
* 🎓 **University of Moratuwa** | Front-End Web Development Specialization

---

## 📊 Engineering Activity & Metrics

<div align="center">

<img height="180" src="https://github-readme-stats.vercel.app/api?username=Sathurjanv23&show_icons=true&hide_border=true&count_private=true&include_all_commits=true&theme=tokyonight&title_color=38bdf8&text_color=94a3b8&icon_color=38bdf8&bg_color=0b0f19" alt="GitHub Stats" />
&nbsp;
<img height="180" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Sathurjanv23&layout=compact&hide_border=true&langs_count=8&theme=tokyonight&title_color=38bdf8&text_color=94a3b8&bg_color=0b0f19" alt="Top Languages" />

<br/><br/>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=Sathurjanv23&theme=tokyonight&hide_border=true&background=0b0f19&ring=38bdf8&fire=38bdf8&currStreakLabel=38bdf8" alt="Streak Stats" />

<br/><br/>

<img width="95%" src="https://github-readme-activity-graph.vercel.app/graph?username=Sathurjanv23&bg_color=0b0f19&color=38bdf8&line=00d4ff&point=ffffff&area=true&hide_border=true&custom_title=Sathurjan's%20Engineering%20Contribution%20Matrix" alt="Contribution Graph" />

<br/><br/>

<img src="https://github-profile-trophy.vercel.app/?username=Sathurjanv23&theme=tokyonight&no-frame=true&no-bg=true&margin-w=10&column=6" alt="Trophies" />

</div>

---

## 🤝 Let's Connect & Build

I am open to **Software Engineering Opportunities, Backend / Full-Stack Roles, and Architectural Collaborations**.

<div align="center">

<a href="https://www.linkedin.com/in/vijithakumarasena-sathurjan">
  <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
&nbsp;
<a href="mailto:sathurjanv.dev@gmail.com">
  <img src="https://img.shields.io/badge/Email-sathurjanv.dev%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
</a>
&nbsp;
<a href="https://github.com/Sathurjanv23">
  <img src="https://img.shields.io/badge/GitHub-Sathurjanv23-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</a>

<br/><br/>

<!-- Footer Wave -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0e12,40:181920,80:272935,100:f97316&height=120&section=footer" width="100%" alt="Footer Banner" />

</div>
