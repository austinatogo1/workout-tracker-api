# Workout Tracker API

A Flask REST API for tracking workouts and the exercises performed during them. Exercises and workouts are independent resources; a join resource, `WorkoutExercise`, connects them and records per-workout details like reps, sets, and duration.

## Tech Stack

- Python 3.8.13
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite
- Pipenv

## Installation

1. **Clone the repository**

```bash
   git clone https://github.com/austinjordan26/workout-tracker-api.git
   cd workout-tracker-api
```

2. **Install Python 3.8.13** (via pyenv, if not already installed)

```bash
   pyenv install 3.8.13
   pyenv local 3.8.13
```

3. **Install dependencies with Pipenv**

```bash
   pipenv install
   pipenv install --dev
```

   This reads the committed `Pipfile`/`Pipfile.lock`, which already pins every dependency to the versions above, including a `setuptools<70` dev constraint required for `ipdb==0.13.9` to build correctly on Python 3.8.

4. **Apply database migrations**

```bash
   cd server
   pipenv run flask db upgrade
```

   This creates `server/app.db` from the migration history already included in the repo. Do **not** run `flask db init` or `flask db migrate` — the migration history already exists; this step only applies it.

5. **Seed the database**

```bash
   pipenv run python seed.py
```

   Safe to re-run — it clears existing data before reseeding, and won't create duplicates.

## Running the Application

From the `server/` directory:

```bash
pipenv run python app.py
```

The API runs at `http://127.0.0.1:5555`.

## Database

Three models, related through a join table:

- **Exercise** — `id`, `name` (unique), `category`, `equipment_needed`
- **Workout** — `id`, `date`, `duration_minutes`, `notes`
- **WorkoutExercise** — `id`, `workout_id`, `exercise_id`, `reps`, `sets`, `duration_seconds`

A `Workout` has many `Exercise`s through `WorkoutExercise`, and vice versa. `WorkoutExercise` is a full resource in its own right, not just a bridge — it holds data (reps, sets, duration) that belongs to a specific exercise *within* a specific workout, not to either side alone.

## Validation

Three layers, each catching different problems:

- **Table constraints** (database-enforced): `Exercise.name` is unique; `Workout.duration_minutes` must be non-negative (`CHECK` constraint). Foreign keys on `WorkoutExercise` are enforced at the SQLite level.
- **Model validations** (`@validates`, Python-level): `Exercise.name` and `Exercise.category` cannot be empty or whitespace-only; `WorkoutExercise.reps`/`sets`/`duration_seconds` cannot be negative.
- **Schema validations** (Marshmallow, request-level): `Exercise.name` length is capped (1–100 characters); `Workout.duration_minutes` must fall within 0–600; `WorkoutExercise.reps`/`sets`/`duration_seconds` must be non-negative when provided.

## API Endpoints

### Workouts

| Method | Route | Purpose |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout with its associated exercises (including reps/sets/duration) |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout (cascades to its `WorkoutExercise` rows) |

**GET /workouts**
- Response: `200`, array of workouts.

**GET /workouts/\<id\>**
- Response: `200` with nested `workout_exercises`, or `404` if not found.

**POST /workouts**
- Body: `{"date": "2026-08-29", "duration_minutes": 45, "notes": "Leg day"}` (`notes` optional)
- Response: `201` with the created workout, or `400` if the body is missing, malformed, or fails validation (e.g. `duration_minutes` outside 0–600).

**DELETE /workouts/\<id\>**
- Response: `200` with a confirmation message, or `404` if not found.

### Exercises

| Method | Route | Purpose |
|---|---|---|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise with the workouts it's been used in |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise (cascades to its `WorkoutExercise` rows) |

**GET /exercises**
- Response: `200`, array of exercises.

**GET /exercises/\<id\>**
- Response: `200` with nested `workout_exercises` (each showing the associated workout), or `404` if not found.

**POST /exercises**
- Body: `{"name": "Squat", "category": "Strength", "equipment_needed": true}` (`equipment_needed` optional)
- Response: `201` with the created exercise.
- Failure cases: `400` if `name`/`category` are missing or `name` exceeds 100 characters (schema); `400` if `name` is empty/whitespace-only (model); `409` if the name already exists (table constraint).

**DELETE /exercises/\<id\>**
- Response: `200` with a confirmation message, or `404` if not found.

### Workout Exercises (join resource)

| Method | Route | Purpose |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Attach an existing exercise to an existing workout |

**POST /workouts/\<workout_id\>/exercises/\<exercise_id\>/workout_exercises**
- Body (all fields optional): `{"reps": 12, "sets": 4, "duration_seconds": 60}`
- Response: `201` with the created `WorkoutExercise`, including nested `workout` and `exercise`.
- Failure cases: `404` if the workout or exercise doesn't exist; `400` if `reps`/`sets`/`duration_seconds` is negative.
