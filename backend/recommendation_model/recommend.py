import random
from datetime import datetime, timedelta
import math
import matplotlib.pyplot as plt
from classes.image import Image
from backend.classes.request import Request
from backend.classes.link import Link

def recommend(images: list[Image], requests: list[Request], links: list[Link]) -> list[tuple[Image, list[tuple[datetime, float]]]]:
    image_timestamp_scores_score_list: list[tuple[Image, list[tuple[datetime, float]], float]] = []

    for image in images:
        timestamp_score_list: list[tuple[datetime, float]] = []
        score: float = random.randint(0, 10) / 100.0
        latest_datetime = None
        for request in requests:
            if latest_datetime is None: # Check if datetime has been assigned to latest_datetime
                latest_datetime = request.created_at
            elif latest_datetime < request.created_at:
                 latest_datetime = request.created_at # Updating latest datetime to latest created_at value

            if request.img_id == image.id:
                now_datetime = datetime.now() + timedelta(hours=2)
                delta_datetime: float = float(now_datetime.timestamp()) / float(request.created_at.timestamp())
                score += 0.2 * math.exp(0 - delta_datetime)
                timestamp_score_list.append((request.created_at, score))

        for link in links:
            if latest_datetime is None: # Check if datetime has been assigned to latest_datetime
                latest_datetime = link.created_at
            elif latest_datetime < link.created_at:
                 latest_datetime = link.created_at # Updating latest datetime to latest created_at value

            if link.image_id == image.id:
                now_datetime = datetime.now() + timedelta(hours=2)
                delta_datetime: float = float(now_datetime.timestamp()) / float(link.created_at.timestamp())
                score += 0.2 * 3 * math.exp(0 - delta_datetime)
                timestamp_score_list.append((link.created_at, score))

        if timestamp_score_list == []: # If list is empty append score of ZERO
            timestamp_score_list.append((latest_datetime, random.random() * 0.05))
        
        image_timestamp_scores_score_list.append((image, timestamp_score_list, score))

    image_timestamp_scores_score_list.sort(key=lambda x: x[2], reverse=True)
    return [(image, timestamp_scores_list) for image, timestamp_scores_list, _ in image_timestamp_scores_score_list]

def plot_image_scores(sorted_images: list[tuple[Image, list[tuple[datetime, float]]]]) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))

    for image, timestamp_score_list in sorted_images:
        if timestamp_score_list:
            timestamps, scores = zip(*timestamp_score_list)
            ax.plot(timestamps, scores, marker='o', label=f"Image {image.id} ({scores[-1]:.2f})")

    ax.set_xlabel("Datetime")
    ax.set_ylabel("Score")
    ax.set_title("Image Scores")
    ax.legend()
    plt.savefig("outputs/images_trend")

def test_recommend():
    images: list[Image] = [
        Image(1, "high_res_1.jpg", "low_res_1.jpg", "metadata_1", datetime(2024, 10, 21, 10, 0, 0)),
        Image(2, "high_res_2.jpg", "low_res_2.jpg", "metadata_2", datetime(2024, 10, 21, 10, 11, 0)),
        Image(3, "high_res_3.jpg", "low_res_3.jpg", "metadata_3", datetime(2024, 10, 30, 4, 8, 3)),
        Image(4, "high_res_4.jpg", "low_res_4.jpg", "metadata_4", datetime(2024, 10, 30, 12, 30, 0)),
        Image(5, "high_res_5.jpg", "low_res_5.jpg", "metadata_5", datetime(2024, 11, 15, 10, 5, 0)),
        Image(6, "high_res_6.jpg", "low_res_6.jpg", "metadata_6", datetime(2024, 12, 5, 3, 45, 0))
    ]
    requests: list[Request] = [
        Request(1, 1, 1, "reason_1 for image_1", 1, datetime(2024, 10, 21, 17, 37, 0)),
        Request(2, 2, 1, "reason_2 for imgage_1", 1, datetime(2024, 10, 21, 19, 55, 0)),
        Request(3, 3, 3, "reason_3 for image_3", 1, datetime(2024, 10, 30, 15, 19, 36)),
        Request(4, 4, 2, "reason_4 for image_2", 1, datetime(2024, 10, 25, 17, 31, 55)),
        Request(5, 5, 2, "reason_5 for image_2", 1, datetime(2024, 10, 28, 3, 22, 8)),
        Request(6, 6, 2, "reason_6 for image_2", 1, datetime(2024, 10, 28, 10, 19, 12))
    ]
    links: list[Link] = [
        Link(1, 1, "key_1 for image_1", 5, datetime(2024, 10, 21, 22, 17, 0)),
        Link(2, 3, "key_2 for image_3", 5, datetime(2024, 11, 3, 6, 41, 0)),
        Link(3, 1, "key_3 for image_1", 4, datetime(2024, 10, 22, 18, 33, 8)),
        Link(4, 1, "key_4 for image_1", 3, datetime(2024, 10, 29, 21, 44, 20)),
        Link(5, 1, "key_5 for image_1", 2, datetime(2024, 10, 30, 11, 19, 5)),
        Link(6, 2, "key_6 for image_2", 5, datetime(2024, 11, 3, 17, 4, 5)),
    ]
    
    while images or requests or links:
        if images:
            oldest_image = images.pop(0)
            print(f"Popped oldest image: {oldest_image.id}, {oldest_image.timestamp}")
        elif requests:
            oldest_request = requests.pop(0)
            print(f"Popped oldest request: {oldest_request.id}, {oldest_request.timestamp}")
        elif links:
            oldest_link = links.pop(0)
            print(f"Popped oldest link: {oldest_link.id}, {oldest_link.timestamp}")

        sorted_images = recommend(images, requests, links)
        latest_timestamp = max([image.timestamp for image in sorted_images] + [request.timestamp for request in requests] + [link.timestamp for link in links])
        plot_image_scores(sorted_images)
        print(f"Latest timestamp: {latest_timestamp}")

test_recommend()
