from code.app.models.posts import PostBase
from code.database.declarations.posts import get_posts, get_post, get_user_posts, edit_post_in_db, \
    parse_post_to_response

"""
Unable to test those functions: add_post, get_posts_containing because:
 - add_posts requires uuid (not supported in sqlLight used for mocking)
 - get_posts_containing uses elastic search, which is not mocked
"""



def test_get_posts(mocked_session):
    posts = get_posts(mocked_session, "2")
    assert len(posts) == 2
    assert posts[0].title == "Test Post"
    assert posts[0].description == "Test Post Description"
    assert posts[0].author_id == "1"
    assert posts[1].title == "Test Post 2"
    assert posts[1].description == "Test Post Description 2"

def test_get_posts_diff_estate(mocked_session):
    posts = get_posts(mocked_session, "3")
    assert len(posts) == 1
    assert posts[0].title == "Test Post 3"
    assert posts[0].description == "Test Post Description 3"
    assert posts[0].author_id == "3"

def test_get_post(mocked_session):
    post = get_post(mocked_session, "1")
    assert post.title == "Test Post"
    assert post.description == "Test Post Description"
    assert post.author_id == "1"

def test_get_user_posts(mocked_session):
    posts = get_user_posts(mocked_session, "1")
    assert len(posts) == 1
    assert posts[0].title == "Test Post"
    assert posts[0].description == "Test Post Description"
    assert posts[0].author_id == "1"

def test_edit_post_in_db(mocked_session):
    post = get_post(mocked_session, "1")
    assert post.title == "Test Post"
    assert post.description == "Test Post Description"
    new_post = PostBase(title="New Title", description="New Description")

    post = edit_post_in_db(mocked_session, "1", new_post)
    assert post.title == "New Title"
    assert post.description == "New Description"
    assert post.author_id == "1"
    assert post.created_at is not None

def test_edit_post_in_db_not_existing(mocked_session):
    post = get_post(mocked_session, "1")
    assert post.title == "Test Post"
    assert post.description == "Test Post Description"
    new_post = PostBase(title="New Title", description="New Description")

    post = edit_post_in_db(mocked_session, "100", new_post)
    assert post is None

def test_parse_post_to_response(mocked_session):
    parsed_post = parse_post_to_response(mocked_session, get_post(mocked_session, "1"))
    assert parsed_post.id == "1"
    assert parsed_post.title == "Test Post"
    assert parsed_post.description == "Test Post Description"
    assert parsed_post.author_name == "Scott, Kevin"





