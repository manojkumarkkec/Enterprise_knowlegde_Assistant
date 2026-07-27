from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.models.permissions import Permission
from app.auth.models.role import Role


ROLES = [
    {
        "name": "admin",
        "description": "Administrator with full access",
    },
    {
        "name": "analyst",
        "description": "Can analyze documents",
    },
    {
        "name": "viewer",
        "description": "Read-only access",
    },
]

PERMISSIONS = [
    {
        "name": "user:create",
        "description": "Create users",
    },
    {
        "name": "user:delete",
        "description": "Delete users",
    },
    {
        "name": "document:read",
        "description": "Read documents",
    },
    {
        "name": "document:create",
        "description": "Create documents",
    },
    {
        "name": "document:delete",
        "description": "Delete documents",
    },
]


async def assign_permissions(
    role: Role,
    permissions_to_assign: list[Permission],
) -> None:
    """
    Assign permissions without creating duplicates.
    """

    existing_permissions = {
        permission.name
        for permission in role.permissions
    }

    for permission in permissions_to_assign:
        if permission.name not in existing_permissions:
            role.permissions.append(permission)


async def seed_rbac(
    session: AsyncSession,
) -> None:

    permissions: dict[str, Permission] = {}
    roles: dict[str, Role] = {}

    # -----------------------------
    # Create Permissions
    # -----------------------------
    for permission_data in PERMISSIONS:

        result = await session.execute(
            select(Permission).where(
                Permission.name == permission_data["name"]
            )
        )

        permission = result.scalar_one_or_none()

        if permission is None:
            permission = Permission(**permission_data)
            session.add(permission)
            await session.flush()

        permissions[permission.name] = permission

    # -----------------------------
    # Create Roles
    # -----------------------------
    for role_data in ROLES:

        result = await session.execute(
            select(Role)
            .options(
                selectinload(Role.permissions)
            )
            .where(
                Role.name == role_data["name"]
            )
        )

        role = result.scalar_one_or_none()

        if role is None:
            role = Role(**role_data)
            session.add(role)

            # Flush so role gets its UUID
            await session.flush()

            # Refresh so relationship collection exists
            await session.refresh(
                role,
                attribute_names=["permissions"],
            )

        roles[role.name] = role

    # -----------------------------
    # Admin Permissions
    # -----------------------------
    await assign_permissions(
        roles["admin"],
        [
            permissions["user:create"],
            permissions["user:delete"],
            permissions["document:read"],
            permissions["document:create"],
            permissions["document:delete"],
        ],
    )

    # -----------------------------
    # Analyst Permissions
    # -----------------------------
    await assign_permissions(
        roles["analyst"],
        [
            permissions["document:read"],
            permissions["document:create"],
        ],
    )

    # -----------------------------
    # Viewer Permissions
    # -----------------------------
    await assign_permissions(
        roles["viewer"],
        [
            permissions["document:read"],
        ],
    )

    await session.commit()

    print("RBAC seed completed successfully.")