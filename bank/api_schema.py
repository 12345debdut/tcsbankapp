from bank import ma
from bank.models import Customer
class CustomerSchema(ma.Schema):
    class Meta:
        fields=('customer_id','SSH_id','active','message','last_updated')
        # model=Customer

customer_schema=CustomerSchema()