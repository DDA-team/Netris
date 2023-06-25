import asyncio
import time
from inference_v1 import Pipeline
from models import Item
from prestarted import Session


class Worker:
    def __init__(self, weights, conf):
        self.model = Pipeline(weights, conf=conf)

    def run_process(self):
        while True:
            session = Session()
            all_items = session.query(Item).filter_by(is_complete=False).all()
            session.close()
            for i in all_items:
                output_video_path = f"temp/{i.id}_res.mp4"
                try:
                    result = self.model.inference(i.input_video, output_video_path)
                    print(2)
                    session.query(Item).filter_by(id=i.id).update(
                        {
                            "is_complete": True,
                            "output_video": output_video_path,
                            "events": str(result[0]),
                            "downtime_events": str(result[1]),
                            "seed": str(result[2]),
                        }
                    )
                    session.commit()
                except Exception as er:
                    print("Model error:", er)
                    break
                session.close()
            time.sleep(5)


if __name__ == "__main__":
    while True:
        worker_instanse = Worker("best.pt", 0.25)
        worker_instanse.run_process()
