import os
import asyncio

from reaction.rpc import RabbitRPC
from typing import List

from det2.det2 import Det2

rpc_batch_size = int(os.environ.get('RPC_BATCH_SIZE'))
assert rpc_batch_size > 0

class rpc(RabbitRPC):
    # Confirmed to work on fresh RabbitMQ install on Fedora
    URL = 'amqp://guest:guest@rabbitmq:5672'  

class MyModel:
    def __init__(self):
        self.model = Det2(
            bgr=False, 
            weights= "det2/weights/faster-rcnn/faster_rcnn_R_50_FPN_3x/model_final_280758.pkl",
            config= "det2/configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml",
            classes_path= 'det2/configs/coco80.names',
            thresh=0.5,
            )

    # https://github.com/catalyst-team/reaction/blob/master/reaction/rpc/rabbitmq.py
    @rpc(batch_size=rpc_batch_size, wait_for_batch=True, pool_size=1)
    # @rpc()
    def infer(self, *images):
        res = self.model.detect_get_box_in(images, box_format='ltrb')
        res = [ str(r) for r in res ]
        print(f'#### RESULT: {res}', flush=True)
        return res
     
if __name__ == '__main__':
    m = MyModel()
    #m.load()

    loop = asyncio.get_event_loop()
    loop.create_task(m.infer.consume())
    loop.run_forever()
