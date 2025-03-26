import random
from datetime import datetime, timedelta
import math
import matplotlib.pyplot as plt
from classes.image import Image
from classes.request import Request
from classes.link import Link

def apply_randomness(score: float):
    if score == 0.0:
        score = float(random.randint(0, 15)) / 100000.0
    else:
        score *= float(100.0 - random.randint(-10, 10)) / 100.0
    return score

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
            if request.image_id == image.id:
                request_score = math.pow(1.05, (0 - (now - request.created_at).total_seconds() / (60 * 60 * 24)))
                new_score = request_weight * request_score
                timestamps.append((request.created_at, new_score))

                # Apply randomness to the score
                new_score = apply_randomness(new_score)
                score += new_score
                # Append to score hisory
                score_history.append((request.created_at, score))

        # Calculate link scores
        for link in links:
            if link.image_id == image.id:
                link_score = math.pow(1.05, (0 - (now - link.created_at).total_seconds() / (60 * 60 * 24)))
                new_score = link_weight * link_score
                timestamps.append((link.created_at, new_score))
                # Apply randomness to the score
                new_score = apply_randomness(new_score)

                score += new_score
        
                # Append to score hisory
                score_history.append((link.created_at, score))
        
        image_scores.append((image, score))

        """
        # Add timestamps for the last 30 days
        for days_ago in range(30):
            past_date = now - timedelta(days=days_ago)
            if timestamps:
                # Use the latest score for the past date
                latest_score = max([s[1] for s in timestamps if s[0] <= past_date], default=0)
                score_history.append((past_date, latest_score))
        """


    # Sort images based on scores in descending order
    sorted_image_id_score_list = sorted(image_scores, key=lambda x: x[1], reverse=True)


    # Extract sorted images from the tuples
    return sorted_image_id_score_list, score_history

def compute_image_rating(images: list[Image], requests: list[Request], links: list[Link], request_weight: float = 0.5, link_weight: float = 0.75):
    images_realtime_scores: list[tuple[Image, list[tuple[datetime, float]]]] = list()

    for image in images:
        image_realtime_scores: list[tuple[datetime, float]] = list()
        # Calculate request scores
        for request in requests:
            if request.image_id == image.id:
                new_score = request_weight
                # Apply randomness to the score
                new_score = apply_randomness(new_score)

                # Append new score into image_realtime_scores
                image_realtime_scores.append((request.created_at, new_score))

        for link in links:
            if link.image_id == image.id:
                new_score = request_weight
                # Apply randomness to the score
                new_score = apply_randomness(new_score)

                # Append new score into image_realtime_scores
                image_realtime_scores.append((link.created_at, new_score))


        # Sort images_realtime_scores in datetime ascending order
        sorted_image_realtime_scores: list[tuple[datetime, float]] = sorted(image_realtime_scores, key=lambda readltime_score: readltime_score[1], reverse=True)
        images_realtime_scores.append((image, sorted_image_realtime_scores))
    
    #for image, image_realtime_scores in images_realtime_scores:
    #    print(image.id, [score for _, score in image_realtime_scores])
    
    return images_realtime_scores

