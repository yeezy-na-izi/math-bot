from aiogram.fsm.state import State, StatesGroup


class MatrixStates(StatesGroup):
    send_vector_for_slau = State()
    send_matrix_for_slau = State()
    send_matrix_for_determinant = State()
    send_matrix_for_ref = State()
    send_matrix_for_inv = State()
    send_first_matrix_for_mul = State()
    send_second_matrix_for_mul = State()


class NumbersTheoryStates(StatesGroup):
    logic_equation_input = State()
    euclid_input = State()
    factorize_input = State()
    zn_idempotent_input = State()
    zn_nilpotent_input = State()
    zn_inverse_input = State()
