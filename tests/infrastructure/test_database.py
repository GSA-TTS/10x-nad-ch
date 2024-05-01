from conftest import TEST_COLUMN_MAPS_PATH
import yaml
from nad_ch.core.entities import (
    DataProducer,
    DataSubmissionStatus,
    DataSubmission,
    ColumnMap,
    User,
)


def test_add_producer(producers):
    new_producer = DataProducer("Producer A")
    saved_producer = producers.add(new_producer)
    assert saved_producer.id == 1
    assert saved_producer.created_at is not None
    assert saved_producer.updated_at is not None
    assert saved_producer.name == "Producer A"
    assert isinstance(saved_producer, DataProducer)


def test_producer_repo_get_by_name(producers_xyz):
    producer_name = "State X"

    retrieved_producer = producers_xyz.get_by_name(producer_name)
    assert retrieved_producer.id == 1
    assert retrieved_producer.created_at is not None
    assert retrieved_producer.updated_at is not None
    assert retrieved_producer.name == producer_name
    assert isinstance(retrieved_producer, DataProducer)


def test_producer_repo_get_all(producers_xyz):
    producer_names = ("State X", "State Y", "State Z")

    retrieved_producers = producers_xyz.get_all()
    assert len(retrieved_producers) == 3
    assert all(producer.id == i + 1 for i, producer in enumerate(retrieved_producers))
    assert all(producer.created_at is not None for producer in retrieved_producers)
    assert all(producer.updated_at is not None for producer in retrieved_producers)
    assert all(
        producer.name == producer_name
        for producer, producer_name in list(zip(retrieved_producers, producer_names))
    )
    assert isinstance(retrieved_producers[0], DataProducer)


def test_add_user(users):
    new_user = User(
        email="userY@gmail.com",
        login_provider="Y.com",
        logout_url="dummy logout value for Y",
    )
    saved_user = users.add(new_user)
    assert saved_user.id == 1
    assert saved_user.created_at is not None
    assert saved_user.updated_at is not None
    assert saved_user.email == "userY@gmail.com"
    assert saved_user.login_provider == "Y.com"
    assert saved_user.logout_url == "dummy logout value for Y"
    assert isinstance(saved_user, User)


def test_user_repo_get_by_email(users_xyz):
    retrieved_user = users_xyz.get_by_email("userY@gmail.com")
    assert retrieved_user.id == 2
    assert retrieved_user.created_at is not None
    assert retrieved_user.updated_at is not None
    assert retrieved_user.email == "userY@gmail.com"
    assert retrieved_user.login_provider == "Y.com"
    assert retrieved_user.logout_url == "dummy logout value for Y"
    assert isinstance(retrieved_user, User)


def test_user_repo_get_by_id(users_xyz):
    retrieved_user = users_xyz.get_by_id(3)
    assert retrieved_user.id == 3
    assert retrieved_user.created_at is not None
    assert retrieved_user.updated_at is not None
    assert retrieved_user.email == "userZ@gmail.com"
    assert retrieved_user.login_provider == "Z.com"
    assert retrieved_user.logout_url == "dummy logout value for Z"
    assert isinstance(retrieved_user, User)


def test_user_repo_get_all(users_xyz):
    user_names = ("X", "Y", "Z")
    retrieved_users = users_xyz.get_all()
    assert len(retrieved_users) == 3
    assert all(user.id == i + 1 for i, user in enumerate(retrieved_users))
    assert all(user.created_at is not None for user in retrieved_users)
    assert all(user.updated_at is not None for user in retrieved_users)
    assert all(
        user.email == f"user{user_name}@gmail.com"
        for user, user_name in list(zip(retrieved_users, user_names))
    )
    assert all(
        user.login_provider == f"{user_name}.com"
        for user, user_name in list(zip(retrieved_users, user_names))
    )
    assert all(
        user.logout_url == f"dummy logout value for {user_name}"
        for user, user_name in list(zip(retrieved_users, user_names))
    )
    assert isinstance(retrieved_users[0], User)


def test_add_column_map(column_maps, producers_xyz):
    producer = producers_xyz.get_by_name("State X")
    mapping = {"a": "1", "b": "2"}
    column_map = ColumnMap(
        name="testmap",
        producer=producer,
        mapping=mapping,
        version_id=2,
    )
    saved_column_map = column_maps.add(column_map)
    assert saved_column_map.id == 1
    assert saved_column_map.created_at is not None
    assert saved_column_map.updated_at is not None
    assert saved_column_map.name == "testmap"
    assert saved_column_map.version_id == 2
    assert saved_column_map.mapping == mapping
    assert isinstance(saved_column_map, ColumnMap)


