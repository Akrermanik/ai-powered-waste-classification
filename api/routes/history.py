from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_user
from api.schemas.history import HistoryItem, HistoryListResponse
from core.history import get_user_prediction, list_user_history, remove_user_prediction

router = APIRouter(prefix="/v1/history", tags=["history"])


@router.get("", response_model=HistoryListResponse)
def get_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
) -> HistoryListResponse:
    items = list_user_history(current_user["id"], limit=limit)
    return HistoryListResponse(
        items=[HistoryItem(**item) for item in items],
        count=len(items),
    )


@router.get("/{prediction_id}", response_model=HistoryItem)
def get_history_item(
    prediction_id: int,
    current_user: dict = Depends(get_current_user),
) -> HistoryItem:
    item = get_user_prediction(current_user["id"], prediction_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found",
        )
    return HistoryItem(**item)


@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history_item(
    prediction_id: int,
    current_user: dict = Depends(get_current_user),
) -> None:
    deleted = remove_user_prediction(current_user["id"], prediction_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found",
        )
