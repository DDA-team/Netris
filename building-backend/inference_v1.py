from ultralytics import YOLO
import cv2
import os
import time
import scipy.spatial.distance as dist
import json
import datetime
import numpy as np
import random
import uuid


class Pipeline:
    def __init__(self, weight, conf=0.5) -> None:
        self.weight = weight
        self.model = self.load_model()
        self.conf = conf
        self.num_warmup = 10
        self.offset = 1
        self.num_last_frames = 2
        self.step_frame = 3
        self.color_dict = {}
        self.names = None
        for id in range(4):
            self.color_dict[id] = (
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                np.random.randint(0, 255),
            )

    def load_model(self):
        model = YOLO(self.weight)
        return model

    def create_video(self, cap, out_file="out.mp4"):
        # создание видеофайла для записи
        width = int(cap.get(3))  # float `width`
        height = int(cap.get(4))  # float `height`
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps_source = cap.get(cv2.CAP_PROP_FPS)
        Frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_size = (width, height)
        vid = cv2.VideoWriter(
            out_file, fourcc, fps_source / self.step_frame, video_size
        )
        return vid, fps_source, video_size, Frames

    def postprocessing_res(
        self, results, centr_dict: dict, id_list_frame: list, classes_id: dict
    ):
        # обработка результатов
        # добавление координат центров
        # и обнаруженных id на текущем кадре
        bboxes_frame = []
        for res in results:
            for data in res.boxes.data.tolist():
                if self.names is None:
                    self.names = results[0].names
                if len(data) == 7:
                    x1, y1, x2, y2, id, confidence, class_id = data
                else:
                    x1, y1, x2, y2, confidence, class_id = data
                    id = None
                if id:
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    centr_dict[id] = (int(center_x), int(center_y))
                    id_list_frame.append(int(id))
                    class_name = results[0].names[int(class_id)]

                    classes_id[id] = class_name
                bboxes_frame.append([x1, y1, x2, y2, id, class_id])
        return bboxes_frame

    def chek_status(self, id, distance, id_time_dict: dict, status_dict: dict):
        if id not in id_time_dict.keys():
            id_time_dict[id] = {
                "active": 0,
                "passive": 0,
            }
        if distance > self.offset:
            status_dict[id] = "a"
            id_time_dict[id]["active"] += self.step_frame
        else:
            status_dict[id] = "p"
            id_time_dict[id]["passive"] += self.step_frame

    def crop_end(self, fn=None):  # функция для обрезки расширения файла
        return fn[: fn.rfind(".")]

    def visulize(self, bboxes_frame, frame, centr_dict, id_time_dict):
        def draw_bboxes(img, bbox, color):
            x1, y1 = bbox[:2]
            x2, y2 = bbox[2:4]
            img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)
            return img

        def draw_text(img, label, box, color):
            # draw text
            box = [int(i) for i in box]
            x0, y0, x1, y1 = box
            font_face = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 1
            font_thickness = 2
            text_w, text_h = cv2.getTextSize(
                label, font_face, font_scale, font_thickness
            )[0]
            text_color = (255, 255, 255)
            text_pt = (x0, y0 - 3)
            rec_pt = (x0, y0), (x0 + text_w, y0 - text_h - 4)

            cv2.rectangle(img, rec_pt[0], rec_pt[1], color, -1)
            cv2.putText(
                img,
                label,
                text_pt,
                font_face,
                font_scale,
                text_color,
                font_thickness,
                cv2.LINE_AA,
            )
            return img

        for data in bboxes_frame:
            x1, y1, x2, y2, id, class_id = data
            color = self.color_dict[class_id]
            bbox = [x1, y1, x2, y2]
            class_name = self.names[class_id]
            label = f"{id} ({class_name})"
            if id:
                frame = draw_bboxes(frame, bbox, color)
                frame = draw_text(frame, label, bbox, color)
                cv2.circle(
                    frame,
                    centr_dict[id],
                    1,
                    [0, 255, 0],
                    6,
                )
                if id not in id_time_dict.keys():
                    time_a = 0
                else:
                    time_a = round(id_time_dict[id]["active"] / self.fps_source, 2)
                cv2.putText(
                    frame,
                    f"{time_a}s",
                    ((int(x1), int(y2))),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    [255, 255, 255],
                    2,
                )
        return frame

    def inference(self, video_path, outpath, show=True, show_fps=True):
        # начальные значения
        i = 0

        pure_inf_time = 0
        ids_last_frames = []
        ids_reap = {}
        centers_last_frames = []
        id_time_dict = {}
        result_json = {}
        classes_id = {}
        seed = uuid.uuid4()
        os.makedirs(f"temp/{seed}", exist_ok=True)
        out_name = os.path.basename(video_path)
        # чтение видео
        cap = cv2.VideoCapture(video_path)

        vid, fps_source, shape, Frames = self.create_video(cap, out_file=outpath)
        proc_frame_keys = [i for i in range(self.step_frame, Frames, self.step_frame)]
        save_frame_keys = random.choices(proc_frame_keys, k=5)
        print(save_frame_keys)
        self.fps_source = fps_source

        # Цикл обработки кадров видео
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()
            if success:
                # time
                start_time = time.perf_counter()
                # центры, статус, id
                centr_dict = {}
                status_dict = {}
                id_list_frame = []

                if i % self.step_frame == 0:
                    # Run YOLOv8 inference on the frame
                    try:
                        results = self.model.track(
                            frame,
                            stream=False,
                            persist=True,
                            conf=self.conf,
                        )
                    except Exception as er:
                        # skip frame
                        print(f"Error frame: {er}")
                        raise Exception("Model error")
                    bboxes_frame = self.postprocessing_res(
                        results, centr_dict, id_list_frame, classes_id
                    )
                    # добавление истории id
                    if len(ids_last_frames) < self.num_last_frames:
                        ids_last_frames.append(id_list_frame)
                    else:
                        ids_last_frames.pop(0)
                        ids_last_frames.append(id_list_frame)
                    # добавление истории центров
                    if len(centers_last_frames) < self.num_last_frames:
                        centers_last_frames.append(centr_dict)
                    else:
                        centers_last_frames.pop(0)
                        centers_last_frames.append(centr_dict)
                    # Visualize the results on the frame
                    if show:
                        annotated_frame = self.visulize(
                            bboxes_frame, frame, centr_dict, id_time_dict
                        )
                        if i in save_frame_keys:
                            cv2.imwrite(f"temp/{seed}/{i}.jpg", annotated_frame)
                        # annotated_frame = results[0].plot()

                    # цикл обработки состояний
                    if len(ids_last_frames) >= self.num_last_frames:
                        for id in ids_last_frames[0]:
                            if id not in ids_reap.keys():
                                ids_reap[id] = 1
                            id_event = f"{id}{ids_reap[id]}"
                            if id_event not in result_json.keys():
                                result_json[id_event] = {
                                    "id": id,
                                    "class": classes_id[id],
                                    "start_time": str(
                                        datetime.timedelta(seconds=(i / fps_source))
                                    ),
                                    "end_time": str(
                                        datetime.timedelta(
                                            seconds=(Frames / fps_source)
                                        )
                                    ),
                                }
                            else:
                                if id not in ids_last_frames[-1]:
                                    result_json[id_event]["end_time"] = str(
                                        datetime.timedelta(seconds=(i / fps_source))
                                    )
                                    ids_reap[id] += 1
                            if id in ids_last_frames[-1]:
                                # рассчет расстояния
                                distance = dist.euclidean(
                                    centers_last_frames[0][id],
                                    centers_last_frames[-1][id],
                                )
                                # определение статуса и подсчет его времени
                                self.chek_status(
                                    id, distance, id_time_dict, status_dict
                                )
                    if show:
                        visual = annotated_frame
                    else:
                        visual = frame
                    if show_fps:
                        elapsed = time.perf_counter() - start_time
                        if i >= self.num_warmup:
                            pure_inf_time += elapsed
                            if (i + 1) % 1 == 0:
                                fps = (i + 1 - self.num_warmup) / pure_inf_time
                                cv2.putText(
                                    visual,
                                    f"fps: {fps:.2f}",
                                    (0, shape[1] - 10),
                                    cv2.FONT_HERSHEY_DUPLEX,
                                    1,
                                    [0, 255, 0],
                                    2,
                                )
                    # Display the annotated frame
                    vid.write((visual))
                    # cv2.namedWindow("YOLOv8 Inference", cv2.WINDOW_NORMAL)
                    # cv2.imshow("YOLOv8 Inference", visual)
                    # cv2.waitKey(0)
                # Break the loop if 'q' is pressed
                i += 1
                # if cv2.waitKey(1) & 0xFF == ord("q"):
                #     break
            else:
                # Break the loop if the end of the video is reached
                break
        cap.release()
        vid.release()
        # cv2.destroyAllWindows()
        with open(f"temp/{self.crop_end(out_name)}_timestamp.json", "w") as file:
            json.dump(result_json, file)
        for id in id_time_dict.keys():
            id_time_dict[id]["active"] = str(
                datetime.timedelta(seconds=(id_time_dict[id]["active"] / fps_source))
            )
            id_time_dict[id]["passive"] = str(
                datetime.timedelta(seconds=(id_time_dict[id]["passive"] / fps_source))
            )
        with open(f"temp/{self.crop_end(out_name)}_activite.json", "w") as file2:
            json.dump(id_time_dict, file2)
        return (
            f"temp/{self.crop_end(out_name)}_timestamp.json",
            f"temp/{self.crop_end(out_name)}_activite.json",
            seed,
        )


if __name__ == "__main__":
    pipe = Pipeline("./netris_8s(1280).pt", conf=0.25)
    video_path = "../data/v3.mp4.mp4"
    # video_path = "./data/test.mp4"
    pipe.inference(video_path, show=True, show_fps=True)
    # pipe.inference(video_path, show=True, show_fps=True)
    # pipe.inference(video_path, show=True, show_fps=True)