def test_column_map_get_all(producer_column_maps):
    column_maps = producer_column_maps.get_all()
    for i, column_map in enumerate(column_maps):
        name = f"testproducer{i + 1}"
        assert column_map.id == i + 1
        assert column_map.created_at is not None
        assert column_map.updated_at is not None
        assert column_map.name == name
        assert column_map.version_id == 1
        test_column_map_path = f"{TEST_COLUMN_MAPS_PATH}/{name}.yaml"
        with open(test_column_map_path, "r") as file:
            mapping = yaml.safe_load(file)
        assert column_map.mapping == mapping
        assert isinstance(column_map, ColumnMap)


def test_column_map_get_by_data_submission(producer_column_maps_and_submissions):
    column_maps, submissions = producer_column_maps_and_submissions
    column_map1 = column_maps.get_by_data_submission(submissions.get_by_id(1))
    column_map2 = column_maps.get_by_data_submission(submissions.get_by_id(2))
    for i, column_map in enumerate((column_map1, column_map2)):
        name = f"testproducer{i + 1}"
        assert column_map.id == i + 1
        assert column_map.name == name
        test_column_map_path = f"{TEST_COLUMN_MAPS_PATH}/{name}.yaml"
        with open(test_column_map_path, "r") as file:
            mapping = yaml.safe_load(file)
        assert column_map.mapping == mapping
        assert isinstance(column_map, ColumnMap)


def test_column_map_get_by_name_and_version(producer_column_maps):
    column_map = producer_column_maps.get_by_name_and_version("testproducer1", 1)
    assert column_map.id == 1
    assert column_map.created_at is not None
    assert column_map.updated_at is not None
    assert column_map.name == "testproducer1"
    assert column_map.version_id == 1
    test_column_map_path = f"{TEST_COLUMN_MAPS_PATH}/testproducer1.yaml"
    with open(test_column_map_path, "r") as file:
        mapping = yaml.safe_load(file)
    assert column_map.mapping == mapping
    assert isinstance(column_map, ColumnMap)


def test_add_data_submission(repositories):
    producers, submissions, column_maps, users = repositories
    producer_name = "State X"
    new_producer = DataProducer(producer_name)
    saved_producer = producers.add(new_producer)
    new_column_map = ColumnMap("TestMap", saved_producer, version_id=1)
    saved_column_map = column_maps.add(new_column_map)
    new_submission = DataSubmission(
        "MySubmission",
        "my_submission.zip",
        DataSubmissionStatus.PENDING_VALIDATION,
        saved_producer,
        saved_column_map,
    )

    saved_submission = submissions.add(new_submission)

    assert saved_submission.id == 1
    assert saved_submission.created_at is not None
    assert saved_submission.updated_at is not None
    assert saved_submission.producer.id == saved_producer.id
    assert saved_submission.name == "MySubmission"


def test_data_submission_get_by_id(producer_column_maps_and_submissions):
    _, submissions = producer_column_maps_and_submissions
    submission = submissions.get_by_id(2)
    assert submission.id == 2
    assert submission.created_at is not None
    assert submission.updated_at is not None
    assert submission.report is None
    assert submission.producer.id == 2
    assert submission.column_map.id == 2
    assert submission.name == "testproducer2-submission"


def test_data_submission_get_by_producer(producer_column_maps_and_submissions):
    column_maps, submissions = producer_column_maps_and_submissions
    producer = column_maps.get_all()[1].producer
    submissions_entities = submissions.get_by_producer(producer)

    assert len(submissions_entities) == 1
    submission = submissions_entities[0]
    assert submission.id == 2
    assert submission.created_at is not None
    assert submission.updated_at is not None
    assert submission.report is None
    assert submission.producer.id == 2
    assert submission.column_map.id == 2
    assert submission.name == "testproducer2-submission"


def test_data_submission_update_report(producer_column_maps_and_submissions):
    _, submissions = producer_column_maps_and_submissions
    submission = submissions.get_by_id(2)
    assert submission.report is None
    assert submission.name == "testproducer2-submission"

    new_report = {"a": 1, "c": 2}
    submission = submissions.update_report(submission.id, new_report)
    assert submission.report == new_report
    assert submission.name == "testproducer2-submission"
