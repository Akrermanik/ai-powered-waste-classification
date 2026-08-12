from database.connection import init_db
from database.predictions import delete_prediction, get_predictions_for_user, insert_prediction
from database.users import create_user, get_user_by_username


def test_database_initialization():
    init_db()
    user = get_user_by_username("missing")
    assert user is None


def test_user_creation_and_duplicate():
    assert create_user("alice", "Alice", "hash1") is True
    assert create_user("alice", "Alice Again", "hash2") is False

    user = get_user_by_username("alice")
    assert user is not None
    assert user["name"] == "Alice"


def test_prediction_insert_and_retrieve():
    create_user("bob", "Bob", "hash")
    user = get_user_by_username("bob")
    assert user is not None

    prediction_id = insert_prediction(
        user_id=user["id"],
        label="Glass",
        confidence=0.88,
        object_count=1,
        inference_time_ms=120.0,
        predictions=[{"class_name": "Glass", "confidence": 0.88}],
    )
    assert prediction_id > 0

    items = get_predictions_for_user(user["id"])
    assert len(items) == 1
    assert items[0]["label"] == "Glass"


def test_prediction_deletion():
    create_user("carol", "Carol", "hash")
    user = get_user_by_username("carol")
    prediction_id = insert_prediction(user["id"], "Paper", 0.7)

    assert delete_prediction(prediction_id, user["id"]) is True
    assert get_predictions_for_user(user["id"]) == []
