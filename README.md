# 🚗 Smart Vehicle Purchase Consultant (SVPC)

<p align="center">
  <img src="docs/assets/banner.png" alt="SVPC Banner" width="900">
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)

</p>

An AI-powered vehicle recommendation platform that helps users find the most suitable vehicle based on their budget, lifestyle, preferences, and driving requirements.

The Smart Vehicle Purchase Consultant combines structured questionnaires, intelligent preference inference, fuzzy logic, and Large Language Models (LLMs) to provide personalized vehicle recommendations along with natural language explanations for every recommendation.

---

## ✨ Features

- 🚙 Intelligent vehicle recommendations based on user preferences
- 🧠 AI-powered recommendation explanations using Google Gemini
- 📊 Fuzzy Logic–based decision making for subjective preferences
- 📋 Dynamic questionnaire for capturing user requirements
- 📈 Multi-criteria vehicle ranking engine
- 🔍 Explainable recommendations with reasoning
- 📂 Modular repository-based backend architecture
- ⚡ FastAPI REST API
- 📑 Automatic OpenAPI & Swagger documentation
- 🧪 Comprehensive testing and static type checking
- 🔒 Type-safe configuration and validation with Pydantic

---

# How It Works

The recommendation pipeline consists of multiple stages:

```text
                    User Questionnaire
                             │
                             ▼
                  Feature Extraction
                             │
                             ▼
                 Preference Inference
                             │
                             ▼
                   Fuzzy Logic Engine
                             │
                             ▼
                  Vehicle Ranking Engine
                             │
                             ▼
                Gemini Explanation Engine
                             │
                             ▼
                Personalized Recommendations
```

The system evaluates multiple aspects of a user's preferences including:

- Budget
- Vehicle Type
- Fuel Preference
- Seating Capacity
- Daily Usage
- Highway vs City Driving
- Performance Requirements
- Comfort Preferences
- Safety Priorities
- Technology Features
- Transmission Preference
- Ownership Priorities

These preferences are translated into weighted criteria that are used to rank vehicles from the available dataset.

---

# Technology Stack

## Backend

- FastAPI
- Python 3.13+
- Uvicorn

## AI & Machine Learning

- Google Gemini API
- Scikit-Learn
- Scikit-Fuzzy
- NumPy
- Pandas

## Configuration & Validation

- Pydantic v2
- pydantic-settings
- python-dotenv

## Development Tools

- UV
- Pytest
- Ruff
- MyPy

---

# Project Structure

```text
backend/
│
├── app/
│   ├── ai/
│   ├── api/
│   ├── constants/
│   ├── core/
│   ├── exceptions/
│   ├── lifecycle/
│   ├── middleware/
│   ├── models/
│   ├── monitoring/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── datasets/
│   ├── raw/
│   └── processed/
│
├── artifacts/
├── docs/
├── scripts/
├── tests/
│
├── .env.example
├── pyproject.toml
└── uv.lock
```

---

# API Overview

The backend exposes REST APIs for:

- Vehicle recommendation generation
- Questionnaire processing
- Health monitoring
- AI explanation generation
- Recommendation retrieval

Interactive API documentation is automatically available through Swagger UI.

---

# Installation

## Clone the repository

```bash
git clone https://github.com/<username>/smart-vehicle-purchase-consultant.git

cd smart-vehicle-purchase-consultant/backend
```

---

## Install dependencies

Using UV:

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file using the provided template.

```bash
cp .env.example .env
```

Example configuration:

```env
PROJECT_NAME=Smart Vehicle Purchase Consultant

API_VERSION=1.0.0

API_PREFIX=/api/v1

HOST=127.0.0.1

PORT=8000

DEBUG=True

ENVIRONMENT=development

LOG_LEVEL=INFO

GEMINI_API_KEY=YOUR_API_KEY
```

---

# Running the Application

Development mode:

```bash
uv run uvicorn app.main:app --reload
```

Production mode:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

OpenAPI Specification

```
http://localhost:8000/openapi.json
```

---

# Running Tests

Execute the test suite:

```bash
uv run pytest
```

Run static type checking:

```bash
uv run mypy app
```

Run linting:

```bash
uv run ruff check .
```

---

# Recommendation Pipeline

The recommendation engine follows the workflow below:

1. Collect user preferences through a structured questionnaire.
2. Validate and preprocess user responses.
3. Infer user priorities using rule-based and fuzzy logic techniques.
4. Generate weighted preference scores.
5. Rank vehicles from the available dataset.
6. Generate AI-powered explanations for the highest-ranked vehicles.
7. Return the final ranked recommendations.

---

# Design Principles

The backend is designed around the following principles:

- Clean Architecture
- Separation of Concerns
- Repository Pattern
- Dependency Injection
- Type Safety
- Modular Components
- Scalability
- Maintainability
- Testability
- Extensibility

---

# Security

The application follows common backend security practices including:

- Environment-based configuration
- API key isolation
- Request validation
- Structured exception handling
- Typed configuration
- Input validation through Pydantic

---

# Future Enhancements

Potential future improvements include:

- User authentication and authorization
- User profiles and saved recommendations
- Recommendation history
- Real-time vehicle inventory integration
- Support for multiple LLM providers
- Database-backed persistence
- Admin dashboard
- Recommendation analytics
- Vehicle comparison dashboard
- Hybrid ML + Fuzzy recommendation models

---

# Contributing

Contributions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/your-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push to your branch.

```bash
git push origin feature/your-feature
```

5. Open a Pull Request.

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# Author

**Kshitiz Aggarwal**

B.Tech Information Technology  
Guru Gobind Singh Indraprastha University (GGSIPU)

---

## Acknowledgements

This project builds upon concepts from:

- FastAPI
- Pydantic
- Scikit-Learn
- Scikit-Fuzzy
- Google Gemini
- OpenAPI Specification