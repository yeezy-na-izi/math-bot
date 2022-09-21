from aiogram import Router


def get_user_router() -> Router:
    from . import info, start, matrix, numbers_theory, get_random_student

    router = Router()
    router.include_router(info.router)
    router.include_router(start.router)
    router.include_router(matrix.router)
    router.include_router(numbers_theory.router)
    router.include_router(get_random_student.router)

    return router
