# Directory Structure for SaaS Applications

This document outlines a scalable folder structure for FastAPI-based SaaS applications. It's inspired by production setups at successful startups.

---

## Principles

- **Domain-driven** layout (group by feature, not by file type)
- Separation of **infra**, **API**, and **business logic**
- Clear paths for testing and scalability

---

## Recommended Structure

```bash
saas-app/
├── alembic/                # Database migrations
├── src/
│   ├── main.py             # FastAPI app entrypoint
│   ├── config.py           # Global app config
│   ├── database.py         # DB session and engine
│   ├── auth/               # Auth domain
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── dependencies.py
│   │   └── utils.py
│   ├── billing/            # Billing domain
│   │   └── ...
│   ├── users/              # User domain
│   │   └── ...
│   ├── templates/          # HTMX/Jinja2 templates
│   ├── exceptions.py       # Global custom exceptions
│   └── constants.py        # Global constants
├── tests/
│   ├── auth/
│   ├── billing/
│   └── ...
├── .env
├── requirements.txt
└── README.md

## Benefits

- **Scales well** across multiple domains  
- **Easier onboarding** for new developers  
- Keeps **business logic close to API routes**  
- Encourages **modularity** and **reusability**

---

## Naming Conventions

| File              | Purpose                                      |
|-------------------|----------------------------------------------|
| `router.py`       | FastAPI endpoints for the module             |
| `schemas.py`      | Pydantic request/response models             |
| `models.py`       | SQLAlchemy models                            |
| `service.py`      | Business logic layer                         |
| `dependencies.py` | Shared dependency injection functions        |
| `utils.py`        | Small helper functions                       |

---

## Alternatives

If your app is microservice-based, you may have one module per service with duplicated layouts.

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Netflix Dispatch](https://github.com/Netflix/dispatch)
