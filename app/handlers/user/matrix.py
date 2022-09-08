from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import Config
from app.states import MatrixStates
from app.utils.matrix import Matrix, SizesMatchError, SquareMatrixRequired, NonInvertibleMatrix

router = Router()


async def matrix_input(message: Message, config: Config):
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
async def det_handler(message: Message, state: FSMContext, bot: Bot):
    # set state for determinant and send mess
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
    # set state for determinant and send mess
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


@router.message(Command(commands=["inv"]))
async def inv_handler(message: Message, state: FSMContext):
    # set state for determinant and send mess
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
        await message.answer(
            "Невозможно рассчитать обратную матрицу для данной матрицы!\n"
            "Попробуйте еще раз."
        )
        return

    text = (
        f"<b>Для матрицы:</b>\n"
        f"{matrix}\n\n"
        f"Обратная матрица:\n"
        f"<code>{str(result)}</code>"
    )
    await message.answer(text)


