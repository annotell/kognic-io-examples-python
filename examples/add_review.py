from __future__ import absolute_import

from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model.review.review import (
    AddFeedbackItem,
    AddFeedbackItemPin,
    AddFeedbackItemSuggestedProperty,
    ReviewRequest,
    ReviewResponse,
    ReviewWorkflowEnum,
)


def run(client: KognicIOClient, open_label_uuid: str, error_type_id: str) -> ReviewResponse:
    review = ReviewRequest(
        feedback_items=[
            AddFeedbackItem(
                sensor_id="<the id/name of the sensor>",
                frame_id="<the id of the frame>",  # in our OpenLabel file this is frame.frame_properties.external_id
                object_id="<the id of the object>",
                pin=AddFeedbackItemPin(x=0.0, y=0.0, z=0.0),
                description="I post this via the Python client",
                suggested_property=AddFeedbackItemSuggestedProperty(
                    property_name="propertyName", suggested_property_value="suggestedPropertyValue"
                ),
                error_type_id=error_type_id,
                metadata={"key": "value"},
            )
        ],
        # Leave out workflow when the input is in an integration review phase, e.g. Client Automatic Review
        workflow=ReviewWorkflowEnum.CORRECT,
        accepted=False,
    )

    return client.review.create_review(open_label_uuid=open_label_uuid, body=review)


if __name__ == "__main__":
    setup_logging(level="DEBUG")

    client = KognicIOClient()

    open_label_uuid = "<the uuid of the OpenLABEL>"
    error_type_id = "<the id of the error type>"
    annotation = run(client, open_label_uuid, error_type_id)
