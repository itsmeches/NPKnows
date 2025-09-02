# NPKnows — Leaf-Based Bitter Gourd Health Assessment (Phase 2)

A full‑stack project that identifies **NPK deficiency signs on bitter gourd (ampalaya) leaves** from images and provides soil compatibility guidance. The repo contains a **Django** backend that serves a trained **Keras/TensorFlow** model (`saved_model.h5`) via a REST API and a **React + Tailwind** frontend (`my-app/`) for an end‑to‑end user experience.

> ✅ This README is a structured starting point based on the current repo layout. Adjust paths, commands, and versions to match your environment.

---

## Features

* 🌿 Image‑based detection of nutrient deficiencies on bitter gourd leaves (focus on **N**, **P**, **K**).
* 🧠 Pretrained CNN model served by a Django API.
* 🖥️ React frontend with Tailwind UI for uploading images and viewing predictions.
* 📦 Simple local setup; runs frontend and backend separately for DX.

---

## Tech Stack

**Backend**

* Python + Django REST Framework
* TensorFlow / Keras

**Frontend**

* React + Tailwind CSS

**Other**

* SQLite (development)

---

## Repository Structure (high‑level)

```
NPKnows/
├─ api/                     # Django app(s) for the API (adjust name if different)
├─ bitter_gourd_health/     # Project or module for model / training utilities (if applicable)
├─ images/                  # Sample or UI images
├─ my-app/                  # React frontend (Tailwind configured)
├─ node_modules/            # Frontend deps (can be reinstalled)
├─ saved_model.h5           # Trained Keras/TensorFlow classifier
├─ manage.py                # Django entry point
├─ db.sqlite3               # Dev database (auto-created locally)
├─ package.json             # Frontend scripts & deps
├─ tailwind.config.js       # Tailwind config for frontend
├─ postcss.config.js        # PostCSS config for frontend
└─ README.md                # You are here
```

> If you move or rename files (e.g., the model path), update the API code accordingly.

---

## Prerequisites

* **Python** ≥ 3.9 (3.10/3.11 recommended)
* **Node.js** ≥ 18 and **npm** ≥ 9
* OS: Windows/macOS/Linux

---

## Quick Start

### 1) Clone

```bash
git clone https://github.com/itsmeches/NPKnows.git
cd NPKnows
```

### 2) Backend (Django + TensorFlow)

Create a virtual env and install dependencies.

```bash
# Windows (PowerShell)
python -m venv .venv
. .venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# If a requirements.txt exists
pip install -r requirements.txt

# Otherwise install common deps (adjust as needed)
pip install django djangorestframework pillow numpy tensorflow
```

Run migrations and start the dev server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

The API should now be live at `http://localhost:8000/`.

> **Model file**: Ensure `saved_model.h5` is accessible by the API code. If your API expects another path (e.g., inside `api/`), move the file there or update the loader code.

### 3) Frontend (React + Tailwind)

Open a second terminal:

```bash
cd my-app
npm install
# For CRA\ nnpm start
# For Vite
# npm run dev
```

Frontend will typically be available at `http://localhost:3000/` (CRA) or as printed by Vite.

---

## Environment Variables (Backend)

Create a `.env` (or use Django settings) for secrets and config:

```
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
# If the model path is configurable
MODEL_PATH=./saved_model.h5
ALLOWED_HOSTS=localhost,127.0.0.1
```

> If using `python-dotenv` or `django-environ`, load these in `settings.py`.

---

## API (Expected)

Assuming a typical image‑classification endpoint—update to match your implementation.

### `POST /api/predict/`

**Body**: `multipart/form-data` with field `image` (file)

**Response (example):**

```json
{
  "class": "Nitrogen_Deficiency",
  "probabilities": {
    "Nitrogen_Deficiency": 0.82,
    "Phosphorus_Deficiency": 0.10,
    "Potassium_Deficiency": 0.06,
    "Healthy": 0.02
  },
  "advice": "Apply N-rich fertilizer; monitor leaf greenness in 7–10 days."
}
```

**cURL**

```bash
curl -X POST http://localhost:8000/api/predict/ \
  -F "image=@/path/to/leaf.jpg"
```

> If your actual endpoint differs (e.g., `/predict/` or `/api/v1/predict/`), update this section.

---

## Frontend Usage

1. Start the backend (`runserver`).
2. Start the frontend (`npm start` or `npm run dev`).
3. In the web app, upload a leaf image and submit to see the predicted class and guidance.

---

## Training & Dataset (Summary)

* Model: CNN (Keras/TensorFlow) trained on bitter gourd leaf images with labels for **N**, **P**, **K** deficiency and **Healthy**.
* Data: Foldered image dataset or CSV index (update this section with your exact dataset source, splits, and augmentation strategy).
* Export: Saved as `saved_model.h5` included in repo for development. Consider hosting large models via releases or storage for production.

**Repro (sketch):**

```python
# example skeleton – align with your training code
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
  keras.layers.Input((224,224,3)),
  keras.layers.Conv2D(32,3,activation='relu'),
  keras.layers.MaxPooling2D(),
  keras.layers.Conv2D(64,3,activation='relu'),
  keras.layers.MaxPooling2D(),
  keras.layers.Flatten(),
  keras.layers.Dense(128,activation='relu'),
  keras.layers.Dense(4,activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# ... dataset loading & training here ...
model.save('saved_model.h5')
```

---

## Development Tips

* Keep model loading **lazy** (load once at startup) to avoid per‑request overhead.
* Validate image inputs; handle non‑RGB formats.
* For production, consider: gunicorn/uvicorn + nginx, CORS, and model caching.
* Move `db.sqlite3` out of the repo or ignore it for cleanliness.

---

## Troubleshooting

* **TensorFlow install fails on Windows** → Ensure correct Python version and VC++ Build Tools.
* **`ModuleNotFoundError` for DRF** → `pip install djangorestframework` and add to `INSTALLED_APPS`.
* **CORS errors from frontend** → Add `django-cors-headers` and configure allowed origins.
* **Large image upload errors** → Increase Django `DATA_UPLOAD_MAX_MEMORY_SIZE` or use streaming.

---

## Roadmap

* [ ] Confirm/Document exact API routes
* [ ] Add `requirements.txt` and pin versions
* [ ] Add `.env` handling and sample file
* [ ] Document dataset sources & ethics
* [ ] Model evaluation metrics & confusion matrix
* [ ] Dockerfile + Compose for one‑command dev
* [ ] CI for lint/test

---

## Contributors

* Chester (itsmeches)
* JM Reyes
* Kyla Jamito
* Patrick Eva



---

## License

No license specified yet. Consider adding **MIT** or your preferred license.

---

## Acknowledgments

* Faculty advisers, classmates, and farmers who provided domain knowledge
* Open‑source frameworks: Django, DRF, TensorFlow/Keras, React, Tailwind
