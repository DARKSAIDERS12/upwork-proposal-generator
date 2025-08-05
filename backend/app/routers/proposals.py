from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.openai_service import OpenAIService
from ..schemas import (
    ProposalGenerationRequest, 
    ProposalGenerationResponse, 
    MultipleProposalsResponse,
    Proposal,
    ProposalCreate
)
from ..models.user import User
from ..models.proposal import Proposal as ProposalModel
from .auth import get_current_user

router = APIRouter(prefix="/proposals", tags=["proposals"])

@router.post("/generate", response_model=ProposalGenerationResponse)
def generate_proposal(
    request: ProposalGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Генерирует предложение на основе данных проекта"""
    
    try:
        # Инициализируем OpenAI сервис
        openai_service = OpenAIService()
        
        # Подготавливаем данные для генерации
        project_data = {
            "project_description": request.project_description,
            "budget_range": request.budget_range,
            "specialization": request.specialization,
            "experience_level": request.experience_level,
            "key_requirements": request.key_requirements,
            "tone": request.tone
        }
        
        # Генерируем предложение
        result = openai_service.generate_proposal(project_data)
        
        # Сохраняем предложение в базу данных
        proposal = ProposalModel(
            user_id=current_user.id,
            project_description=request.project_description,
            budget_range=request.budget_range,
            specialization=request.specialization,
            experience_level=request.experience_level,
            key_requirements=request.key_requirements,
            generated_content=result["content"],
            tone=request.tone,
            tokens_used=result["tokens_used"],
            generation_time=result["generation_time"]
        )
        
        db.add(proposal)
        db.commit()
        db.refresh(proposal)
        
        return ProposalGenerationResponse(
            content=result["content"],
            tokens_used=result["tokens_used"],
            generation_time=result["generation_time"],
            model=result["model"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации предложения: {str(e)}"
        )

@router.post("/generate-multiple", response_model=MultipleProposalsResponse)
def generate_multiple_proposals(
    request: ProposalGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Генерирует несколько вариантов предложений"""
    
    try:
        # Инициализируем OpenAI сервис
        openai_service = OpenAIService()
        
        # Подготавливаем данные для генерации
        project_data = {
            "project_description": request.project_description,
            "budget_range": request.budget_range,
            "specialization": request.specialization,
            "experience_level": request.experience_level,
            "key_requirements": request.key_requirements,
            "tone": request.tone
        }
        
        # Генерируем несколько предложений
        results = openai_service.generate_multiple_proposals(project_data, count=3)
        
        # Сохраняем все предложения в базу данных
        saved_proposals = []
        for result in results:
            proposal = ProposalModel(
                user_id=current_user.id,
                project_description=request.project_description,
                budget_range=request.budget_range,
                specialization=request.specialization,
                experience_level=request.experience_level,
                key_requirements=request.key_requirements,
                generated_content=result["content"],
                tone=result.get("tone", request.tone),
                tokens_used=result["tokens_used"],
                generation_time=result["generation_time"]
            )
            db.add(proposal)
            saved_proposals.append(proposal)
        
        db.commit()
        
        # Возвращаем результаты
        proposals_response = []
        for result in results:
            proposals_response.append(ProposalGenerationResponse(
                content=result["content"],
                tokens_used=result["tokens_used"],
                generation_time=result["generation_time"],
                model=result["model"]
            ))
        
        return MultipleProposalsResponse(proposals=proposals_response)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации предложений: {str(e)}"
        )

@router.get("/", response_model=List[Proposal])
def get_user_proposals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Получает список предложений пользователя"""
    
    proposals = db.query(ProposalModel).filter(
        ProposalModel.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return proposals

@router.get("/{proposal_id}", response_model=Proposal)
def get_proposal(
    proposal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получает конкретное предложение пользователя"""
    
    proposal = db.query(ProposalModel).filter(
        ProposalModel.id == proposal_id,
        ProposalModel.user_id == current_user.id
    ).first()
    
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Предложение не найдено"
        )
    
    return proposal

@router.delete("/{proposal_id}")
def delete_proposal(
    proposal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удаляет предложение пользователя"""
    
    proposal = db.query(ProposalModel).filter(
        ProposalModel.id == proposal_id,
        ProposalModel.user_id == current_user.id
    ).first()
    
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Предложение не найдено"
        )
    
    db.delete(proposal)
    db.commit()
    
    return {"message": "Предложение успешно удалено"} 