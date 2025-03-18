from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError

from app.audio.schemas import LLMOutputSchema
from app.audio.validators import validate_expected_audio_length

router = Blueprint("audio", __name__, url_prefix="/audio")


@router.post("/validate")
def validate_llm_output() -> Response:
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty JSON request"}), 400

        llm_output = LLMOutputSchema.model_validate(data)
        text = validate_expected_audio_length(llm_output.text)

        return jsonify(llm_output.model_dump() | {"text": text})
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
