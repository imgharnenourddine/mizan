<div align="center">

# ميزان · Mizan

### *L'agent IA de bien-être étudiant*

<br/>

> **"Il connaît ta journée avant que tu lui parles."**

<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![Claude API](https://img.shields.io/badge/Claude-Sonnet_4.6-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Aiven-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://aiven.io)
[![Hackathon](https://img.shields.io/badge/Wellness_%26_Agent_Challenge-2026-6C63FF?style=for-the-badge)](https://enset.ma)

<br/>

**Wellness & Agent Challenge 2026 · ENSET Mohammedia · Eudaimonia Club**

</div>

---

## 📖 Table des matières

- [Le concept](#-le-concept)
- [Le problème qu'on résout](#-le-problème-quon-résout)
- [Comment ça marche](#-comment-ça-marche)
- [Features complètes](#-features-complètes)
- [Architecture](#-architecture)
- [Stack technique](#-stack-technique)
- [Structure du projet](#-structure-du-projet)
- [Installation & Setup](#-installation--setup)
- [Variables d'environnement](#-variables-denvironnement)
- [Division des tâches](#-division-des-tâches)
- [Roadmap MVP](#-roadmap-mvp)
- [L'équipe](#-léquipe)

---

## 💡 Le concept

**Mizan** est un agent IA contextuel de bien-être étudiant. Il ne attend pas que tu lui parles — il t'observe dans le temps, apprend ton profil, et agit **proactivement** en croisant ton état émotionnel réel avec ta charge académique réelle.

Quand tu ouvres l'app le matin, Mizan sait déjà :

- Ce que tu as comme cours aujourd'hui et à quelle heure
- Si un examen approche dans les 3 prochains jours
- Comment tu te sentais hier soir
- Combien tu as dormi
- Ton pattern émotionnel des 7 derniers jours

Donc au lieu de demander *"qu'est-ce que tu as à faire aujourd'hui ?"*, il dit directement :

> *"Tu as cours de 8h à 12h, et ton examen d'Analyse est dans 2 jours. Comment tu te sens par rapport à ça ?"*

C'est là que ça devient vraiment puissant.

---

## 🎯 Le problème qu'on résout

Les étudiants jonglent entre cours, examens, projets, et bien-être mental — **sans outil qui comprend les deux à la fois.** Les apps de bien-être ne connaissent pas ton emploi du temps. Les apps académiques ne connaissent pas ton état mental.

Mizan est le premier agent qui **croise les deux** avec un contexte institutionnel réel.

---

## ⚙️ Comment ça marche

### La journée type avec Mizan

```
🌅 MATIN
   ↓
Mizan lit ton emploi du temps du jour
Mizan vérifie tes examens dans les 3 prochains jours
Mizan analyse ton pattern des derniers jours
   ↓
Briefing complet : "Tu as cours de 8h à 12h. Examen d'Analyse dans 2 jours."
2 questions rapides : humeur + sommeil
   ↓
✅ Plan de journée personnalisé généré

🌙 SOIR
   ↓
Check-in rapide
Proposition révision si bon état / récupération si fatigué
Bilan des objectifs du jour
```

### La structure institutionnelle pré-chargée

L'admin configure la plateforme **une seule fois** :

```
ENSET Mohammedia
   └── Département
        └── Filière
             └── Promotion
                  ├── Étudiants       (CSV trombinoscope)
                  ├── Emploi du temps (CSV)
                  ├── Planning examens (CSV)
                  └── Projets         (CSV)
```

Quand l'étudiant active son compte, il trouve **déjà** son emploi du temps, ses examens, et sa filière. Il n'entre rien manuellement.

---

## ✨ Features complètes

### 🌅 Check-in du matin
- Briefing complet de la journée avant toute question
- 2 questions seulement : humeur (1-5) + heures de sommeil
- Plan de journée généré en croisant état émotionnel + charge réelle

### 🌙 Check-in du soir
- Bilan des objectifs du jour
- Proposition de révision du cours si bon état émotionnel
- Si fatigué → proposition récupération, pas de révision

### 🎯 Modes de travail (sélection manuelle)

| Mode | Icône |
|------|-------|
| Révision | 📚 |
| Examen | ✍️ |
| Projet | 💻 |
| Repos | 😴 |
| Sport | 🏃 |
| Cours | 🎓 |

Mizan croise les modes avec l'humeur :
> *"Cette semaine tu as passé 80% en révision et ton humeur a baissé jeudi et vendredi. Tu manques de temps de repos."*

### 📊 Historique & visualisation
- Graphe d'humeur sur 7, 14, 30 jours
- Moyenne de sommeil hebdomadaire
- Jours de stress vs jours calmes
- Répartition des modes de travail par semaine

### 🎯 Objectifs personnels
- L'étudiant fixe ses objectifs (dormir 7h, sport 20min, réviser 3h)
- Mizan suit, célèbre les progrès, réajuste si non atteints

### 📚 Révision intelligente
Si bon état émotionnel après le cours :
> *"Tu te sens bien. Tu as eu Algorithmes ce matin — tu veux que je te prépare une révision rapide ?"*
→ Résumé des points clés + questions de révision + timing suggéré

### 🔔 Alertes proactives
- **Pré-examen** : Intensification du suivi 3 jours avant chaque examen
- **Surcharge** : Emploi du temps chargé + humeur basse → conseils adaptés
- **Stress prolongé** : 3 jours consécutifs → suggestion douce de parler à un conseiller
- **Jour libre** : Pas de cours → proposition plan révision ou récupération selon état

### 🧠 Ressources intelligentes
Proposées selon l'état détecté :
- Anxiété → techniques de méditation
- Procrastination → méthode Pomodoro
- Fatigue chronique → article sur le sommeil

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                 │
│   Check-in · Plan journée · Graphes · Modes          │
└────────────────────┬────────────────────────────────┘
                     │ REST API + WebSocket
┌────────────────────▼────────────────────────────────┐
│                  Backend (FastAPI)                    │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Auth Service│  │Institutional │  │Student Svc  │ │
│  │ JWT + RBAC  │  │School/Filière│  │Profils CSV  │ │
│  └─────────────┘  └──────────────┘  └─────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │              Agent Mizan (Claude API)            │ │
│  │                                                   │ │
│  │  Context Builder → Claude Sonnet → Plan Parser   │ │
│  │                                                   │ │
│  │  Inputs: emploi du temps + examens + humeur       │ │
│  │          + sommeil + modes + historique           │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Checkin Svc │  │  Goals Svc   │  │Analytics Svc│ │
│  └─────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              PostgreSQL (Aiven Cloud)                 │
└─────────────────────────────────────────────────────┘
```

---

## 🛠 Stack technique

| Couche | Technologie |
|--------|-------------|
| **Agent IA** | Claude API `claude-sonnet-4-6` |
| **Backend** | FastAPI · Python 3.12 |
| **Base de données** | PostgreSQL · Aiven Cloud |
| **ORM** | SQLAlchemy 2.0 async |
| **Migrations** | Alembic |
| **Auth** | JWT · passlib bcrypt |
| **Frontend** | Next.js 14 · TypeScript |
| **UI** | Tailwind CSS · shadcn/ui |
| **Graphes** | Recharts |
| **Temps réel** | WebSockets natifs |
| **Déploiement** | Railway (backend) · Vercel (frontend) |

---

## 📁 Structure du projet

```
mizan/
├── mizan-backend/
│   ├── app/
│   │   ├── api/v1/routes/
│   │   │   ├── auth.py
│   │   │   ├── institutional.py
│   │   │   ├── students.py
│   │   │   ├── checkins.py
│   │   │   ├── goals.py
│   │   │   ├── modes.py
│   │   │   ├── agent.py
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── institutional_service.py
│   │   │   ├── student_service.py
│   │   │   ├── checkin_service.py
│   │   │   ├── goal_service.py
│   │   │   ├── mode_service.py
│   │   │   ├── agent_service.py        ← Le cœur de Mizan
│   │   │   ├── context_builder.py      ← Construit le contexte pour Claude
│   │   │   └── analytics_service.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── institution.py
│   │   │   ├── student.py
│   │   │   ├── checkin.py
│   │   │   ├── goal.py
│   │   │   ├── mode_session.py
│   │   │   └── resource.py
│   │   ├── schemas/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── dependencies.py
│   │   └── utils/
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── main.py
│
└── mizan-frontend/
    ├── app/
    │   ├── (auth)/login/
    │   ├── dashboard/
    │   ├── checkin/morning/
    │   ├── checkin/evening/
    │   ├── modes/
    │   ├── goals/
    │   ├── history/
    │   └── admin/
    ├── components/
    ├── lib/
    └── public/
```

---

## 🚀 Installation & Setup

### Prérequis
- Python 3.12+
- Node.js 18+
- Compte [Aiven](https://aiven.io) (PostgreSQL free tier)
- Clé API [Anthropic](https://console.anthropic.com)

### Backend

```bash
# 1. Cloner le repo
git clone https://github.com/[votre-org]/mizan.git
cd mizan/mizan-backend

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Lancer les migrations
alembic upgrade head

# 6. Démarrer le serveur
uvicorn main:app --reload
```

### Frontend

```bash
cd mizan/mizan-frontend

# 1. Installer les dépendances
npm install

# 2. Configurer
cp .env.local.example .env.local
# Éditer .env.local

# 3. Démarrer
npm run dev
```

Backend disponible sur `http://localhost:8000`  
Frontend disponible sur `http://localhost:3000`  
Documentation API sur `http://localhost:8000/docs`

---

## 🔐 Variables d'environnement

### Backend `.env`

```env
# Base de données (Aiven PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@host:port/defaultdb?ssl=require

# Sécurité
SECRET_KEY=your-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Claude API
ANTHROPIC_API_KEY=sk-ant-...

# App
APP_ENV=development
```

### Frontend `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

---

## 👥 Division des tâches

### 👤 Développeur 1 — Fondations + Agent

| # | Tâche | Complexité |
|---|-------|-----------|
| 1 | Auth Service (JWT, RBAC, 5 rôles) | 🔴 Complexe |
| 2 | Institutional Service (école/filière/classe) | 🟡 Moyenne |
| 3 | File Service (upload CSV, parsing) | 🟢 Simple |
| 4 | Student Service (profils, trombinoscope) | 🟡 Moyenne |
| 5 | Context Builder (construit le prompt Claude) | 🔴 Complexe |
| 6 | Agent Service (Claude API + plan parser) | 🔴 Complexe |
| 7 | Analytics Service (graphes, patterns) | 🟡 Moyenne |

### 👤 Développeur 2 — Données métier + Frontend

| # | Tâche | Complexité |
|---|-------|-----------|
| 1 | Modèles DB (checkin, goals, modes, resources) | 🟡 Moyenne |
| 2 | Checkin Service (matin/soir, historique) | 🟡 Moyenne |
| 3 | Goal Service (objectifs, suivi, célébration) | 🟢 Simple |
| 4 | Mode Session Service (tracker d'activité) | 🟢 Simple |
| 5 | Pages Frontend (dashboard, check-in, graphes) | 🔴 Complexe |
| 6 | Composants UI (mood picker, plan card, charts) | 🟡 Moyenne |
| 7 | Notification Service (alertes proactives) | 🟡 Moyenne |

> ⚠️ **Point de sync :** Dev 2 attend que Dev 1 finisse Auth Service avant de commencer. Tout le reste avance en parallèle.

---

## 📋 Roadmap MVP

### 🔴 P1 — Obligatoire pour la démo

- [ ] Auth + Login page
- [ ] Upload CSV emploi du temps + examens
- [ ] Check-in du matin (briefing + 2 questions)
- [ ] Génération du plan de journée par Claude
- [ ] Modes de travail (tracker)
- [ ] Dashboard étudiant avec graphe humeur 7 jours

### 🟡 P2 — Important

- [ ] Check-in du soir
- [ ] Objectifs personnels + suivi
- [ ] Alerte pré-examen automatique
- [ ] Détection surcharge (emploi du temps chargé + humeur basse)
- [ ] Dashboard admin

### 🟢 P3 — Bonus

- [ ] Proposition révision intelligente après cours
- [ ] Ressources ciblées (méditation, Pomodoro, sommeil)
- [ ] Alerte conseiller après 3 jours de stress
- [ ] Export rapport hebdomadaire

---

## 📅 Planning Hackathon (3 jours)

```
Jour 1 — Fondations
├── Matin  : Setup DB + Auth + modèles
├── Après-midi : Institutional + Upload CSV + Student
└── Soir   : Context Builder + premiers tests Claude

Jour 2 — Cœur métier
├── Matin  : Agent Service complet + Check-in
├── Après-midi : Frontend Dashboard + Check-in UI
└── Soir   : Modes + Goals + tests intégration

Jour 3 — Finition & Démo
├── Matin  : Graphes + Analytics + polish UI
├── Après-midi : Tests end-to-end + bugfix
└── Soir   : Préparation pitch + démo finale
```

---

## 🌟 Ce qui rend Mizan vraiment agentique

- **Proactif** : n'attend pas que l'étudiant demande quelque chose
- **Contextuel** : croise données institutionnelles réelles + état émotionnel
- **Temporel** : observe dans le temps, apprend les patterns personnels
- **Adaptatif** : change ses recommandations selon l'état du jour
- **Préventif** : détecte les situations à risque avant qu'elles s'aggravent

---

<div align="center">

**Mizan — ميزان**  
*L'équilibre entre performance académique et bien-être étudiant*

**Wellness & Agent Challenge 2026 · ENSET Mohammedia**

`#WELLNESSAGENT` · `#GIEW2026` · `AGENTIC AI` · `WELLBEING`

</div>
