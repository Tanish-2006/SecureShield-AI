from fastapi import HTTPException

from database.models.project import Project


def create_project(
    db,
    name,
    description,
    owner_id
):
    project = Project(
        name=name,
        description=description,
        owner_id=owner_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects_by_user(
    db,
    owner_id
):
    return db.query(Project).filter(
        Project.owner_id == owner_id
    ).all()


def get_project_by_id(
    db,
    project_id
):
    return db.query(Project).filter(
        Project.id == project_id
    ).first()


def get_user_project_or_404(
    db,
    project_id,
    user_id
):
    project = get_project_by_id(
        db,
        project_id
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return project
