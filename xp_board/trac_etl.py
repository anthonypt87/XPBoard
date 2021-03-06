from . import etl
from . import models
from . import user_etl
from . import trac_client


class TicketExtractor(etl.Extractor):

    def extract(self, trac_id):
        return trac_client.client.get_ticket(trac_id)


class UserTransformer(etl.Transformer):

    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def transform(self, ticket):
        return user_etl.UserETL.execute_one(
        	getattr(ticket, self.attribute_name)
        )


class PriorityTransformer(etl.Transformer):

    @classmethod
    def transform(cls, ticket):
        return int(ticket.priority[0])


class TicketETL(etl.ETL):

    extractor = TicketExtractor()

    transformers = {
        'id': 'trac_id',
        'reporter': UserTransformer('reporter'),
        'owner': UserTransformer('owner'),
        'status': None,
        'resolution': None,
        'summary': None,
        'priority': PriorityTransformer,
        'component': None
    }

    loader = etl.ModelLoader(models.Ticket)
