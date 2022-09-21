import random
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["get_random_student"]))
async def get_random_student_cmd(message: Message):
    students = [
        'Авдонина Ксения Сергеевна',
        'Андреев Дмитрий Сергеевич',
        'Анисимов Денис Андреевич',
        'Аракчеева Полина Алексеевна',
        'Аршинов Максим Андреевич',
        'Беляев Ярослав Русланович'
        'Воробьев Андрей Георгиевич',
        'Губкин Иван Сергеевич',
        'Деримедведь Анастасия Владимировна',
        'Забора Георгий Данилович',
        'Землянский Михаил Евгеньевич',
        'Качура Ульяна Валерьевна',
        'Кирданов Алексей Климович',
        'Коровушкин Николай Андреевич',
        'Костенко Алиса Владимировна',
        'Кочнов Игорь Олегович',
        'Кравченко Алёна Сергеевна',
        'Луценко Владимир Витальевич',
        'Лысенко Кирилл Александрович',
        'Мизюрин Степан Викторович',
        'Монжалей Ксения Дмитриевна',
        'Мурашка Ксения Максимовна',
        'Попов Григорий Алексеевич',
        'Пузанов Кирилл Константинович',
        'Ринчинов Вячеслав Баирович',
        'Сафронова Дарья Дмитриевна',
        'Томаровский Кирилл Сергеевич',
        'Тыщенко Андрей Владимирович',
        'Хованский Максим Дмитриевич',
        'Хохлов Кирилл Денисович',
        'Шальнев Сергей Юрьевич',
    ]
    await message.answer(random.choice(students))
