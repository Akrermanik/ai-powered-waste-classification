from auth.service import login_user, register_user
from core.history import get_user_prediction, list_user_history, save_prediction


def test_save_and_list_history():
    register_user("hist_user", "History User", "secret123")
    login = login_user("hist_user", "secret123")
    user_id = login["user"]["id"]

    save_prediction(user_id, "Organic", 0.75, object_count=2, inference_time_ms=50.0)
    items = list_user_history(user_id)
    assert len(items) == 1
    assert items[0]["label"] == "Organic"


def test_user_specific_history_isolation():
    register_user("user_a", "User A", "pass-a")
    register_user("user_b", "User B", "pass-b")

    user_a = login_user("user_a", "pass-a")["user"]["id"]
    user_b = login_user("user_b", "pass-b")["user"]["id"]

    pred_id = save_prediction(user_a, "Metal", 0.9)

    assert len(list_user_history(user_a)) == 1
    assert len(list_user_history(user_b)) == 0
    assert get_user_prediction(user_b, pred_id) is None
    assert get_user_prediction(user_a, pred_id) is not None
