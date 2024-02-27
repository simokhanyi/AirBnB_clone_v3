#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import pep8
import unittest
from flask import Flask
from api.v1.views import app_views
from unittest.mock import patch, PropertyMock

State = state.State


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_f = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_state(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_state_module_docstring(self):
        """Test for the state.py module docstring"""
        self.assertIsNot(state.__doc__, None,
                         "state.py needs a docstring")
        self.assertTrue(len(state.__doc__) >= 1,
                        "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Test for the State class docstring"""
        self.assertIsNot(State.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_func_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for func in self.state_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestState(unittest.TestCase):
    """Test the State class"""

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute name, and it's as an empty string"""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        if models.storage_t == 'db':
            self.assertEqual(state.name, None)
        else:
            self.assertEqual(state.name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        s = State()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in s.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        s = State()
        new_d = s.to_dict()
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))


class TestStateAPI(unittest.TestCase):
    """Tests for State API endpoints"""

    @patch('api.v1.views.states.storage.all')
    def test_get_states(self, mock_storage_all):
        """Test retrieving list of states"""
        app = Flask(__name__)
        app.register_blueprint(app_views)
        with app.test_client() as client:
            mock_storage_all.return_value = {}
            response = client.get('/states')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])

    @patch('api.v1.views.states.storage.get')
    def test_get_state(self, mock_storage_get):
        """Test retrieving a state"""
        app = Flask(__name__)
        app.register_blueprint(app_views)
        with app.test_client() as client:
            mock_storage_get.return_value = None
            response = client.get('/states/1')
            self.assertEqual(response.status_code, 404)

    def test_get_state_stats(self):
        """Test retrieving state stats"""
        app = Flask(__name__)
        app.register_blueprint(app_views)
        with app.test_client() as client:
            response = client.get('/states/stats')
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['__class__'], 'State')

    @patch('api.v1.views.states.storage.new')
    @patch('api.v1.views.states.storage.save')
    def test_create_state(self, mock_storage_save, mock_storage_new):
        """Test creating a state"""
        app = Flask(__name__)
        app.register_blueprint(app_views)
        with app.test_client() as client:
            mock_storage_new.return_value = {}
            mock_storage_save.return_value = {}
            response = client.post('/states', json={'name': 'Test State'})
            self.assertEqual(response.status_code, 201)
            data = response.json
            self.assertEqual(data['name'], 'Test State')

    @patch('api.v1.views.states.storage.get')
    @patch('api.v1.views.states.storage.save')
    def test_update_state(self, mock_storage_save, mock_storage_get):
        """Test updating a state"""
        app = Flask(__name__)
        app.register_blueprint(app_views)
        with app.test_client() as client:
            mock_storage_get.return_value = None
            response = client.put('/states/1', json={'name': 'Updated State'})
            self.assertEqual(response.status_code, 404)

    @patch('api.v1.views.states.storage.get')
    @patch('api.v1.views.states.storage.delete')
    def test_delete_state(self, mock_storage_delete, mock_storage_get):
        """Test deleting a state"""
        app = Flask(__name__)
        app.register_blueprint(app_views)
        with app.test_client() as client:
            mock_storage_get.return_value = None
            response = client.delete('/states/1')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
