from kognic.io.model import Position, RotationQuaternion
from kognic.io.model.calibration.camera.custom_camera_calibration import CustomCameraCalibration, Point2d, Point3d, TestCase


def example_custom_camera_calibration():
    camera_position = Position(x=0.0, y=0.0, z=0.0)
    camera_rotation = RotationQuaternion(w=1.0, x=0.0, y=0.0, z=0.0)

    points = [
        Point3d(x=3, y=1, z=4),
        Point3d(x=1, y=5, z=9),
        Point3d(x=2, y=6, z=5),
        Point3d(x=3, y=5, z=8),
        Point3d(x=7, y=9, z=-3),
    ]
    expected = [
        Point2d(x=3411.33796820, y=1457.47007896),
        Point2d(x=2140.20057104, y=1964.16186360),
        Point2d(x=2855.80249826, y=3218.94856504),
        Point2d(x=2607.03503582, y=2058.95553923),
        Point2d(x=-1, y=-1),  # Point is behind camera
    ]

    test_cases = [TestCase(point3d=point3d, point2d=point2d) for point3d, point2d in zip(points, expected, strict=True)]

    return CustomCameraCalibration.from_file(
        wasm_path="./examples/resources/pinhole.wasm",
        position=camera_position,
        rotation_quaternion=camera_rotation,
        test_cases=test_cases,
        image_height=1080,
        image_width=1920,
    )
