import bcrypt

print(bcrypt.hashpw("1234".encode(), salt=bcrypt.gensalt()))
import asyncio
from typing import Optional

from db.models import Product


# async def test():
    # await Product.create(name="Laptop", price=10000)
    # await Product.create(name="To'p", price=10000)
    # p:list[Optional['Product']]  = list(await Product.get_by_name("x"))
    # if p:
    #     for i in p:
    #         print(i.name)
    # else:
    #     print("Not FOund")

    # await Product.delete(2)
#     await Product.update(2 , name = 'Komp')
#
# asyncio.run(test())