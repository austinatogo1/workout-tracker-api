from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


def clear_data():
    """Delete existing rows in dependency order: children before parents."""
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()


def seed_exercises():
    exercises = [
        Exercise(name="Squat", category="Strength", equipment_needed=True),
        Exercise(name="Push Up", category="Strength", equipment_needed=False),
        Exercise(name="Plank", category="Core", equipment_needed=False),
        Exercise(name="Deadlift", category="Strength", equipment_needed=True),
        Exercise(name="Jumping Jacks", category="Cardio", equipment_needed=False),
    ]
    db.session.add_all(exercises)
    db.session.commit()
    return exercises


def seed_workouts():
    workouts = [
        Workout(date=date(2026, 8, 24), duration_minutes=45, notes="Leg day"),
        Workout(date=date(2026, 8, 26), duration_minutes=30, notes="Quick core session"),
        Workout(date=date(2026, 8, 28), duration_minutes=50, notes="Full body"),
    ]
    db.session.add_all(workouts)
    db.session.commit()
    return workouts


def seed_workout_exercises(exercises, workouts):
    squat, push_up, plank, deadlift, jumping_jacks = exercises
    leg_day, core_session, full_body = workouts

    workout_exercises = [
        WorkoutExercise(workout=leg_day, exercise=squat, reps=10, sets=4),
        WorkoutExercise(workout=leg_day, exercise=deadlift, reps=8, sets=3),
        WorkoutExercise(workout=core_session, exercise=plank, sets=3, duration_seconds=60),
        WorkoutExercise(workout=full_body, exercise=squat, reps=12, sets=3),
        WorkoutExercise(workout=full_body, exercise=push_up, reps=15, sets=3),
        WorkoutExercise(workout=full_body, exercise=jumping_jacks, sets=3, duration_seconds=45),
    ]
    db.session.add_all(workout_exercises)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        print("Clearing existing data...")
        clear_data()

        print("Seeding exercises...")
        exercises = seed_exercises()

        print("Seeding workouts...")
        workouts = seed_workouts()

        print("Seeding workout exercises...")
        seed_workout_exercises(exercises, workouts)

        print("Done!")
