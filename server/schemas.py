from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String(required=True)
    equipment_needed = fields.Boolean()


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=0, max=600))
    notes = fields.String()


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    reps = fields.Integer(validate=validate.Range(min=0))
    sets = fields.Integer(validate=validate.Range(min=0))
    duration_seconds = fields.Integer(validate=validate.Range(min=0))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)
    workout = fields.Nested(WorkoutSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, dump_only=True, exclude=('workout',)
    )


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, dump_only=True, exclude=('exercise',)
    )
