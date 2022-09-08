from aiogram.fsm.state import State, StatesGroup


class MatrixStates(StatesGroup):
    send_matrix_for_determinant = State()
    send_matrix_for_ref = State()
    send_matrix_for_inv = State()