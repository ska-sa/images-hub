import os
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta
import math
import matplotlib.pyplot as plt
from classes.database import Database
from classes.image import Image
from classes.request import Request
from classes.link import Link

def apply_randomness(score: float):
    if score == 0.0:
        score = float(random.randint(0, 10)) / 100000.0
    else:
        score *= float(100.0 - random.randint(-10, 10)) / 100.0
    return score

def compute_image_rating(images: list[Image], requests: list[Request], links: list[Link], request_weight: float = 0.5, link_weight: float = 0.75):
    images_realtime_scores: list[tuple[Image, list[tuple[datetime, float]]]] = list()

    for image in images:
        min_created_at: datetime = image.created_at
        max_created_at: datetime = min(image.created_at + timedelta(days=1), datetime.now())
        image_realtime_scores: list[tuple[datetime, float]] = list()
        # Calculate request scores
        for request in requests:
            if request.image_id == image.id:
                new_score = request_weight
                # Apply randomness to the score
                new_score = apply_randomness(new_score)

                # Append new score into image_realtime_scores
                image_realtime_scores.append((request.created_at, new_score))


            if min_created_at > request.created_at:
                min_created_at = request.created_at

            if max_created_at < request.created_at:
                max_created_at = request.created_at

        for link in links:
            if link.image_id == image.id:
                new_score = link_weight
                # Apply randomness to the score
                new_score = apply_randomness(new_score)

                # Append new score into image_realtime_scores
                image_realtime_scores.append((link.created_at, new_score))

            

            if min_created_at > link.created_at:
                min_created_at = request.created_at

            if max_created_at < link.created_at:
                max_created_at = request.created_at

        # Sort images_realtime_scores in datetime ascending order
        sorted_image_realtime_scores: list[tuple[datetime, float]] = sorted(image_realtime_scores, key=lambda readltime_score: readltime_score[0], reverse=False)
        if len(sorted_image_realtime_scores) == 0:
            new_score = apply_randomness(0)
            sorted_image_realtime_scores.append((min_created_at, new_score))
            sorted_image_realtime_scores.append((max_created_at, apply_randomness(new_score * 1.1)))
            
        images_realtime_scores.append((image, sorted_image_realtime_scores))
    


    images_realtime_cumulative_score: list[tuple[Image, list[tuple[datetime, float]]]] = list()
    
    for image, image_realtime_scores in images_realtime_scores:
        realtime_cumulative_scores = list()
        cumulative_score: float = 0.0
        if len(image_realtime_scores) > 0:
            latest_datetime = image_realtime_scores[-1][0]
            for created_at, score in image_realtime_scores:
                cumulative_score += score * math.pow(1.01, (0 - (latest_datetime - created_at).total_seconds() / (60 * 60 * 24)))
                realtime_cumulative_scores.append((created_at, cumulative_score))
        images_realtime_cumulative_score.append((image, realtime_cumulative_scores))
    
    return images_realtime_cumulative_score

def get_recommended_images() -> list[Image]:

    load_dotenv()
    db = Database()   

    images: list[Image] = list()
    imgs = db.read("image")
    for img in imgs:
        images.append(Image(*img))

    requests: list[Request] = list()
    reqs = db.read("request")
    for req in reqs:
        requests.append(Request(*req))

    links: list[Link] = list()
    lnks = db.read("link")
    for lnk in lnks:
        links.append(Link(*lnk))

    images_realtime_cumulative_score = compute_image_rating(images, requests, links)

    recommended_images: list[Image] = [image for image, _ in images_realtime_cumulative_score]
    return recommended_images

def main() -> None:
    recommended_images: list[Image] = get_recommended_images()
    for recommended_image in recommended_images:
        print(recommended_image.id)

if __name__ == "__name__":
    main()