def plot_image_scores(score_history: list[tuple[datetime, float]], output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))

    if score_history:
        timestamps, scores = zip(*score_history)
        ax.plot(timestamps, scores, marker='o', label="Image Scores Over Time")
    else:
        ax.set_title("No Data Available")
        ax.set_xlabel("Datetime")
        ax.set_ylabel("Score")
        ax.text(0.5, 0.5, "No scores to display", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    ax.set_xlabel("Datetime")
    ax.set_ylabel("Score")
    ax.set_title("Image Scores Over Time")
    #ax.legend()
    plt.savefig(output_path)

def test_recommend(images: list[Image], requests: list[Request], links: list[Link]):
    # Test with different datasets
    test_cases = [
        (0, 0, 0, [None]),  # Test case 0: 0 images, 0 requests, 0 links, expected_image None 2024 10 30
        (1, 0, 0, [1]),  # Test case 1: 1 images, 0 requests, 0 links, expected_image image.id = 1 2024 11 15
        (2, 0, 0, [1, 2]),  # Test case 2: 2 images, 0 requests, 0 links, expected_image image.id = 1, 2 2024 11 30
        (4, 0, 0, [1, 2, 3, 4]),  # Test case 3: 4 images, 0 requests, 0 links, expected_image image.id = 1, 2, 3, 4 2024 12 15
        (5, 0, 0, [1, 2, 3, 4, 5]),  # Test case 4: 5 images, 0 requests, 0 links, expected_image image.id = 1, 2, 3, 4, 5 2024 12 30
        (5, 0, 0, [1, 2, 3, 4, 5]),  # Test case 5: 5 images, 0 requests, 0 links, expected_image image.id = 1, 2, 3, 4, 5 2025 01 15
        (5, 0, 0, [1, 2, 3, 4, 5]),  # Test case 6: 5 images, 0 requests, 0 links, expected_image image.id = 1, 2, 3, 4, 5 2025 01 30
        (5, 2, 3, [1, 2, 3, 9]),  # Test case 7: 5 images, 2 requests, 3 links, expected_image image.id = 1, 2, 3, 9 2025 02 15
        
        (5, 2, 3, [1, 2, 3]),  # Test case 8: 5 images, 2 requests, 3 links, expected_image image.id = 1, 2, 3 2025 02 30
        (9, 2, 6, [1, 2, 9]),  # Test case 9: 9 images, 2 requests, 6 links, expected_image image.id = 1, 2, 9 2025 03 15
        (9, 2, 6, [1, 2, 9]),  # Test case 10: 9 images, 2 requests, 6 links, expected_image image.id = 1, 2, 9 2025 03 30 
    ]
    
    for i, test_case in enumerate(test_cases):
        num_images, num_requests, num_links, expected_highly_recommended_image_ids = test_case
        images_realtime_scores = compute_image_rating(images[:num_images], requests[:num_requests], links[:num_links])
        
        
        for image, image_realtime_scores in images_realtime_scores:
            cumulative_score: float = 0.0
            realtime_cumulative_scores = list()
            if len(image_realtime_scores) > 0:
                latest_datetime = image_realtime_scores[-1][0]
                for datetime, score in image_realtime_scores:
                    cumulative_score += score * math.pow(1.05, (0 - (latest_datetime - datetime).total_seconds() / (60 * 60 * 24)))
                    realtime_cumulative_scores.append((datetime, cumulative_score))

            plot_image_scores(realtime_cumulative_scores, f"outputs/test_{i}.png")
            #print(image.id, [score for _, score in image_realtime_scores])
        """
        sorted_image_score_list, score_history = compute_image_scores(images[:num_images], requests[:num_requests], links[:num_links])
        
        #print(sorted_image_id_score_list)
        # Determine the highly recommended image
        highly_recommended_image_id = sorted_image_score_list[0][0].id if sorted_image_score_list else None
        highly_recommended_image_score = sorted_image_score_list[0][1] if sorted_image_score_list else None
        
        if i == 5:
            break
        
        plot_image_scores(score_history, f"outputs/test_{i}.png")
        print(f"Test {i}:", "Pass" if highly_recommended_image_id in expected_highly_recommended_image_ids else "Fail")
        print(f"\tHighly Recommended Image: image.id={highly_recommended_image_id}, image score={highly_recommended_image_score}\n")
        """

def main() -> None:
    images = [
        Image(1, 'DEEP2heat_cropped.jpg', 'DEEP2heat_cropped.jpg', '{}', datetime(2024, 11, 13, 7, 55, 25)),

        Image(2, 'Heat-wave.jpg', 'Heat-wave.jpg', '{}', datetime(2024, 11, 22, 15, 21, 33)),

        Image(3, 'MeerKAT_and_bubbles_composite.png', 'MeerKAT_and_bubbles_composite.png', '{}', datetime(2024, 12, 2, 17, 17, 4)),

        Image(4, 'MeerKATDeep2_compositeV6.jpg', 'MeerKATDeep2_compositeV6.jpg', '{}', datetime(2024, 12, 5, 22, 14, 45)),

        Image(5, 'n1316compositeGREENmasked.png', 'n1316compositeGREENmasked.png', '{}', datetime(2024, 12, 20, 16, 48, 43)),

        Image(6, 'hartebeesthoek.jpg', 'hartebeesthoek.jpg', '{}', datetime(2025, 3, 7, 13, 49, 11)),
        Image(7, 'Xgalaxy_composite.jpg', 'Xgalaxy_composite.jpg', '{}', datetime(2025, 3, 7, 13, 49, 49)),
        Image(8, 'radio bubbles.jpg', 'radio bubbles.jpg', '{}', datetime(2025, 3, 7, 13, 50, 26)),

        Image(9, 'sarao-evening-observation.jpg', 'sarao-evening-observation.jpg', '{}', datetime(2025, 3, 11, 8, 18, 5)),
    ]

    requests = [
        Request(1, 1, 1, 'We are researching the structure of the SARAO telescope as part of our AVNSTT graduate project.', 2, datetime(2025, 2, 5, 11, 54, 15)),
        Request(2, 1, 3, 'To make money from NFTs...', 0, datetime(2025, 2, 5, 12, 13, 51))
    ]

    links = [
        Link(1, 2, '61660859X1738757999246', 4, datetime(2025, 2, 5, 12, 19, 59)),

        Link(2, 2, '61i6065981739190925562', 5, datetime(2025, 2, 10, 12, 35, 25)),
        Link(3, 2, '61Q60f59E1739191189661', 5, datetime(2025, 2, 10, 12, 39, 49)),

        Link(4, 1, '61i60T59v1741696148246', 0, datetime(2025, 3, 11, 12, 29, 8)),
        Link(5, 2, '61260k59G1741696809326', 5, datetime(2025, 3, 11, 12, 40, 9)),
        Link(6, 9, '61k60e5941741700640423', 4, datetime(2025, 3, 11, 13, 44, 0)),
    ]

    test_recommend(images, requests, links)

if __name__ == "__main__":
    main()
