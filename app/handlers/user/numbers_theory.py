from io import StringIO

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import Config
from app.states import NumbersTheoryStates
from app.utils.logic import OPS, build_table

router = Router()
logic_ops_description = "\n".join([f"{op} {op_data[3]}" for op, op_data in OPS.items()])


@router.message(Command(commands=["logic"]))
async def logic_handler(message: Message, state: FSMContext):
    await message.answer(
        f'<u>Допустимые операторы:</u>\n{logic_ops_description}\n\n'
        'Введите логическое выражение:',
    )
    await state.set_state(NumbersTheoryStates.logic_equation_input)


@router.message(state=NumbersTheoryStates.logic_equation_input)
async def logic_equation_input(message: Message, state: FSMContext, config: Config):
    try:
        table, variables = build_table(message.text, config.math.max_vars)
        out = StringIO()
        print(*variables, 'F', file=out, sep=' ' * 2)
        for row in table:
            print(*row, file=out, sep=' ' * 2)
        answer = f'<code>{out.getvalue()}</code>'
        await message.answer(answer)
        await state.clear()
    except (AttributeError, SyntaxError):
        await message.answer(
            "Ошибка ввода данных!\n"
            "Попробуйте еще раз."
        )
    except ValueError:
        await message.answer(
            f"Ограничение по кол-ву переменных: {config.math.max_vars}\n"
            f"Попробуйте еще раз."
        )
