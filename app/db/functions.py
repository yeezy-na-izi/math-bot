from tortoise.exceptions import DoesNotExist

from app.db import models


class User(models.User):
    def __str__(self):
        return f"{self.id}) {self.telegram_id}"

    @classmethod
    async def is_registered(cls, telegram_id: int) -> [models.User, bool]:
        try:
            return await cls.get(telegram_id=telegram_id)
        except DoesNotExist:
            return False

    @classmethod
    async def register(cls, telegram_id) -> [models.User, bool]:
        await User(telegram_id=telegram_id).save()

    @classmethod
    async def get_count(cls) -> int:
        return await cls.all().count()


class LogRecord(models.LogRecord):
    @classmethod
    async def add(cls, user: models.User, command: str, info: dict = None, fail: bool = False) -> models.LogRecord:
        log_record = await cls(user=user, command=command, info=info, fail=fail)
        await log_record.save()
        return log_record

    @classmethod
    async def get_count(cls) -> int:
        return await cls.all().count()

    @classmethod
    async def get_count_by_fail(cls, fail: bool) -> int:
        return await cls.filter(fail=fail).count()

    @classmethod
    async def get_fails_records(cls) -> list:
        return await cls.filter(fail=True).all()
