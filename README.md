# Sentiment Analyzer — Project 1

A local AI-powered sentiment analysis web app built with Python, HuggingFace Transformers, and Streamlit. Type any text and the app tells you whether it is Positive, Negative, or Neutral — with a confidence score. Runs 100% on your local machine with no API keys and no cloud costs.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
3. [Installing Dependencies](#installing-dependencies)
4. [How to Run the App](#how-to-run-the-app)
5. [Code Walkthrough — Line by Line](#code-walkthrough--line-by-line)
6. [Example Test Inputs](#example-test-inputs)

---

## Requirements

- Python 3.10 or higher (required for `match/case` syntax)
- Windows 10/11 (also works on Mac and Linux)
- Internet connection for the **first run only** (to download the AI model, ~250MB)
- After that, fully offline

---

## Setting Up a Virtual Environment

A virtual environment (venv) is like a clean, isolated box for your project. It keeps the libraries you install here separate from the rest of your computer, so nothing clashes with other Python projects you might have.

### Step 1 — Open your terminal

On Windows, search for **PowerShell** or **Command Prompt** in the Start menu and open it.

### Step 2 — Navigate to your project folder

```bash
mkdir sentiment-analyzer
cd sentiment-analyzer
```

### Step 3 — Create the virtual environment

```bash
python3 -m venv venv
```

This creates a folder called `venv` inside your project directory. That folder holds its own copy of Python and will store all the libraries we install next.

> On Windows, if `python3` does not work, try `python` instead.

### Step 4 — Activate the virtual environment

```bash
# On Windows (PowerShell)
venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
venv\Scripts\activate.bat

# On Mac / Linux
source venv/bin/activate
```

Once activated, you will see `(venv)` at the start of your terminal line. That means you are now inside the virtual environment.

### Step 5 — Deactivating (when you are done for the day)

```bash
deactivate
```

This exits the virtual environment. Next time you return, just run the activate command again from Step 4.

---

## Installing Dependencies

With your virtual environment activated, run:

```bash
pip install transformers torch streamlit
```

This installs three libraries:

| Library        | What it does                                                      |
| -------------- | ----------------------------------------------------------------- |
| `transformers` | HuggingFace library — gives you access to pre-trained AI models   |
| `torch`        | PyTorch — the engine that runs the AI math under the hood         |
| `streamlit`    | Turns your Python script into a web app with almost no extra code |

---

## How to Run the App

### Step 1 — Create the app file

Inside your `sentiment-analyzer` folder, create a new file called `app.py` and paste the full code into it (see the Code Walkthrough section below for the complete code).

### Step 2 — Make sure your virtual environment is active

You should see `(venv)` in your terminal. If not, run the activate command from the setup section above.

### Step 3 — Run the app

```bash
streamlit run app.py
```

### Step 4 — Open in your browser

Streamlit will automatically open your browser at:

```
http://localhost:8501
```

If it does not open automatically, copy and paste that URL into your browser manually.

> The **first run** will download the AI model (about 250MB). This happens once. After that, the app loads instantly and works fully offline.

---

## Code Walkthrough — Line by Line

Here is the complete code followed by a detailed explanation of every single line.

### Full Code

```python
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Sentiment Analyzer")
st.title("Sentiment Analyzer")
st.write("A Text Sentiment Analyzer")

user_input = st.text_area("Enter your text to analyze its sentiment:")

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

classifier = load_model()

if st.button("Analyze"):
    if user_input.strip():
        result = classifier(user_input)[0]
        label = result["label"]
        confidence = round(result["score"] * 100, 2)

        match label:
            case "POSITIVE":
                st.success(f"Positive - {confidence}% confidence")
            case "NEGATIVE":
                st.error(f"Negative - {confidence}% confidence")
            case "NEUTRAL":
                st.info(f"Neutral - {confidence}% confidence")
            case _:
                st.warning(f"Unknown sentiment")
    else:
        st.warning("Input is invalid!")
```

### Line-by-Line Explanation

---

#### Lines 1–2 — Importing the tools

```python
import streamlit as st
from transformers import pipeline
```

Think of `import` like opening a toolbox before you start a job. You are pulling in two toolboxes here:

- `streamlit` is your **UI toolbox** — it builds the web page and all its buttons, text boxes, and colored result cards.
- `transformers` is your **AI toolbox** — it gives you access to pre-trained models that already understand human language.

The `as st` part is just a nickname. Instead of typing `streamlit.title(...)` every time, you can just type `st.title(...)`. Saves a lot of typing.

---

#### Lines 4–6 — Setting up the page

```python
st.set_page_config(page_title="Sentiment Analyzer")
st.title("Sentiment Analyzer")
st.write("A Text Sentiment Analyzer")
```

These three lines build the top section of your web page:

- `set_page_config` controls what appears in the **browser tab** — just the title in this version (the icon has been removed).
- `st.title` puts a **large heading** on the page.
- `st.write` puts a short **description** below the heading.

In Streamlit, one line of Python equals one element on the page. It is designed to be that simple.

---

#### Lines 8–10 — Loading the AI model

```python
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")
```

This is the most important part of the whole app — this is where the AI brain gets loaded.

- `pipeline("sentiment-analysis")` connects to HuggingFace and downloads a pre-trained **BERT model** that already knows how to detect emotions in text. You do not train anything yourself — the model has already been trained on millions of sentences by HuggingFace.
- `def load_model():` wraps it in a function so we can call it cleanly.
- `@st.cache_resource` is a **decorator** — a special instruction placed above a function. It tells Streamlit: _"Run this function once, store the result in memory, and never run it again for the rest of the session."_ Without this, the app would reload the entire AI model every single time you click the Analyze button, which would be extremely slow.

---

#### Line 12 — Activating the model

```python
classifier = load_model()
```

This line actually calls the function above and stores the loaded AI model in a variable called `classifier`. From this point on, `classifier` is your AI — it is ready to accept text and return a sentiment result.

---

#### Line 14 — The text input box

```python
user_input = st.text_area("Enter your text to analyze its sentiment:")
```

`st.text_area` draws a multi-line text box on the page. The label above the box now reads `"Enter your text to analyze its sentiment:"`. Whatever the user types into it gets stored in the variable `user_input`. The `height` parameter has been removed, so Streamlit uses its default height automatically.

---

#### Line 16 — The Analyze button

```python
if st.button("Analyze"):
```

`st.button` draws a clickable button labeled "Analyze" on the page. The `if` means: **everything indented below this line only runs when the user clicks the button.**

An important thing to understand about Streamlit: every time the user does anything — types text, clicks a button — Streamlit re-runs the entire Python script from top to bottom. The `if st.button(...)` acts as a gate, so the analysis code only fires on an actual click.

---

#### Line 17 — Guard against empty input

```python
    if user_input.strip():
```

`.strip()` removes any leading or trailing blank spaces from the text. If the user just pressed the spacebar a few times and then clicked Analyze, this line catches that. In Python, an empty string is considered "falsy," meaning the `if` block will not run if there is nothing real to analyze.

---

#### Lines 16–18 — Running the AI

```python
        result = classifier(user_input)[0]
        label = result["label"]
        confidence = round(result["score"] * 10, 2)
```

- `classifier(user_input)` is where the actual AI analysis happens. You are feeding the user's text directly into the BERT model.
- The model returns a **list** of results. We add `[0]` at the end to grab just the first (and only) result from that list.
- `result["label"]` extracts just the word — either `"POSITIVE"`, `"NEGATIVE"`, or `"NEUTRAL"`.
- `result["score"]` is a decimal between 0 and 1, like `0.9876`, representing the model's confidence.
- Multiplying by `10` shifts it one decimal place — so `0.9876` becomes `9.876`, trimmed to `9.88` by `round(..., 2)`.

> The `st.spinner` loading animation has been removed in this version. The result appears immediately after clicking Analyze.

The result object looks like this internally:

```python
{"label": "POSITIVE", "score": 0.9876}
```

---

#### Lines 20–27 — Displaying the result with match/case

```python
        match label:
            case "POSITIVE":
                st.success(f"Positive - {confidence}% confidence")
            case "NEGATIVE":
                st.error(f"Negative - {confidence}% confidence")
            case "NEUTRAL":
                st.info(f"Neutral - {confidence}% confidence")
            case _:
                st.warning(f"Unknown sentiment")
```

This is Python's **match/case** statement — introduced in Python 3.10. It is the Python equivalent of a switch statement in other languages like JavaScript or C#. Instead of writing a chain of `if / elif / elif / else`, you write `match` once and then list each possible `case` cleanly below it.

Think of it like a sorting machine at a post office. The label comes in, and the machine checks: is it POSITIVE? Send it to the green bin. Is it NEGATIVE? Send it to the red bin. And so on.

- `match label:` — starts the switch. Python will check `label` against each case below.
- `case "POSITIVE":` — runs if the label is exactly the string `"POSITIVE"`. Shows a green success box.
- `case "NEGATIVE":` — runs if the label is `"NEGATIVE"`. Shows a red error box.
- `case "NEUTRAL":` — runs if the label is `"NEUTRAL"`. Shows a blue info box.
- `case _:` — the **wildcard/default case**. The underscore `_` means "anything that didn't match above." This is your safety net — if the model returns an unexpected label, the app still handles it gracefully with a yellow warning instead of crashing.

Streamlit's colored alert boxes used here:

| Function          | Color  | Used for           |
| ----------------- | ------ | ------------------ |
| `st.success(...)` | Green  | Positive sentiment |
| `st.error(...)`   | Red    | Negative sentiment |
| `st.info(...)`    | Blue   | Neutral sentiment  |
| `st.warning(...)` | Yellow | Unknown / fallback |

The `f"..."` syntax is called an **f-string** — Python's way of embedding a variable directly inside a string. So if `confidence = 9.88`, then `f"Positive - {confidence}% confidence"` becomes `"Positive - 9.88% confidence"` automatically.

---

#### Lines 28–29 — The empty input warning

```python
    else:
        st.warning("Input is invalid!")
```

This is the fallback for when the user clicks Analyze without typing anything. `st.warning` shows a **yellow warning box** with the message. It is a simple but important guard rail that prevents the app from crashing on empty input.

---

## Example Test Inputs

Try these out once your app is running:

| Input                                                          | Expected Result                  |
| -------------------------------------------------------------- | -------------------------------- |
| "This product is absolutely amazing, best purchase I've made!" | POSITIVE, high confidence        |
| "Terrible experience, never buying from this company again."   | NEGATIVE, high confidence        |
| "The package arrived on Tuesday."                              | NEUTRAL or low-confidence result |
| "I am so happy with the service, truly outstanding!"           | POSITIVE, high confidence        |
| "The food was okay, nothing special."                          | NEGATIVE or NEUTRAL              |

---

## Project Info

- Part of a 5-project AI engineering portfolio
- Stack: Python, HuggingFace Transformers, PyTorch, Streamlit
- Cost: Free — runs entirely on your local machine
- Internet required: First run only (model download)
