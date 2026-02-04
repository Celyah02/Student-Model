import os
import joblib
import numpy as np
from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

MODEL_PATH = os.path.join(settings.BASE_DIR, 'performance', 'model.pkl')

# Lazy load model to avoid errors at startup
_model = None

def get_model():
    """Load model lazily with error handling."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Please train the model first using: python manage.py shell -> from performance.train_model import train -> train()"
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_page(request):
    return render(request, 'performance/index.html')


@api_view(['POST'])
def predict_performance(request):
    try:
        data = request.data

        # -------- Parse inputs --------
        hours_studied = int(data['hours_studied'])
        sleep_hours = int(data['sleep_hours'])
        previous_scores = int(data['previous_scores'])
        sample_papers = int(data['sample_papers'])
        extracurricular = 1 if data['extracurricular'] else 0

        # -------- BASIC VALIDATION --------
        for name, value in {
            "hours_studied": hours_studied,
            "sleep_hours": sleep_hours,
            "previous_scores": previous_scores,
            "sample_papers": sample_papers,
        }.items():
            if value < 0:
                return Response(
                    {
                        "error": "Invalid input",
                        "cause": f"{name} cannot be negative."
                    },
                    status=400
                )

        # -------- LOGICAL CONSTRAINT --------
        if hours_studied + sleep_hours > 24:
            return Response(
                {
                    "error": "Invalid input",
                    "cause": (
                        "A day has only 24 hours. "
                        "The sum of hours studied and sleep hours exceeds 24."
                    )
                },
                status=400
            )

        # -------- EXTREME LOW-EFFORT RULE --------
        if (
            hours_studied == 0
            and sample_papers == 0
            and previous_scores == 0
            and sleep_hours == 24
        ):
            return Response(
                {
                    "predicted_performance_index": 20.0,
                    "note": (
                        "Prediction overridden: Student showed no academic effort "
                        "and slept the entire day."
                    )
                }
            )

        # -------- ML PREDICTION (NORMAL CASES) --------
        model = get_model()
        features = np.array([[
            hours_studied,
            previous_scores,
            extracurricular,
            sleep_hours,
            sample_papers
        ]])

        prediction = model.predict(features)[0]

        # -------- SAFETY CLAMP --------
        prediction = max(0, min(100, prediction))

        return Response({
            "predicted_performance_index": round(float(prediction), 2)
        })

    except KeyError as e:
        return Response(
            {
                "error": "Missing field",
                "cause": f"Field {str(e)} is required."
            },
            status=400
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
