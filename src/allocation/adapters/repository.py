import abc

from allocation.adapters import orm
from allocation.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, sku) -> model.Product:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_batchref(self, batchref) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    async def add(self, product):
        self.session.add(product)

    async def get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()

    async def get_by_batchref(self, batchref):
        return (
            self.session.query(model.Product)
            .join(model.Batch)
            .filter(
                orm.batches.c.reference == batchref,
            )
            .first()
        )
