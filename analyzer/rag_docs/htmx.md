# HTMX Usage Examples with FastAPI

HTMX enables dynamic client-side interactions with server-rendered HTML. It's a great choice for fast development with minimal frontend complexity.

---

## Basic Setup

Include the HTMX script in your HTML template:

```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

## Example: button click loads server response
<button hx-get="/hello" hx-target="#message" hx-swap="innerHTML">
  Say Hello
</button>
<div id="message"></div>


# HTMX Usage Examples with FastAPI

This guide shows how to integrate HTMX with FastAPI to create interactive UIs without writing custom JavaScript.

---

## Example: Button Click Loads Server Response

### HTML

```html
<button hx-get="/hello" hx-target="#message" hx-swap="innerHTML">
  Say Hello
</button>
<div id="message"></div>
``` 

# HTMX Usage Examples

## Example: Button Click Loads Server Response

**HTML**

```html
<button hx-get="/hello" hx-target="#message" hx-swap="innerHTML">
  Say Hello
</button>
<div id="message"></div>
```

**FastAPI Route**

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/hello", response_class=HTMLResponse)
async def hello():
    return "<p>Hello from the server!</p>"
```

---

## Example: Login Form

**HTML**

```html
<form hx-post="/login" hx-target="#feedback" hx-swap="innerHTML">
  <input type="text" name="username" />
  <input type="password" name="password" />
  <button type="submit">Login</button>
</form>
<div id="feedback"></div>
```

**FastAPI Route**

```python
from fastapi import Form
from fastapi.responses import HTMLResponse

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret":
        return "<p>Login successful!</p>"
    return "<p>Invalid credentials</p>"
```

---

## Example: Inline Editing

**HTML**

```html
<div hx-get="/edit/42" hx-trigger="click" hx-target="this" hx-swap="outerHTML">
  Click to edit
</div>
```

**Server Response**

```python
from fastapi.responses import HTMLResponse

@app.get("/edit/42", response_class=HTMLResponse)
async def edit_item():
    return """
    <input type='text' name='item' value='Editable value' 
      hx-post='/save/42' hx-trigger='blur' hx-target='this' hx-swap='outerHTML' />
    """
```

---

## Best Practices

- Use `hx-swap="outerHTML"` to replace entire elements
- Use `hx-target` to specify where the server response should go
- Use `hx-trigger="blur"` for autosaving on focus loss
- Return `HTMLResponse` from FastAPI for rendering HTML snippets
- Organize your templates using reusable partials

---

## Resources

- [HTMX Docs](https://htmx.org/docs/)
- [FastAPI + HTMX Examples](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [HTMX Patterns](https://htmx.org/examples/)


