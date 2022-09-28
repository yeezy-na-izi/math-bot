from typing import Union

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import Config
from app.states import MatrixStates
from app.utils.matrix import Matrix, SizesMatchError, SquareMatrixRequired, NonInvertibleMatrix

router = Router()


async def matrix_input(message: Message, config: Config) -> Union[Matrix, None]:
    try:
        lst = [[float(x) for x in row.split()] for row in message.text.split('\n')]
        matrix = Matrix.from_list(lst)
    except SizesMatchError:
        await message.answer(
            'Несовпадение размеров строк или столбцов. Матрица должна быть <b>прямоугольной</b>.\n'
            'Попробуйте еще раз.',
        )
        return
    except ValueError:
        await message.answer(
            'Необходимо вводить <b>числовую</b> квадратную матрицу\n'
            'Попробуйте еще раз.',
        )
        return
    else:
        if matrix.n > config.math.max_matrix:
            await message.answer(
                f'Ввод матрицы имеет ограничение в {config.math.max_matrix}x{config.math.max_matrix}!\n'
                f'Попробуйте еще раз.',
            )
            return
    return matrix


@router.message(Command(commands=["det"]))
async def det_handler(message: Message, state: FSMContext):
    await message.answer("Введите матрицу для вычисления определителя")
    await state.set_state(MatrixStates.send_matrix_for_determinant)


@router.message(state=MatrixStates.send_matrix_for_determinant)
async def send_matrix_determinant(message: Message, state: FSMContext, config: Config):
    matrix = await matrix_input(message, config)
    if matrix is None:
        return

    try:
        result = str(matrix.det())
    except SquareMatrixRequired:
        await message.answer(
            "Невозможно рассчитать определитель для не квадратной матрицы!\n"
            "Попробуйте еще раз."
        )
        return

    text = (
        f"<b>Для матрицы:</b>\n"
        f"{matrix}\n\n"
        f"<b>Определитель матрицы:</b>\n"
        f"{result}"
    )
    await message.answer(text)
    await state.clear()


@router.message(Command(commands=["ref"]))
async def ref_handler(message: Message, state: FSMContext):
    await message.answer("Введите матрицу для представления матрицы в виде ступенчатой")
    await state.set_state(MatrixStates.send_matrix_for_ref)


@router.message(state=MatrixStates.send_matrix_for_ref)
async def send_matrix_ref(message: Message, state: FSMContext, config: Config):
    matrix = await matrix_input(message, config)
    if matrix is None:
        return

    result = matrix.ref()
    text = (
        f"<b>Для матрицы:</b>\n"
        f"{matrix}\n\n"
        f"Матрица в ступенчатом виде:\n"
        f"<code>{str(result)}</code>"
    )
    await message.answer(text)
    await state.clear()


@router.message(Command(commands=["inv"]))
async def inv_handler(message: Message, state: FSMContext):
    await message.answer("Введите матрицу для вычисления обратной матрицы")
    await state.set_state(MatrixStates.send_matrix_for_inv)


@router.message(state=MatrixStates.send_matrix_for_inv)
async def send_matrix_inv(message: Message, state: FSMContext, config: Config):
    matrix = await matrix_input(message, config)
    if matrix is None:
        return

    try:
        result = matrix.inverse()
    except NonInvertibleMatrix:
        text = "Невозможно рассчитать обратную матрицу для данной матрицы!"
    else:
        text = (
            f"<b>Для матрицы:</b>\n"
            f"{matrix}\n\n"
            f"Обратная матрица:\n"
            f"<code>{str(result)}</code>"
        )

    await message.answer(text)
    await state.clear()


@router.message(Command(commands=["mul"]))
async def mul_handler(message: Message, state: FSMContext):
    await message.answer("Введите первую матрицу для вычисления умножения матриц")
    await state.set_state(MatrixStates.send_first_matrix_for_mul)


@router.message(state=MatrixStates.send_first_matrix_for_mul)
async def send_first_matrix_mul(message: Message, state: FSMContext, config: Config):
    matrix = await matrix_input(message, config)
    if matrix is None:
        return

    await state.update_data(first_matrix=matrix)
    await message.answer("Введите вторую матрицу для вычисления умножения матриц")
    await state.set_state(MatrixStates.send_second_matrix_for_mul)


@router.message(state=MatrixStates.send_second_matrix_for_mul)
async def send_second_matrix_mul(message: Message, state: FSMContext, config: Config):
    matrix = await matrix_input(message, config)
    if matrix is None:
        return

    data = await state.get_data()
    first_matrix = data["first_matrix"]
    try:
        result = first_matrix * matrix
    except SizesMatchError:
        text = "Невозможно рассчитать произведение матриц с такими размерами!"
    else:
        text = (
            f"<b>Для матриц:</b>\n"
            f"{first_matrix}\n\n"
            f"{matrix}\n\n"
            f"Произведение матриц:\n"
            f"<code>{str(result)}</code>"
        )

    await message.answer(text)
    await state.clear()


@router.message(Command(commands=["slau"]))
async def slau_handler(message: Message, state: FSMContext):
    await message.answer("Введите матрицу для решения СЛАУ")
    await state.set_state(MatrixStates.send_matrix_for_slau)


@router.message(state=MatrixStates.send_matrix_for_slau)
async def send_matrix_slau(message: Message, state: FSMContext, config: Config):
    matrix = await matrix_input(message, config)
    if matrix is None:
        return
    try:
        matrix = matrix.inverse()
    except NonInvertibleMatrix:
        text = "Невозможно рассчитать обратную матрицу для данной матрицы!"
    else:
        text = "Введите вектор для решения СЛАУ"

    await state.update_data(matrix=matrix)
    await message.answer(text=text)
    await state.set_state(MatrixStates.send_vector_for_slau)


@router.message(state=MatrixStates.send_vector_for_slau)
async def send_vector_slau(message: Message, state: FSMContext, config: Config):
    vector = await matrix_input(message, config)
    if vector is None:
        return

    data = await state.get_data()
    matrix = data["matrix"]
    try:
        result = matrix * vector
    except SizesMatchError:
        text = "Невозможно рассчитать решение СЛАУ с такими размерами!"

    else:
        text = (
            f"<b>Для матрицы:</b>\n"
            f"{matrix}\n\n"
            f"и вектора:\n"
            f"{vector}\n\n"
            f"Решение СЛАУ:\n"
            f"<code>{str(result)}</code>"
        )

    await message.answer(text)
    await state.clear()
