from __future__ import absolute_import

from typing import List

from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model.review.review import Review


def run(client: KognicIOClient, request_input_id: str) -> List[Review]:
    return client.review.get_auto_reviews(request_input_id=request_input_id)


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    request_input_id = "<request-input-id>"
    auto_reviews = run(client, request_input_id)
