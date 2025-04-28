from user_simulator.models import User

def sign_in():
    pass

def buy_product(product_id):
    pass

def scenario_1():
    sign_in()
    """
        db에서 존재하는 product_id를 랜덤으로 가져옴
        product_id = random.choice(Product.objects.values_list('id', flat=True))
    """
    sign_in()
    while True:
        buy_product(product_id)

