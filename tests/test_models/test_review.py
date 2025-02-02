#!/usr/bin/python3
"""
Contains the TestReviewDocs classes
"""

from datetime import datetime
import inspect
import models
from models import review, place, user
from models.base_model import BaseModel
import pep8
import unittest
from api.v1.views import app_views
from flask import jsonify, abort, request

Review = review.Review
Place = place.Place
User = user.User


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Test that models/review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_review(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test for the Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestReview(unittest.TestCase):
    """Test the Review class"""

    def test_is_subclass(self):
        """Test if Review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Test Review has attr place_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.place_id, None)
        else:
            self.assertEqual(review.place_id, "")

    def test_user_id_attr(self):
        """Test Review has attr user_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.user_id, None)
        else:
            self.assertEqual(review.user_id, "")

    def test_text_attr(self):
        """Test Review has attr text, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        if models.storage_t == 'db':
            self.assertEqual(review.text, None)
        else:
            self.assertEqual(review.text, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in r.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], r.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], r.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))


class TestReviewAPI(unittest.TestCase):
    """Tests for Review API endpoints"""

    def test_get_reviews(self):
        """Test retrieving list of reviews of a place"""
        # Create a place and a review
        place = Place()
        review = Review()
        place.reviews.append(review)
        storage.new(place)
        storage.new(review)
        storage.save()

        # Request the reviews of the place
        response = app_views.test_client().get(f'/places/{place.id}/reviews')

        # Check if status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the review
        data = response.json
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], review.id)

    def test_get_review(self):
        """Test retrieving a review"""
        # Create a review
        review = Review()
        storage.new(review)
        storage.save()

        # Request the review
        response = app_views.test_client().get(f'/reviews/{review.id}')

        # Check if status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the review
        data = response.json
        self.assertEqual(data['id'], review.id)

    def test_delete_review(self):
        """Test deleting a review"""
        # Create a review
        review = Review()
        storage.new(review)
        storage.save()

        # Delete the review
        response = app_views.test_client().delete(f'/reviews/{review.id}')

        # Check if status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the review is deleted
        deleted_review = storage.get(Review, review.id)
        self.assertIsNone(deleted_review)

    def test_create_review(self):
        """Test creating a review"""
        # Create a user and a place
        user = User()
        place = Place()
        storage.new(user)
        storage.new(place)
        storage.save()

        # Create review data
        review_data = {
            'user_id': user.id,
            'text': 'Great place!'
        }

        # Create the review
        response =(
            app_views.test_client()
            .post(f'/places/{place.id}/reviews', json=review_data)
        )

        # Check if status code is 201
        self.assertEqual(response.status_code, 201)

        # Check if the review is created
        data = response.json
        created_review = storage.get(Review, data['id'])
        self.assertIsNotNone(created_review)
        self.assertEqual(created_review.user_id, user.id)
        self.assertEqual(created_review.text, 'Great place!')

    def test_update_review(self):
        """Test updating a review"""
        # Create a review
        review = Review()
        storage.new(review)
        storage.save()

        # Update review data
        updated_data = {
            'text': 'Updated review!'
        }

        # Update the review
        response = (
            app_views.test_client()
            .put(f'/reviews/{review.id}', json=updated_data)
        )

        # Check if status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the review is updated
        updated_review = storage.get(Review, review.id)
        self.assertEqual(updated_review.text, 'Updated review!')


if __name__ == '__main__':
    unittest.main()
