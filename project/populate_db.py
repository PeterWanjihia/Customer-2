from faker import Faker
from __init__ import create_app, db
from models import Client, CustomerTransaction
from random import random
from random import uniform
from datetime import datetime



fake = Faker()

def populate_data(num_customers):
    with app.app_context():
        for _ in range(num_customers):
            client = Client(
                name=fake.name(),
                email=fake.email(),
                address=fake.address(),
                contact_info=fake.phone_number()
            )
            
            existing_client = Client.query.filter_by(email=client.email).first()
            if existing_client is None:
                db.session.add(client)
                db.session.commit()

                for _ in range(fake.random_int(min=1, max=5)):
                    transaction = CustomerTransaction(
                        customer_id=client.id,
                        date=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
                        transNumber=fake.random_int(),
                        transAmount=round(uniform(0.0, 1000.0), 2)
                    )
                    db.session.add(transaction)
                    db.session.commit()



if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        populate_data(100)  # Example: Populate 100 customers
