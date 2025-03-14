import random
from datetime import datetime, timedelta
import math
import matplotlib.pyplot as plt
from classes.image import Image
from classes.request import Request
from classes.link import Link

def compute_image_scores(images: list[Image], requests: list[Request], links: list[Link], request_weight: float = 0.5, link_weight: float = 0.75) -> tuple[list[Image], list[tuple[datetime, float]]]:
    now = datetime.now()
    image_scores = []
    score_history = []

    # Calculate scores for each image
    for image in images:
        score = 0.0
        timestamps = []

        # Calculate request scores
        for request in requests:
            if request.img_id == image.id:
                request_score = math.pow(1.05, (0 - (now - request.created_at).total_seconds() / (60 * 60 * 24)))
                score += request_weight * request_score
                timestamps.append((request.created_at, score))

        # Calculate link scores
        for link in links:
            if link.image_id == image.id:
                link_score = math.pow(1.05, (0 - (now - link.created_at).total_seconds() / (60 * 60 * 24)))
                score += link_weight * link_score
                timestamps.append((link.created_at, score))

        # Apply randomness to the score
        if score == 0.0:
            score = float(random.randint(0, 15)) / 100000.0
        else:
            score *= float(100.0 - random.randint(-10, 10)) / 100.0
        
        image_scores.append((image, score))

        # Add timestamps for the last 30 days
        for days_ago in range(30):
            past_date = now - timedelta(days=days_ago)
            if timestamps:
                # Use the latest score for the past date
                latest_score = max([s[1] for s in timestamps if s[0] <= past_date], default=0)
                score_history.append((past_date, latest_score))

    # Sort images based on scores in descending order
    sorted_images = sorted(image_scores, key=lambda x: x[1], reverse=True)

    # Extract sorted images from the tuples
    return [img for img, score in sorted_images], score_history

def plot_image_scores(score_history: list[tuple[datetime, float]], output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))

    timestamps, scores = zip(*score_history)
    ax.plot(timestamps, scores, marker='o', label="Image Scores Over Time")

    ax.set_xlabel("Datetime")
    ax.set_ylabel("Score")
    ax.set_title("Image Scores Over Time")
    ax.legend()
    plt.savefig(output_path)

def test_recommend(images: list[Image], requests: list[Request], links: list[Link]):
    # Test with different datasets
    test_cases = [
        (0, 0, 0, None),  # Test case 1: 0 images, 0 requests, 0 links, expected_image
    ]
    
    for i, test_case in enumerate(test_cases):
        num_images, num_requests, num_links, expected_highly_recommended_image = test_case
        sorted_images, score_history = compute_image_scores(images[:num_images], requests[:num_requests], links[:num_links])
        plot_image_scores(score_history, f"outputs/test_{i}.png")

def main() -> None:
    images = [
        Image(1, "high_res_1.jpg", "low_res_1.jpg", "metadata_1", datetime(2024, 10, 21, 10, 0, 0)),
        Image(2, "high_res_2.jpg", "low_res_2.jpg", "metadata_2", datetime(2024, 10, 21, 10, 11, 0)),
        Image(3, "high_res_3.jpg", "low_res_3.jpg", "metadata_3", datetime(2024, 10, 30, 4, 8, 3)),
        Image(4, "high_res_4.jpg", "low_res_4.jpg", "metadata_4", datetime(2024, 10, 30, 12, 30, 0)),
        Image(5, "high_res_5.jpg", "low_res_5.jpg", "metadata_5", datetime(2024, 11, 15, 10, 5, 0)),
        Image(6, "high_res_6.jpg", "low_res_6.jpg", "metadata_6", datetime(2024, 12, 5, 3, 45, 0))
    ]
    requests = [
        Request(1, 1, 1, "reason_1 for image_1", 1, datetime(2024, 10, 21, 17, 37, 0)),
        Request(2, 2, 1, "reason_2 for image_1", 1, datetime(2024, 10, 21, 19, 55, 0)),
        Request(3, 3, 3, "reason_3 for image_3", 1, datetime(2024, 10, 30, 15, 19, 36)),
        Request(4, 4, 2, "reason_4 for image_2", 1, datetime(2024, 10, 25, 17, 31, 55)),
        Request(5, 5, 2, "reason_5 for image_2", 1, datetime(2024, 10, 28, 3, 22, 8)),
        Request(6, 6, 2, "reason_6 for image_2", 1, datetime(2024, 10, 28, 10, 19, 12))
    ]
    links = [
        Link(1, 1, "key_1 for image_1", 5, datetime(2024, 10, 21, 22, 17, 0)),
        Link(2, 3, "key_2 for image_3", 5, datetime(2024, 11, 3, 6, 41, 0)),
        Link(3, 1, "key_3 for image_1", 4, datetime(2024, 10, 22, 18, 33, 8)),
        Link(4, 1, "key_4 for image_1", 3, datetime(2024, 10, 29, 21, 44, 20)),
        Link(5, 1, "key_5 for image_1", 2, datetime(2024, 10, 30, 11, 19, 5)),
        Link(6, 2, "key_6 for image_2", 5, datetime(2024, 11, 3, 17, 4, 5)),
    ]

    test_recommend(images, requests, links)

    #sorted_images, score_history = compute_image_scores(images, requests, links)
    #for image in sorted_images:
    #    print(image.id, end="\t")

    #plot_image_scores(score_history, "outputs/all_images_scores.png")

if __name__ == "__main__":
    main()
    print()
