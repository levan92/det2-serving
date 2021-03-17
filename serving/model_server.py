import asyncio

from reaction.rpc import RabbitRPC
from typing import List

class rpc(RabbitRPC):
    # Confirmed to work on fresh RabbitMQ install on Fedora
    URL = 'amqp://guest:guest@rabbitmq:5672'  
     
class MyModel:
    # https://github.com/catalyst-team/reaction/blob/master/reaction/rpc/rabbitmq.py
    @rpc()
    #@rpc(batch_size=64, wait_for_batch=True, pool_size=1)
    def myfunction1(self, *batch) -> List[float]:
        print(f"Called with a batch_size of {len(batch)}")

        prediction_batch = []
        for i,b in enumerate(batch):
            prediction = [ e*e*(i+1) for e in range(5) ]
            prediction_batch.append( prediction )

        print(f"Returned batch_size of {len(prediction_batch)}")
        return prediction_batch
     
if __name__ == '__main__':
    m = MyModel()
    #m.load()

    loop = asyncio.get_event_loop()
    loop.create_task(m.myfunction1.consume())
    loop.run_forever()
